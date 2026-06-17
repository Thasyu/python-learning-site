import ast

#システムがコードを実行する関数
from backend.app.sandbox import run_in_sandbox

#ユーザーの入力を正規化する関数
def normalize_output(text):
    return text.strip().replace("\r\n", "\n").replace("\r", "\n")

def validate_output_by_rule(actual_output, validator_name):
    lines = [line.strip() for line in normalize_output(actual_output).split("\n") if line.strip() != ""]

    if validator_name == "non_empty":
        return len(lines) > 0

    if validator_name and validator_name.startswith("int_range_"):
        # e.g. int_range_1_10 or int_range_1_10_lines3
        parts = validator_name.split("_")
        if len(parts) not in (4, 5):
            return False
        try:
            min_v = int(parts[2])
            max_v = int(parts[3])
            required_lines = int(parts[4].replace("lines", "")) if len(parts) == 5 else None
        except ValueError:
            return False

        if required_lines is not None and len(lines) != required_lines:
            return False
        if len(lines) == 0:
            return False

        for line in lines:
            try:
                value = int(line)
            except ValueError:
                return False
            if value < min_v or value > max_v:
                return False
        return True

    # Unknown validator should fail-safe.
    return False

def contains_required_keywords(user_code, required_keywords):
    normalize_code = user_code.replace(" ", "").replace('"', "'")
    for keyword in required_keywords:
        if keyword not in normalize_code:
            return False
    return True


def resolve_rule_value(rule, question_data, literal_key, generated_key_name):
    if literal_key in rule:
        return rule.get(literal_key)

    generated_values = (question_data or {}).get("generated_values") or {}
    generated_key = rule.get(generated_key_name)
    if isinstance(generated_key, str):
        return generated_values.get(generated_key)

    return None


def get_dotted_name(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        base_name = get_dotted_name(node.value)
        if base_name is None:
            return None
        return f"{base_name}.{node.attr}"

    return None


def has_subscript_assignment(module_node, object_name=None):
    for node in ast.walk(module_node):
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if not isinstance(target, ast.Subscript):
                continue
            if object_name is None or get_dotted_name(target.value) == object_name:
                return True

    return False


def has_subscript_delete(module_node, object_name=None):
    for node in ast.walk(module_node):
        if not isinstance(node, ast.Delete):
            continue

        for target in node.targets:
            if not isinstance(target, ast.Subscript):
                continue
            if object_name is None or get_dotted_name(target.value) == object_name:
                return True

    return False


def resolve_operator_class(symbol):
    binary_operator_map = {
        "+": ast.Add,
        "-": ast.Sub,
        "*": ast.Mult,
        "/": ast.Div,
        "//": ast.FloorDiv,
        "%": ast.Mod,
        "**": ast.Pow,
    }
    compare_operator_map = {
        "==": ast.Eq,
        "!=": ast.NotEq,
        ">": ast.Gt,
        "<": ast.Lt,
        ">=": ast.GtE,
        "<=": ast.LtE,
    }

    if symbol in binary_operator_map:
        return "binary", binary_operator_map[symbol]
    if symbol in compare_operator_map:
        return "compare", compare_operator_map[symbol]

    return None, None


def infer_expression_kind(node, symbol_kinds):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return "unknown"
        if isinstance(node.value, (int, float, complex)):
            return "number"
        if isinstance(node.value, str):
            return "string"
        return "unknown"

    if isinstance(node, ast.Name):
        return symbol_kinds.get(node.id, "unknown")

    if isinstance(node, ast.UnaryOp):
        operand_kind = infer_expression_kind(node.operand, symbol_kinds)
        if operand_kind == "number" and isinstance(node.op, (ast.UAdd, ast.USub)):
            return "number"
        return "unknown"

    if isinstance(node, ast.BinOp):
        left_kind = infer_expression_kind(node.left, symbol_kinds)
        right_kind = infer_expression_kind(node.right, symbol_kinds)

        if left_kind == "number" and right_kind == "number" and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
            return "number"

        if left_kind == "string" and right_kind == "string" and isinstance(node.op, ast.Add):
            return "string"

        return "unknown"

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and len(node.args) == 1:
        if node.func.id in {"int", "float"}:
            return "number"
        if node.func.id == "str":
            return "string"

    if isinstance(node, ast.JoinedStr):
        return "string"

    return "unknown"


def collect_symbol_kinds(module_node):
    symbol_kinds = {}

    def set_target_kind(target, kind):
        if isinstance(target, ast.Name):
            symbol_kinds[target.id] = kind

    for node in module_node.body:
        if isinstance(node, ast.Assign):
            value_kind = infer_expression_kind(node.value, symbol_kinds)
            for target in node.targets:
                set_target_kind(target, value_kind)
        elif isinstance(node, ast.AnnAssign):
            value_kind = infer_expression_kind(node.value, symbol_kinds) if node.value is not None else "unknown"
            set_target_kind(node.target, value_kind)
        elif isinstance(node, ast.AugAssign):
            current_kind = infer_expression_kind(node.target, symbol_kinds)
            value_kind = infer_expression_kind(node.value, symbol_kinds)

            if current_kind == "number" and value_kind == "number" and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
                set_target_kind(node.target, "number")
            elif current_kind == "string" and value_kind == "string" and isinstance(node.op, ast.Add):
                set_target_kind(node.target, "string")
            else:
                set_target_kind(node.target, "unknown")

    return symbol_kinds


def find_print_calls(module_node):
    print_calls = []

    for node in ast.walk(module_node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            print_calls.append(node)

    return print_calls


def make_abstract_value(is_known, value, dependencies):
    return {
        "is_known": is_known,
        "value": value,
        "dependencies": set(dependencies),
    }


def unknown_value(dependencies=None):
    return make_abstract_value(False, None, dependencies or set())


def known_value(value, dependencies=None):
    return make_abstract_value(True, value, dependencies or set())


def assign_value_to_target(environment, target, abstract_value):
    if isinstance(target, ast.Name):
        environment[target.id] = make_abstract_value(
            abstract_value["is_known"],
            abstract_value["value"],
            set(abstract_value["dependencies"]) | {target.id},
        )


def apply_binary_operator(left_value, right_value, operator_node):
    dependencies = set(left_value["dependencies"]) | set(right_value["dependencies"])

    if not left_value["is_known"] or not right_value["is_known"]:
        return unknown_value(dependencies)

    try:
        if isinstance(operator_node, ast.Add):
            return known_value(left_value["value"] + right_value["value"], dependencies)
        if isinstance(operator_node, ast.Sub):
            return known_value(left_value["value"] - right_value["value"], dependencies)
        if isinstance(operator_node, ast.Mult):
            return known_value(left_value["value"] * right_value["value"], dependencies)
        if isinstance(operator_node, ast.Div):
            return known_value(left_value["value"] / right_value["value"], dependencies)
        if isinstance(operator_node, ast.FloorDiv):
            return known_value(left_value["value"] // right_value["value"], dependencies)
        if isinstance(operator_node, ast.Mod):
            return known_value(left_value["value"] % right_value["value"], dependencies)
        if isinstance(operator_node, ast.Pow):
            return known_value(left_value["value"] ** right_value["value"], dependencies)
    except Exception:
        return unknown_value(dependencies)

    return unknown_value(dependencies)


def evaluate_abstract_value(node, environment):
    if isinstance(node, ast.Constant):
        return known_value(node.value)

    if isinstance(node, ast.Name):
        return environment.get(node.id, unknown_value({node.id}))

    if isinstance(node, ast.UnaryOp):
        operand_value = evaluate_abstract_value(node.operand, environment)
        dependencies = set(operand_value["dependencies"])

        if not operand_value["is_known"]:
            return unknown_value(dependencies)

        try:
            if isinstance(node.op, ast.UAdd):
                return known_value(+operand_value["value"], dependencies)
            if isinstance(node.op, ast.USub):
                return known_value(-operand_value["value"], dependencies)
        except Exception:
            return unknown_value(dependencies)

        return unknown_value(dependencies)

    if isinstance(node, ast.BinOp):
        left_value = evaluate_abstract_value(node.left, environment)
        right_value = evaluate_abstract_value(node.right, environment)
        return apply_binary_operator(left_value, right_value, node.op)

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and len(node.args) == 1:
        arg_value = evaluate_abstract_value(node.args[0], environment)
        dependencies = set(arg_value["dependencies"])

        if node.func.id == "int" and arg_value["is_known"]:
            try:
                return known_value(int(arg_value["value"]), dependencies)
            except Exception:
                return unknown_value(dependencies)

        if node.func.id == "float" and arg_value["is_known"]:
            try:
                return known_value(float(arg_value["value"]), dependencies)
            except Exception:
                return unknown_value(dependencies)

        if node.func.id == "str" and arg_value["is_known"]:
            try:
                return known_value(str(arg_value["value"]), dependencies)
            except Exception:
                return unknown_value(dependencies)

        return unknown_value(dependencies)

    if isinstance(node, ast.JoinedStr):
        dependencies = set()
        pieces = []

        for value in node.values:
            abstract_value = evaluate_abstract_value(value, environment) if isinstance(value, ast.FormattedValue) else known_value(value.value)
            dependencies |= set(abstract_value["dependencies"])
            if not abstract_value["is_known"]:
                return unknown_value(dependencies)
            pieces.append(str(abstract_value["value"]))

        return known_value("".join(pieces), dependencies)

    if isinstance(node, ast.FormattedValue):
        return evaluate_abstract_value(node.value, environment)

    return unknown_value()


def analyze_module_execution(module_node):
    environment = {}
    assignment_records = []
    print_records = []

    for statement_index, statement in enumerate(module_node.body):
        if isinstance(statement, ast.Assign):
            abstract_value = evaluate_abstract_value(statement.value, environment)
            for target in statement.targets:
                assign_value_to_target(environment, target, abstract_value)
                if isinstance(target, ast.Name):
                    assignment_records.append({
                        "statement_index": statement_index,
                        "target": target.id,
                        "value": environment[target.id],
                        "node": statement,
                    })
            continue

        if isinstance(statement, ast.AnnAssign) and statement.value is not None:
            abstract_value = evaluate_abstract_value(statement.value, environment)
            assign_value_to_target(environment, statement.target, abstract_value)
            if isinstance(statement.target, ast.Name):
                assignment_records.append({
                    "statement_index": statement_index,
                    "target": statement.target.id,
                    "value": environment[statement.target.id],
                    "node": statement,
                })
            continue

        if isinstance(statement, ast.AugAssign):
            current_value = evaluate_abstract_value(statement.target, environment)
            change_value = evaluate_abstract_value(statement.value, environment)
            updated_value = apply_binary_operator(current_value, change_value, statement.op)
            assign_value_to_target(environment, statement.target, updated_value)
            if isinstance(statement.target, ast.Name):
                assignment_records.append({
                    "statement_index": statement_index,
                    "target": statement.target.id,
                    "value": environment[statement.target.id],
                    "node": statement,
                })
            continue

        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            call = statement.value
            if isinstance(call.func, ast.Name) and call.func.id == "print":
                print_records.append({
                    "statement_index": statement_index,
                    "call": call,
                    "args": [evaluate_abstract_value(arg, environment) for arg in call.args],
                    "environment": {
                        name: make_abstract_value(value["is_known"], value["value"], set(value["dependencies"]))
                        for name, value in environment.items()
                    },
                })

    return {
        "assignments": assignment_records,
        "prints": print_records,
    }


def build_generated_bindings(question_data, binding_specs):
    generated_values = question_data.get("generated_values") or {}
    bindings = []

    for spec in binding_specs:
        variable_name = spec.get("name") if isinstance(spec.get("name"), str) else generated_values.get(spec.get("name_key"))
        expected_value = spec.get("value") if "value" in spec else generated_values.get(spec.get("value_key"))
        bindings.append({
            "variable_name": variable_name,
            "expected_value": expected_value,
        })

    return bindings


def validate_print_argument_kind(module_node, rule, question_data=None):
    print_calls = find_print_calls(module_node)
    if not print_calls:
        return False, "print() を使って出力してください。"

    print_index = rule.get("print_index", 0)
    arg_index = rule.get("arg_index", 0)
    expected_kind = rule.get("expected_kind")

    if print_index >= len(print_calls):
        return False, "指定された print() が見つかりません。"

    print_call = print_calls[print_index]
    if arg_index >= len(print_call.args):
        return False, "print() の引数が不足しています。"

    symbol_kinds = collect_symbol_kinds(module_node)
    actual_kind = infer_expression_kind(print_call.args[arg_index], symbol_kinds)

    if actual_kind == expected_kind:
        return True, None

    labels = {
        "number": "数値",
        "string": "文字列"
    }
    expected_label = labels.get(expected_kind, expected_kind)
    return False, f"print() の {arg_index + 1} 番目の引数は{expected_label}として出力してください。"


def validate_require_node_type(module_node, rule, question_data=None):
    node_type = rule.get("node_type")
    if not isinstance(node_type, str) or not hasattr(ast, node_type):
        return False, f"未対応の AST ルールです: {node_type}"

    node_class = getattr(ast, node_type)
    if any(isinstance(node, node_class) for node in ast.walk(module_node)):
        return True, None

    labels = {
        "Assign": "変数代入",
        "If": "if 文",
        "For": "for 文",
        "FunctionDef": "関数定義"
    }
    required_label = labels.get(node_type, node_type)
    return False, f"{required_label}を使ってください。"


def validate_require_generated_variables_in_print(module_node, rule, question_data=None):
    print_calls = find_print_calls(module_node)
    if not print_calls:
        return False, "print() を使って出力してください。"

    print_index = rule.get("print_index", 0)
    arg_index = rule.get("arg_index", 0)

    if print_index >= len(print_calls):
        return False, "指定された print() が見つかりません。"

    print_call = print_calls[print_index]
    if arg_index >= len(print_call.args):
        return False, "print() の引数が不足しています。"

    generated_values = (question_data or {}).get("generated_values") or {}
    variable_keys = rule.get("variable_keys") or []

    required_vars = []
    for key in variable_keys:
        value = generated_values.get(key)
        if isinstance(value, str):
            required_vars.append(value)

    if not required_vars:
        return False, "採点設定エラー: 必須変数が取得できません。"

    print_expr = print_call.args[arg_index]
    used_names = {
        node.id
        for node in ast.walk(print_expr)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }

    missing_vars = [var_name for var_name in required_vars if var_name not in used_names]
    if not missing_vars:
        return True, None

    return False, f"print() の式で指定された変数を使ってください: {', '.join(missing_vars)}"


def validate_generated_bindings_at_print(module_node, rule, question_data=None):
    analysis = analyze_module_execution(module_node)
    print_index = rule.get("print_index", 0)
    arg_index = rule.get("arg_index", 0)

    if print_index >= len(analysis["prints"]):
        return False, "指定された print() が見つかりません。"

    print_record = analysis["prints"][print_index]
    if arg_index >= len(print_record["args"]):
        return False, "print() の引数が不足しています。"

    binding_specs = rule.get("bindings") or []
    bindings = build_generated_bindings(question_data or {}, binding_specs)
    if not bindings:
        return False, "採点設定エラー: 必須変数が取得できません。"

    missing_dependencies = []
    argument_value = print_record["args"][arg_index]
    for binding in bindings:
        variable_name = binding["variable_name"]
        if not isinstance(variable_name, str) or variable_name not in argument_value["dependencies"]:
            missing_dependencies.append(variable_name)

    if missing_dependencies:
        return False, f"print() の式で指定された変数を使ってください: {', '.join(missing_dependencies)}"

    wrong_values = []
    for binding in bindings:
        variable_name = binding["variable_name"]
        expected_value = binding["expected_value"]
        actual_value = print_record["environment"].get(variable_name)

        if actual_value is None or not actual_value["is_known"] or actual_value["value"] != expected_value:
            wrong_values.append(f"{variable_name}={expected_value}")

    if wrong_values:
        return False, f"指定された値を代入した変数を使ってください: {', '.join(wrong_values)}"

    return True, None


def validate_generated_bindings_before_print(module_node, rule, question_data=None):
    analysis = analyze_module_execution(module_node)
    print_index = rule.get("print_index", 0)

    if print_index >= len(analysis["prints"]):
        return False, "指定された print() が見つかりません。"

    print_statement_index = analysis["prints"][print_index]["statement_index"]
    binding_specs = rule.get("bindings") or []
    bindings = build_generated_bindings(question_data or {}, binding_specs)
    if not bindings:
        return False, "採点設定エラー: 必須変数が取得できません。"

    missing_assignments = []
    for binding in bindings:
        variable_name = binding["variable_name"]
        expected_value = binding["expected_value"]
        found = False

        for record in analysis["assignments"]:
            if record["statement_index"] >= print_statement_index:
                continue
            if record["target"] != variable_name:
                continue
            if record["value"]["is_known"] and record["value"]["value"] == expected_value:
                found = True
                break

        if not found:
            missing_assignments.append(f"{variable_name}={expected_value}")

    if missing_assignments:
        return False, f"指定された値の代入が必要です: {', '.join(missing_assignments)}"

    return True, None


def validate_self_update_assignment(module_node, rule, question_data=None):
    analysis = analyze_module_execution(module_node)
    print_index = rule.get("print_index", 0)
    if print_index >= len(analysis["prints"]):
        return False, "指定された print() が見つかりません。"

    generated_values = (question_data or {}).get("generated_values") or {}
    variable_name = generated_values.get(rule.get("variable_key"))
    operator_symbol = generated_values.get(rule.get("operator_key"))
    expected_change = generated_values.get(rule.get("change_key"))
    print_statement_index = analysis["prints"][print_index]["statement_index"]

    operator_map = {
        "+": ast.Add,
        "-": ast.Sub,
        "*": ast.Mult,
        "/": ast.Div,
        "//": ast.FloorDiv,
        "%": ast.Mod,
        "**": ast.Pow,
    }
    operator_class = operator_map.get(operator_symbol)
    if not isinstance(variable_name, str) or operator_class is None:
        return False, "採点設定エラー: 更新ルールが不正です。"

    for record in analysis["assignments"]:
        if record["statement_index"] >= print_statement_index:
            continue
        node = record["node"]
        if not isinstance(node, ast.Assign) or record["target"] != variable_name:
            continue
        if not isinstance(node.value, ast.BinOp) or not isinstance(node.value.op, operator_class):
            continue
        if not isinstance(node.value.left, ast.Name) or node.value.left.id != variable_name:
            continue

        right_value = evaluate_abstract_value(node.value.right, {})
        if right_value["is_known"] and right_value["value"] == expected_change:
            return True, None

    return False, f"{variable_name} = {variable_name} {operator_symbol} {expected_change} の形で更新してください。"


def validate_augassign_update(module_node, rule, question_data=None):
    analysis = analyze_module_execution(module_node)
    print_index = rule.get("print_index", 0)
    if print_index >= len(analysis["prints"]):
        return False, "指定された print() が見つかりません。"

    generated_values = (question_data or {}).get("generated_values") or {}
    variable_name = generated_values.get(rule.get("variable_key"))
    operator_symbol = generated_values.get(rule.get("operator_key"))
    expected_change = generated_values.get(rule.get("change_key"))
    print_statement_index = analysis["prints"][print_index]["statement_index"]

    operator_map = {
        "+": ast.Add,
        "-": ast.Sub,
        "*": ast.Mult,
        "//": ast.FloorDiv,
        "%": ast.Mod,
    }
    operator_class = operator_map.get(operator_symbol)
    if not isinstance(variable_name, str) or operator_class is None:
        return False, "採点設定エラー: 更新ルールが不正です。"

    for record in analysis["assignments"]:
        if record["statement_index"] >= print_statement_index:
            continue
        node = record["node"]
        if not isinstance(node, ast.AugAssign):
            continue
        if not isinstance(node.target, ast.Name) or node.target.id != variable_name:
            continue
        if not isinstance(node.op, operator_class):
            continue

        value = evaluate_abstract_value(node.value, {})
        if value["is_known"] and value["value"] == expected_change:
            return True, None

    return False, f"{variable_name} {operator_symbol}= {expected_change} の形で更新してください。"


def collect_if_compare_clauses(module_node):
    clauses = []

    for statement in module_node.body:
        if not isinstance(statement, ast.If):
            continue

        current = statement
        while True:
            clauses.append({
                "test": current.test,
                "lineno": getattr(current, "lineno", 10**9),
            })

            if len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                current = current.orelse[0]
                continue

            break

    return clauses


def collect_environment_before_line(module_node, target_line):
    environment = {}

    for statement in module_node.body:
        statement_line = getattr(statement, "lineno", 10**9)
        if statement_line >= target_line:
            break

        if isinstance(statement, ast.Assign):
            abstract_value = evaluate_abstract_value(statement.value, environment)
            for target in statement.targets:
                assign_value_to_target(environment, target, abstract_value)
            continue

        if isinstance(statement, ast.AnnAssign) and statement.value is not None:
            abstract_value = evaluate_abstract_value(statement.value, environment)
            assign_value_to_target(environment, statement.target, abstract_value)
            continue

        if isinstance(statement, ast.AugAssign):
            current_value = evaluate_abstract_value(statement.target, environment)
            change_value = evaluate_abstract_value(statement.value, environment)
            updated_value = apply_binary_operator(current_value, change_value, statement.op)
            assign_value_to_target(environment, statement.target, updated_value)

    return environment


def validate_generated_compare_clause(module_node, rule, question_data=None):
    clauses = collect_if_compare_clauses(module_node)
    clause_index = rule.get("clause_index", 0)
    if clause_index >= len(clauses):
        return False, "指定された if/elif 条件式が見つかりません。"

    clause = clauses[clause_index]
    test = clause["test"]
    if not isinstance(test, ast.Compare):
        return False, "if/elif の条件式で比較演算子を使ってください。"

    operator_symbol = resolve_rule_value(rule, question_data, "operator", "operator_key")
    operator_map = {
        "==": ast.Eq,
        "!=": ast.NotEq,
        ">": ast.Gt,
        "<": ast.Lt,
        ">=": ast.GtE,
        "<=": ast.LtE,
    }
    operator_class = operator_map.get(operator_symbol)
    if operator_class is None:
        return False, "採点設定エラー: 比較演算子が不正です。"

    if len(test.ops) != 1 or not isinstance(test.ops[0], operator_class):
        return False, f"if/elif の条件式で {operator_symbol} を使ってください。"

    expected_compare_value = resolve_rule_value(rule, question_data, "compare_value", "compare_value_key")
    if expected_compare_value is not None:
        if len(test.comparators) != 1:
            return False, "比較式の形が不正です。"

        environment = collect_environment_before_line(module_node, clause["lineno"])
        actual_compare_value = evaluate_abstract_value(test.comparators[0], environment)
        if (
            not actual_compare_value["is_known"]
            or actual_compare_value["value"] != expected_compare_value
        ):
            return False, f"if/elif の比較値は {expected_compare_value} を使ってください。"

    binding_specs = rule.get("bindings") or []
    bindings = build_generated_bindings(question_data or {}, binding_specs)
    if not bindings:
        return False, "採点設定エラー: 必須変数が取得できません。"

    required_variables = []
    for binding in bindings:
        variable_name = binding["variable_name"]
        if not isinstance(variable_name, str):
            return False, "採点設定エラー: 変数名の設定が不正です。"
        required_variables.append(variable_name)

    used_names = {
        node.id
        for node in ast.walk(test)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }

    missing_variables = [name for name in required_variables if name not in used_names]
    if missing_variables:
        return False, f"if/elif の条件式で指定された変数を使ってください: {', '.join(missing_variables)}"

    environment = collect_environment_before_line(module_node, clause["lineno"])
    wrong_values = []
    for binding in bindings:
        variable_name = binding["variable_name"]
        expected_value = binding["expected_value"]
        actual_value = environment.get(variable_name)

        if actual_value is None or not actual_value["is_known"] or actual_value["value"] != expected_value:
            wrong_values.append(f"{variable_name}={expected_value}")

    if wrong_values:
        return False, f"指定された値の代入が必要です: {', '.join(wrong_values)}"

    return True, None


def validate_require_node(module_node, rule, question_data=None):
    """任意の AST ノードタイプがコード中に存在するか確認する。
    rule: { "type": "require_node", "node_type": "For", "message": "for文を使ってください。" }
    """
    node_type = rule.get("node_type")
    if not node_type or not hasattr(ast, node_type):
        return False, f"採点設定エラー: 未対応の AST ノードタイプです: {node_type}"
    node_class = getattr(ast, node_type)
    if any(isinstance(n, node_class) for n in ast.walk(module_node)):
        return True, None
    message = rule.get("message") or f"{node_type} を使ってください。"
    return False, message


def validate_require_function_call(module_node, rule, question_data=None):
    """特定の関数呼び出しがコード中に存在するか確認する。
    rule: { "type": "require_function_call", "name": "print", "message": "..." }
    """
    name = resolve_rule_value(rule, question_data, "name", "name_key")
    if not name:
        return False, "採点設定エラー: require_function_call に name が指定されていません。"
    for node in ast.walk(module_node):
        if (
            isinstance(node, ast.Call)
            and get_dotted_name(node.func) == name
        ):
            return True, None
    message = rule.get("message") or f"{name}() を呼び出してください。"
    return False, message


def validate_require_method_call(module_node, rule, question_data=None):
    """特定のメソッド呼び出しがコード中に存在するか確認する。
    rule: { "type": "require_method_call", "method": "append", "message": "..." }
    object を指定する場合は "object" キーを追加する (省略時はメソッド名のみで一致)。
    """
    method = resolve_rule_value(rule, question_data, "method", "method_key")
    if not method:
        return False, "採点設定エラー: require_method_call に method が指定されていません。"
    object_name = resolve_rule_value(rule, question_data, "object", "object_key")
    for node in ast.walk(module_node):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == method
        ):
            if object_name is None:
                return True, None
            if get_dotted_name(node.func.value) == object_name:
                return True, None
    message = rule.get("message") or f".{method}() を呼び出してください。"
    return False, message


def validate_require_import(module_node, rule, question_data=None):
    """特定のモジュールがインポートされているか確認する。
    rule: { "type": "require_import", "module": "random", "message": "..." }
    """
    module = resolve_rule_value(rule, question_data, "module", "module_key")
    if not module:
        return False, "採点設定エラー: require_import に module が指定されていません。"
    for node in ast.walk(module_node):
        if isinstance(node, ast.Import):
            if any(alias.name == module or alias.name.startswith(module + ".") for alias in node.names):
                return True, None
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod == module or mod.startswith(module + "."):
                return True, None
    message = rule.get("message") or f"{module} をインポートしてください。"
    return False, message


def validate_require_function_def(module_node, rule, question_data=None):
    """関数定義が存在するか確認する。name を指定するとその名前の関数のみ対象。
    rule: { "type": "require_function_def", "name": "greet", "message": "..." }
    """
    name = resolve_rule_value(rule, question_data, "name", "name_key")
    for node in ast.walk(module_node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if name is None or node.name == name:
                return True, None
    if name:
        message = rule.get("message") or f"{name}() 関数を定義してください。"
    else:
        message = rule.get("message") or "関数を定義してください。"
    return False, message


def validate_require_try_except(module_node, rule, question_data=None):
    """try/except ブロックが存在するか確認する。
    rule: { "type": "require_try_except", "message": "..." }
    """
    for node in ast.walk(module_node):
        if isinstance(node, ast.Try) and node.handlers:
            return True, None
    message = rule.get("message") or "try/except を使ってください。"
    return False, message


def validate_require_finally(module_node, rule, question_data=None):
    """try/finally ブロックが存在するか確認する。
    rule: { "type": "require_finally", "message": "..." }
    """
    for node in ast.walk(module_node):
        if isinstance(node, ast.Try) and node.finalbody:
            return True, None
    message = rule.get("message") or "finally ブロックを使ってください。"
    return False, message


def validate_require_attribute_access(module_node, rule, question_data=None):
    attr_name = resolve_rule_value(rule, question_data, "attr", "attr_key")
    object_name = resolve_rule_value(rule, question_data, "object", "object_key")
    if not attr_name:
        return False, "採点設定エラー: require_attribute_access に attr が指定されていません。"

    for node in ast.walk(module_node):
        if not isinstance(node, ast.Attribute) or node.attr != attr_name:
            continue
        if object_name is None or get_dotted_name(node.value) == object_name:
            return True, None

    message = rule.get("message") or f".{attr_name} を使ってください。"
    return False, message


def validate_require_operator(module_node, rule, question_data=None):
    symbol = resolve_rule_value(rule, question_data, "symbol", "symbol_key")
    if not symbol:
        return False, "採点設定エラー: require_operator に symbol が指定されていません。"

    operator_kind, operator_class = resolve_operator_class(symbol)
    if operator_class is None:
        return False, f"採点設定エラー: 未対応の演算子です: {symbol}"

    for node in ast.walk(module_node):
        if operator_kind == "binary":
            if isinstance(node, ast.BinOp) and isinstance(node.op, operator_class):
                return True, None
            if isinstance(node, ast.AugAssign) and isinstance(node.op, operator_class):
                return True, None
        elif operator_kind == "compare":
            if isinstance(node, ast.Compare) and any(isinstance(op, operator_class) for op in node.ops):
                return True, None

    message = rule.get("message") or f"{symbol} を使ってください。"
    return False, message


def validate_require_if_else(module_node, rule, question_data=None):
    for node in ast.walk(module_node):
        if not isinstance(node, ast.If) or not node.orelse:
            continue
        if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            continue
        return True, None

    message = rule.get("message") or "else を含む if 文を使ってください。"
    return False, message


def validate_require_if_elif_else(module_node, rule, question_data=None):
    for node in ast.walk(module_node):
        if not isinstance(node, ast.If):
            continue

        current = node
        saw_elif = False
        while len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
            saw_elif = True
            current = current.orelse[0]

        if saw_elif and current.orelse:
            return True, None

    message = rule.get("message") or "if / elif / else を使ってください。"
    return False, message


def validate_require_call_argument_literal(module_node, rule, question_data=None):
    function_name = resolve_rule_value(rule, question_data, "name", "name_key")
    method_name = resolve_rule_value(rule, question_data, "method", "method_key")
    object_name = resolve_rule_value(rule, question_data, "object", "object_key")
    expected_value = resolve_rule_value(rule, question_data, "value", "value_key")
    arg_index = rule.get("arg_index", 0)

    if function_name is None and method_name is None:
        return False, "採点設定エラー: require_call_argument_literal に呼び出し対象が指定されていません。"

    for node in ast.walk(module_node):
        if not isinstance(node, ast.Call):
            continue

        is_target_call = False
        if function_name is not None and get_dotted_name(node.func) == function_name:
            is_target_call = True
        elif (
            method_name is not None
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == method_name
        ):
            if object_name is None or get_dotted_name(node.func.value) == object_name:
                is_target_call = True

        if not is_target_call or arg_index >= len(node.args):
            continue

        argument_node = node.args[arg_index]
        if isinstance(argument_node, ast.Constant) and argument_node.value == expected_value:
            return True, None

    message = rule.get("message") or "指定された引数を使って関数を呼び出してください。"
    return False, message


def validate_require_except_handler_count(module_node, rule, question_data=None):
    min_count = rule.get("min_count")
    exact_count = rule.get("count")

    if min_count is None and exact_count is None:
        return False, "採点設定エラー: require_except_handler_count に count か min_count が必要です。"

    for node in ast.walk(module_node):
        if not isinstance(node, ast.Try):
            continue

        handler_count = len(node.handlers)
        if exact_count is not None and handler_count == exact_count:
            return True, None
        if min_count is not None and handler_count >= min_count:
            return True, None

    message = rule.get("message") or "必要な数の except を書いてください。"
    return False, message


def validate_require_specific_except(module_node, rule, question_data=None):
    expected_names = []

    single_name = resolve_rule_value(rule, question_data, "name", "name_key")
    if isinstance(single_name, str):
        expected_names.append(single_name)

    literal_names = rule.get("names") or []
    for name in literal_names:
        if isinstance(name, str):
            expected_names.append(name)

    generated_values = (question_data or {}).get("generated_values") or {}
    generated_keys = rule.get("name_keys") or []
    for key in generated_keys:
        value = generated_values.get(key)
        if isinstance(value, str):
            expected_names.append(value)

    expected_names = list(dict.fromkeys(expected_names))
    if not expected_names:
        return False, "採点設定エラー: require_specific_except に例外名が指定されていません。"

    found_names = set()
    for node in ast.walk(module_node):
        if not isinstance(node, ast.ExceptHandler) or node.type is None:
            continue
        handler_name = get_dotted_name(node.type)
        if handler_name is not None:
            found_names.add(handler_name)

    missing_names = [name for name in expected_names if name not in found_names]
    if not missing_names:
        return True, None

    message = rule.get("message") or f"except で指定された例外を捕捉してください: {', '.join(missing_names)}"
    return False, message


def validate_require_generated_list_operations(module_node, rule, question_data=None):
    generated_values = (question_data or {}).get("generated_values") or {}
    operations = []

    operation_key = rule.get("operation_key")
    if isinstance(operation_key, str):
        operation = generated_values.get(operation_key)
        if isinstance(operation, str):
            operations.append(operation)

    operations_key = rule.get("operations_key")
    if isinstance(operations_key, str):
        values = generated_values.get(operations_key)
        if isinstance(values, list):
            operations.extend(value for value in values if isinstance(value, str))

    object_name = resolve_rule_value(rule, question_data, "object", "object_key")
    if not operations:
        return False, "採点設定エラー: リスト操作ルールの対象が取得できません。"

    missing_operations = []
    for operation in operations:
        if operation == "append":
            is_valid, _ = validate_require_method_call(module_node, {"method": "append", "object": object_name}, question_data)
            if not is_valid:
                missing_operations.append("append")
        elif operation == "remove":
            is_valid, _ = validate_require_method_call(module_node, {"method": "remove", "object": object_name}, question_data)
            if not is_valid:
                missing_operations.append("remove")
        elif operation == "change":
            if not has_subscript_assignment(module_node, object_name):
                missing_operations.append("change")

    if not missing_operations:
        return True, None

    message = rule.get("message") or f"必要なリスト操作を使ってください: {', '.join(missing_operations)}"
    return False, message


def validate_require_generated_dict_operations(module_node, rule, question_data=None):
    generated_values = (question_data or {}).get("generated_values") or {}
    operations = []

    operation_key = rule.get("operation_key")
    if isinstance(operation_key, str):
        operation = generated_values.get(operation_key)
        if isinstance(operation, str):
            operations.append(operation)

    operations_key = rule.get("operations_key")
    if isinstance(operations_key, str):
        values = generated_values.get(operations_key)
        if isinstance(values, list):
            operations.extend(value for value in values if isinstance(value, str))

    object_name = resolve_rule_value(rule, question_data, "object", "object_key")
    if not operations:
        return False, "採点設定エラー: 辞書操作ルールの対象が取得できません。"

    missing_operations = []
    for operation in operations:
        if operation in {"add", "update"}:
            if not has_subscript_assignment(module_node, object_name):
                missing_operations.append(operation)
        elif operation == "delete":
            if not has_subscript_delete(module_node, object_name):
                missing_operations.append("delete")

    if not missing_operations:
        return True, None

    message = rule.get("message") or f"必要な辞書操作を使ってください: {', '.join(missing_operations)}"
    return False, message


AST_RULE_VALIDATORS = {
    "print_argument_kind": validate_print_argument_kind,
    "require_node_type": validate_require_node_type,
    "require_node": validate_require_node,
    "require_function_call": validate_require_function_call,
    "require_method_call": validate_require_method_call,
    "require_import": validate_require_import,
    "require_function_def": validate_require_function_def,
    "require_try_except": validate_require_try_except,
    "require_finally": validate_require_finally,
    "require_attribute_access": validate_require_attribute_access,
    "require_operator": validate_require_operator,
    "require_if_else": validate_require_if_else,
    "require_if_elif_else": validate_require_if_elif_else,
    "require_call_argument_literal": validate_require_call_argument_literal,
    "require_except_handler_count": validate_require_except_handler_count,
    "require_specific_except": validate_require_specific_except,
    "require_generated_list_operations": validate_require_generated_list_operations,
    "require_generated_dict_operations": validate_require_generated_dict_operations,
    "require_generated_variables_in_print": validate_require_generated_variables_in_print,
    "generated_bindings_at_print": validate_generated_bindings_at_print,
    "generated_bindings_before_print": validate_generated_bindings_before_print,
    "generated_compare_clause": validate_generated_compare_clause,
    "self_update_assignment": validate_self_update_assignment,
    "augassign_update": validate_augassign_update,
}


def validate_ast_rules(question_data, user_code):
    ast_rules = question_data.get("ast_rules") or []
    if not ast_rules:
        return True, None

    try:
        module_node = ast.parse(user_code)
    except SyntaxError as exc:
        return False, f"コードの構文が正しくありません: {exc.msg}"

    for rule in ast_rules:
        rule_type = rule.get("type")
        validator = AST_RULE_VALIDATORS.get(rule_type)
        if validator is None:
            return False, f"未対応の AST ルールです: {rule_type}"

        is_valid, message = validator(module_node, rule, question_data)
        if not is_valid:
            return False, message

    return True, None

#ユーザーの入力の正誤判定を行う関数
def is_correct_by_execution(question_data, user_code):
    ast_is_valid, ast_message = validate_ast_rules(question_data, user_code)
    if not ast_is_valid:
        return False, ast_message, ""

    full_code_parts = []

    if question_data["judge_type"] != "fix_code":
        if question_data["starter_code"]:
            full_code_parts.append(question_data["starter_code"])

    if user_code.strip():
        full_code_parts.append(user_code)

    if question_data["ending_code"]:
        full_code_parts.append(question_data["ending_code"])

    full_code = "\n".join(full_code_parts)

    input_data = question_data.get("input_data")
    success, actual_output, error_message = run_in_sandbox(full_code, input_data=input_data)

    if not success:
        return False, f"コードの実行中にエラーが発生しました: {error_message}", actual_output
    
    expected_output = normalize_output(question_data["expected_output"])

    if normalize_output(actual_output) == expected_output:
        return True, None, actual_output
    else:
        return False, f"出力が期待されるものと異なります。期待: {expected_output} / 実際: {actual_output}", actual_output

#ユーザーの入力の正誤判定をキーワードを含め行う関数   
def is_correct_by_output_and_keyword(question_data, user_code):
    if not contains_required_keywords(user_code, question_data["required_keywords"]):
        return False, "必要なキーワードが含まれていません。", ""

    ast_is_valid, ast_message = validate_ast_rules(question_data, user_code)
    if not ast_is_valid:
        return False, ast_message, ""
    
    full_code_parts = []

    if question_data["judge_type"] != "fix_code":
        if question_data["starter_code"]:
            full_code_parts.append(question_data["starter_code"])
    
    if user_code.strip():
        full_code_parts.append(user_code)
    
    if question_data["ending_code"]:
        full_code_parts.append(question_data["ending_code"])

    full_code = "\n".join(full_code_parts)

    input_data = question_data.get("input_data")
    success, actual_output, error_message = run_in_sandbox(full_code, input_data=input_data)

    if not success:
        return False, f"コードの実行中にエラーが発生しました: {error_message}", actual_output
    
    expected_output = normalize_output(question_data["expected_output"])

    if normalize_output(actual_output) == expected_output:
        return True, None, actual_output
    else:
        return False, f"出力が期待されるものと異なります。期待: {expected_output} / 実際: {actual_output}", actual_output

def is_correct_by_random_output_and_keyword(question_data, user_code):
    if not contains_required_keywords(user_code, question_data["required_keywords"]):
        return False, "必要なキーワードが含まれていません。", ""

    ast_is_valid, ast_message = validate_ast_rules(question_data, user_code)
    if not ast_is_valid:
        return False, ast_message, ""

    full_code_parts = []

    if question_data["starter_code"]:
        full_code_parts.append(question_data["starter_code"])

    if user_code.strip():
        full_code_parts.append(user_code)

    if question_data["ending_code"]:
        full_code_parts.append(question_data["ending_code"])

    full_code = "\n".join(full_code_parts)

    input_data = question_data.get("input_data")
    success, actual_output, error_message = run_in_sandbox(full_code, input_data=input_data)

    if not success:
        return False, f"コードの実行中にエラーが発生しました: {error_message}", actual_output

    normalized_output = normalize_output(actual_output)
    if normalized_output == "":
        return False, "出力が空です。", actual_output

    output_validator = question_data.get("output_validator")
    if output_validator:
        if not validate_output_by_rule(actual_output, output_validator):
            return False, f"出力がバリデーション条件を満たしていません。validator: {output_validator}", actual_output

    return True, None, actual_output


def is_correct_by_output_and_ast(question_data, user_code):
    ast_is_valid, ast_message = validate_ast_rules(question_data, user_code)
    if not ast_is_valid:
        return False, ast_message, ""

    full_code_parts = []

    if question_data["starter_code"]:
        full_code_parts.append(question_data["starter_code"])

    if user_code.strip():
        full_code_parts.append(user_code)

    if question_data["ending_code"]:
        full_code_parts.append(question_data["ending_code"])

    full_code = "\n".join(full_code_parts)

    input_data = question_data.get("input_data")
    success, actual_output, error_message = run_in_sandbox(full_code, input_data=input_data)

    if not success:
        return False, f"コードの実行中にエラーが発生しました: {error_message}", actual_output

    expected_output = normalize_output(question_data["expected_output"])
    if normalize_output(actual_output) == expected_output:
        return True, None, actual_output

    return False, f"出力が期待されるものと異なります。期待: {expected_output} / 実際: {actual_output}", actual_output

#ユーザーの入力の正誤判定をキーワードのみで行う関数
def is_correct_by_keywords_only(question_data, user_code):
    if contains_required_keywords(user_code, question_data["required_keywords"]):
        return True, None, ""
    else:
        return False, "必要なキーワードが含まれていません。", ""
    
#問題ごとに判定方法を切り替える関数
def judge(question_data, user_code):
    judge_type = question_data["judge_type"]

    if judge_type == "output":
        return is_correct_by_execution(question_data, user_code)
    
    elif judge_type == "output_and_keywords":
        return is_correct_by_output_and_keyword(question_data, user_code)

    elif judge_type == "random_output_and_keywords":
        return is_correct_by_random_output_and_keyword(question_data, user_code)

    elif judge_type == "output_and_ast":
        return is_correct_by_output_and_ast(question_data, user_code)
    
    elif judge_type == "fix_code":
        return is_correct_by_execution(question_data, user_code)
    
    elif judge_type == "keyword_only":
        return is_correct_by_keywords_only(question_data, user_code)
    
    else:
        return False, "未判定の判定方式です", ""