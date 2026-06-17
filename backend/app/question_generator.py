import random
import secrets
import math
import time
import datetime
from copy import deepcopy


CALCULATION_OPERATORS = ["+", "-", "*", "/", "//", "%", "**"]


def create_generated_base(data):
    base_id = data["id"]

    data["id"] = f"{base_id}__gen__{secrets.token_hex(4)}"
    data["source_id"] = base_id

    return data


def indent_code_block(code, indent="    "):
    return "\n".join(f"{indent}{line}" if line else indent for line in code.splitlines())


# =====================================
# difficulty1
# =====================================

def generate_print_number(question_data):
    data = deepcopy(question_data)

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 100)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "number": number
    }

    data["question"] = data["template"].format(
        number=number
    )

    data["expected_output"] = str(number)

    data["model_answers"] = [
        f"print({number})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_print_string(question_data):
    data = deepcopy(question_data)

    text = random.choice(
        data["string_candidates"]
    )

    create_generated_base(data)

    data["generated_values"] = {
        "text": text
    }

    data["question"] = data["template"].format(
        text=text
    )

    data["expected_output"] = text

    data["model_answers"] = [
        f'print("{text}")',
        f"print('{text}')"
    ]

    cleanup_generator_fields(data)

    return data


# =====================================
# difficulty2
# =====================================

def calculate_answer(a, b, operator):
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        return a / b
    if operator == "//":
        return a // b
    if operator == "%":
        return a % b
    if operator == "**":
        return a ** b
    raise ValueError(f"Unsupported operator: {operator}")


def pick_calculation_operands(question_data, operator):
    a = random.randint(
        question_data.get("a_min", 1),
        question_data.get("a_max", 10)
    )

    b_min = question_data.get("b_min", 1)
    b_max = question_data.get("b_max", 10)

    if operator in {"/", "//", "%"}:
        b_min = max(1, b_min)

    b = random.randint(b_min, b_max)
    return a, b


def generate_calculation(question_data):
    data = deepcopy(question_data)

    operators = data.get("operator_candidates", CALCULATION_OPERATORS)
    operator = random.choice(operators)
    a, b = pick_calculation_operands(data, operator)
    answer = calculate_answer(a, b, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "a": a,
        "b": b,
        "operator": operator
    }

    data["question"] = data["template"].format(
        a=a,
        b=b,
        operator=operator
    )

    data["expected_output"] = str(answer)
    data["required_keywords"] = ["print", operator]

    data["model_answers"] = [
        f"print({a} {operator} {b})"
    ]

    cleanup_generator_fields(data)

    return data

def generate_addition(question_data):
    calculation_data = deepcopy(question_data)
    calculation_data["operator_candidates"] = ["+"]
    return generate_calculation(calculation_data)


def generate_string_concat(question_data):
    data = deepcopy(question_data)

    left, right = random.choice(
        data["pairs"]
    )

    result = left + right

    create_generated_base(data)

    data["generated_values"] = {
        "left": left,
        "right": right
    }

    data["question"] = data["template"].format(
        left=left,
        right=right
    )

    data["expected_output"] = result

    data["model_answers"] = [
        f'print("{left}" + "{right}")',
        f"print('{left}' + '{right}')"
    ]

    cleanup_generator_fields(data)

    return data


# =====================================
# difficulty3
# =====================================

def generate_mixed_output(question_data):
    data = deepcopy(question_data)

    text = random.choice(
        data["string_candidates"]
    )

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 100)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "text": text,
        "number": number
    }

    data["question"] = data["template"].format(
        text=text,
        number=number
    )

    data["expected_output"] = f"{text} {number}"

    data["model_answers"] = [
        f'print("{text}", {number})',
        f"print('{text}', {number})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_mixed_concat_output(question_data):
    data = deepcopy(question_data)

    left, right = random.choice(
        data["pairs"]
    )

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 100)
    )

    combined_text = f"{left}{right}"

    create_generated_base(data)

    data["generated_values"] = {
        "left": left,
        "right": right,
        "number": number
    }

    data["question"] = data["template"].format(
        left=left,
        right=right,
        number=number
    )

    data["expected_output"] = f"{combined_text} {number}"

    data["model_answers"] = [
        f'print("{left}" + "{right}", {number})',
        f"print('{left}' + '{right}', {number})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_mixed_calculation_output(question_data):
    data = deepcopy(question_data)

    text = random.choice(
        data["string_candidates"]
    )

    operators = data.get("operator_candidates", CALCULATION_OPERATORS)
    operator = random.choice(operators)
    a, b = pick_calculation_operands(data, operator)
    answer = calculate_answer(a, b, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "text": text,
        "a": a,
        "b": b,
        "operator": operator
    }

    data["question"] = data["template"].format(
        text=text,
        a=a,
        b=b,
        operator=operator
    )

    data["expected_output"] = f"{text} {answer}"
    data["required_keywords"] = ["print", operator]

    data["model_answers"] = [
        f'print("{text}", {a} {operator} {b})',
        f"print('{text}', {a} {operator} {b})"
    ]

    cleanup_generator_fields(data)

    return data

# =====================================
# chapter2
# =====================================

def generate_variable_number(question_data):
    data = deepcopy(question_data)

    var_name = random.choice(data["variable_candidates"])

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 100)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": var_name,
        "number": number
    }

    data["question"] = data["template"].format(
        var_name=var_name,
        number=number
    )

    data["expected_output"] = str(number)

    data["required_keywords"] = [
        var_name,
        "print"
    ]

    data["model_answers"] = [
        f"{var_name} = {number}\nprint({var_name})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_variable_string(question_data):
    data = deepcopy(question_data)

    var_name = random.choice(data["variable_candidates"])
    text = random.choice(data["string_candidates"])

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": var_name,
        "text": text
    }

    data["question"] = data["template"].format(
        var_name=var_name,
        text=text
    )

    data["expected_output"] = text

    data["required_keywords"] = [
        var_name,
        "print"
    ]

    data["model_answers"] = [
        f'{var_name} = "{text}"\nprint({var_name})',
        f"{var_name} = '{text}'\nprint({var_name})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_variable_update(question_data):
    data = deepcopy(question_data)

    var_name = random.choice(data["variable_candidates"])
    operator = random.choice(data.get("operator_candidates", ["+", "-", "*"]))

    start = random.randint(
        data.get("start_min", 1),
        data.get("start_max", 50)
    )

    change = random.randint(
        data.get("change_min", 1),
        data.get("change_max", 10)
    )

    answer = calculate_answer(start, change, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": var_name,
        "start": start,
        "change": change,
        "operator": operator
    }

    data["question"] = data["template"].format(
        var_name=var_name,
        start=start,
        change=change,
        operator=operator
    )

    data["expected_output"] = str(answer)

    data["required_keywords"] = [
        var_name,
        "print"
    ]

    data["model_answers"] = [
        f"{var_name} = {start}\n{var_name} = {var_name} {operator} {change}\nprint({var_name})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_variable_short_update(question_data):
    data = deepcopy(question_data)

    var_name = random.choice(data["variable_candidates"])
    operator = random.choice(data.get("operator_candidates", ["+", "-", "*"]))

    start = random.randint(
        data.get("start_min", 1),
        data.get("start_max", 50)
    )

    change = random.randint(
        data.get("change_min", 1),
        data.get("change_max", 10)
    )

    answer = calculate_answer(start, change, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": var_name,
        "start": start,
        "change": change,
        "operator": operator
    }

    data["question"] = data["template"].format(
        var_name=var_name,
        start=start,
        change=change,
        operator=operator
    )

    data["expected_output"] = str(answer)

    data["required_keywords"] = [
        var_name,
        f"{operator}=",
        "print"
    ]

    data["model_answers"] = [
        f"{var_name} = {start}\n{var_name} {operator}= {change}\nprint({var_name})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_two_variable_calculation(question_data):
    data = deepcopy(question_data)

    left_var = random.choice(data["left_variable_candidates"])
    right_var = random.choice(data["right_variable_candidates"])

    operator = random.choice(
        data.get("operator_candidates", CALCULATION_OPERATORS)
    )

    a, b = pick_calculation_operands(data, operator)

    answer = calculate_answer(a, b, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "left_var": left_var,
        "right_var": right_var,
        "a": a,
        "b": b,
        "operator": operator
    }

    data["question"] = data["template"].format(
        left_var=left_var,
        right_var=right_var,
        a=a,
        b=b,
        operator=operator
    )

    data["expected_output"] = str(answer)

    data["required_keywords"] = [
        left_var,
        right_var,
        "print",
        operator
    ]

    data["model_answers"] = [
        f"{left_var} = {a}\n{right_var} = {b}\nprint({left_var} {operator} {right_var})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_three_variable_calculation(question_data):
    data = deepcopy(question_data)

    selected_vars = random.sample(
        data["variable_candidates"],
        3
    )

    var1, var2, var3 = selected_vars

    a = random.randint(
        data.get("a_min", 1),
        data.get("a_max", 20)
    )

    b = random.randint(
        data.get("b_min", 1),
        data.get("b_max", 10)
    )

    c = random.randint(
        data.get("c_min", 1),
        data.get("c_max", 10)
    )

    answer = a + b * c

    create_generated_base(data)

    data["generated_values"] = {
        "var1": var1,
        "var2": var2,
        "var3": var3,
        "a": a,
        "b": b,
        "c": c
    }

    data["question"] = data["template"].format(
        var1=var1,
        var2=var2,
        var3=var3,
        a=a,
        b=b,
        c=c
    )

    data["expected_output"] = str(answer)

    data["required_keywords"] = [
        var1,
        var2,
        var3,
        "print"
    ]

    data["model_answers"] = [
        f"{var1} = {a}\n{var2} = {b}\n{var3} = {c}\nprint({var1} + {var2} * {var3})"
    ]

    cleanup_generator_fields(data)

    return data

# =====================================
# chapter3
# =====================================

COMPARISON_OPERATORS = ["==", "!=", ">", "<", ">=", "<="]


def compare_values(x, y, operator):
    if operator == "==":
        return x == y
    if operator == "!=":
        return x != y
    if operator == ">":
        return x > y
    if operator == "<":
        return x < y
    if operator == ">=":
        return x >= y
    if operator == "<=":
        return x <= y

    raise ValueError(f"Unsupported comparison operator: {operator}")


def pick_true_comparison_values(question_data, operator):
    x_min = question_data.get("x_min", 1)
    x_max = question_data.get("x_max", 50)
    y_min = question_data.get("y_min", 1)
    y_max = question_data.get("y_max", 50)

    if operator == "==":
        value_min = max(x_min, y_min)
        value_max = min(x_max, y_max)
        value = random.randint(value_min, value_max)
        return value, value

    if operator == "!=":
        x = random.randint(x_min, x_max)

        while True:
            y = random.randint(y_min, y_max)
            if x != y:
                return x, y

    if operator == ">":
        y = random.randint(y_min, min(y_max, x_max - 1))
        x = random.randint(max(x_min, y + 1), x_max)
        return x, y

    if operator == "<":
        x = random.randint(x_min, min(x_max, y_max - 1))
        y = random.randint(max(y_min, x + 1), y_max)
        return x, y

    if operator == ">=":
        y = random.randint(y_min, min(y_max, x_max))
        x = random.randint(max(x_min, y), x_max)
        return x, y

    if operator == "<=":
        x = random.randint(x_min, min(x_max, y_max))
        y = random.randint(max(y_min, x), y_max)
        return x, y

    raise ValueError(f"Unsupported comparison operator: {operator}")


def pick_random_comparison_values(question_data):
    x = random.randint(
        question_data.get("x_min", 1),
        question_data.get("x_max", 50)
    )

    y = random.randint(
        question_data.get("y_min", 1),
        question_data.get("y_max", 50)
    )

    return x, y


def generate_if_compare_only(question_data):
    data = deepcopy(question_data)

    operators = data.get("operator_candidates", COMPARISON_OPERATORS)
    operator = random.choice(operators)

    # difficulty1 は必ず条件が True になる値だけ生成する
    x, y = pick_true_comparison_values(data, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "x": x,
        "y": y,
        "operator": operator
    }

    data["question"] = data["template"].format(
        x=x,
        y=y,
        operator=operator
    )

    data["expected_output"] = "OK"

    data["required_keywords"] = [
        "if",
        "x",
        "y",
        "print",
        operator
    ]

    data["model_answers"] = [
        f'x = {x}\ny = {y}\nif x {operator} y:\n    print("OK")',
        f"x = {x}\ny = {y}\nif x {operator} y:\n    print('OK')"
    ]

    cleanup_generator_fields(data)

    return data


def generate_if_else_compare(question_data):
    data = deepcopy(question_data)

    operators = data.get("operator_candidates", COMPARISON_OPERATORS)
    operator = random.choice(operators)

    x, y = pick_random_comparison_values(data)

    is_true = compare_values(x, y, operator)
    expected_output = "OK" if is_true else "NG"

    create_generated_base(data)

    data["generated_values"] = {
        "x": x,
        "y": y,
        "operator": operator
    }

    data["question"] = data["template"].format(
        x=x,
        y=y,
        operator=operator
    )

    data["expected_output"] = expected_output

    data["required_keywords"] = [
        "if",
        "else",
        "x",
        "y",
        "print",
        operator
    ]

    data["model_answers"] = [
        f'x = {x}\ny = {y}\nif x {operator} y:\n    print("OK")\nelse:\n    print("NG")',
        f"x = {x}\ny = {y}\nif x {operator} y:\n    print('OK')\nelse:\n    print('NG')"
    ]

    cleanup_generator_fields(data)

    return data


def generate_if_elif_else_compare(question_data):
    data = deepcopy(question_data)

    operators = data.get("operator_candidates", COMPARISON_OPERATORS)

    operator1 = random.choice(operators)
    operator2 = random.choice([
        operator for operator in operators
        if operator != operator1
    ])

    x, y = pick_random_comparison_values(data)

    if compare_values(x, y, operator1):
        expected_output = "A"
    elif compare_values(x, y, operator2):
        expected_output = "B"
    else:
        expected_output = "C"

    create_generated_base(data)

    data["generated_values"] = {
        "x": x,
        "y": y,
        "operator1": operator1,
        "operator2": operator2
    }

    data["question"] = data["template"].format(
        x=x,
        y=y,
        operator1=operator1,
        operator2=operator2
    )

    data["expected_output"] = expected_output

    data["required_keywords"] = [
        "if",
        "elif",
        "else",
        "x",
        "y",
        "print",
        operator1,
        operator2
    ]

    data["model_answers"] = [
        f'x = {x}\ny = {y}\nif x {operator1} y:\n    print("A")\nelif x {operator2} y:\n    print("B")\nelse:\n    print("C")',
        f"x = {x}\ny = {y}\nif x {operator1} y:\n    print('A')\nelif x {operator2} y:\n    print('B')\nelse:\n    print('C')"
    ]

    cleanup_generator_fields(data)

    return data


def generate_if_compare_value_check(question_data):
    """新難度1：指定値・演算子の厳密判定"""
    data = deepcopy(question_data)

    operators = data.get("operator_candidates", COMPARISON_OPERATORS)
    operator = random.choice(operators)

    x, y = pick_true_comparison_values(data, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "x": x,
        "y": y,
        "operator": operator
    }

    data["question"] = data["template"].format(
        x=x,
        y=y,
        operator=operator
    )

    data["expected_output"] = "OK"

    data["required_keywords"] = [
        "if",
        "x",
        "y",
        "print",
        operator
    ]

    data["model_answers"] = [
        f'x = {x}\ny = {y}\nif x {operator} y:\n    print("OK")',
        f"x = {x}\ny = {y}\nif x {operator} y:\n    print('OK')"
    ]

    cleanup_generator_fields(data)

    return data


def generate_if_else_compare_value_check(question_data):
    """新難度2：if-else + テーマ別（score, string, modulo）"""
    data = deepcopy(question_data)

    theme = data.get("theme", "score")

    if theme == "score":
        border = random.randint(60, 80)
        score = random.randint(0, 100)
        var_name = "score"
        value1 = score
        value2 = border
        operator = ">="
        ok_text = "合格"
        ng_text = "不合格"
        result = ok_text if score >= border else ng_text

    elif theme == "string":
        password = random.choice(["python", "code", "learn"])
        input_password = random.choice(["python", "code", "learn"])
        var_name = "password"
        value1 = input_password
        value2 = password
        operator = "=="
        ok_text = "OK"
        ng_text = "NG"
        result = ok_text if input_password == password else ng_text

    else:  # theme == "modulo"
        number = random.randint(1, 50)
        var_name = "number"
        value1 = number
        operator = "%"
        ok_text = "偶数"
        ng_text = "奇数"
        result = ok_text if number % 2 == 0 else ng_text
        value2 = 2

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": var_name,
        "value1": value1,
        "value2": value2,
        "operator": operator,
        "ok_text": ok_text,
        "ng_text": ng_text,
        "theme": theme
    }

    if theme == "string":
        data["question"] = data["template"].format(
            password=password
        )
        data["model_answers"] = [
            f'{var_name} = "{value1}"\nif {var_name} {operator} "{value2}":\n    print("{ok_text}")\nelse:\n    print("{ng_text}")',
            f"{var_name} = '{value1}'\nif {var_name} {operator} '{value2}':\n    print('{ok_text}')\nelse:\n    print('{ng_text}')"
        ]
    elif theme == "modulo":
        data["question"] = data["template"].format(
            number=number
        )
        data["model_answers"] = [
            f'{var_name} = {value1}\nif {var_name} {operator} {value2} == 0:\n    print("{ok_text}")\nelse:\n    print("{ng_text}")',
            f"{var_name} = {value1}\nif {var_name} {operator} {value2} == 0:\n    print('{ok_text}')\nelse:\n    print('{ng_text}')"
        ]
    else:  # score
        data["question"] = data["template"].format(
            score=score,
            border=border
        )
        data["model_answers"] = [
            f'{var_name} = {value1}\nif {var_name} {operator} {value2}:\n    print("{ok_text}")\nelse:\n    print("{ng_text}")',
            f"{var_name} = {value1}\nif {var_name} {operator} {value2}:\n    print('{ok_text}')\nelse:\n    print('{ng_text}')"
        ]

    data["expected_output"] = result

    data["required_keywords"] = [
        "if",
        "else",
        "print",
        operator
    ]

    if theme == "modulo":
        data["required_keywords"].append("%")

    cleanup_generator_fields(data)

    return data


def generate_if_elif_compare_multiple(question_data):
    """新難度3：if-elif-else + 複数条件による分岐"""
    data = deepcopy(question_data)

    theme = data.get("theme", "score")

    if theme == "score":
        score = random.randint(0, 100)
        var_name = "score"
        value = score

        if score >= 90:
            expected_output = "S"
        elif score >= 70:
            expected_output = "A"
        elif score >= 60:
            expected_output = "B"
        else:
            expected_output = "C"

        data["question"] = data["template"].format(score=score)

        data["model_answers"] = [
            f'{var_name} = {value}\nif {var_name} >= 90:\n    print("S")\nelif {var_name} >= 70:\n    print("A")\nelif {var_name} >= 60:\n    print("B")\nelse:\n    print("C")',
            f"{var_name} = {value}\nif {var_name} >= 90:\n    print('S')\nelif {var_name} >= 70:\n    print('A')\nelif {var_name} >= 60:\n    print('B')\nelse:\n    print('C')"
        ]

    else:  # theme == "range"
        value = random.randint(1, 200)
        var_name = "value"

        if value >= 100:
            expected_output = "large"
        elif value >= 50:
            expected_output = "medium"
        elif value >= 10:
            expected_output = "small"
        else:
            expected_output = "tiny"

        data["question"] = data["template"].format(value=value)

        data["model_answers"] = [
            f'{var_name} = {value}\nif {var_name} >= 100:\n    print("large")\nelif {var_name} >= 50:\n    print("medium")\nelif {var_name} >= 10:\n    print("small")\nelse:\n    print("tiny")',
            f"{var_name} = {value}\nif {var_name} >= 100:\n    print('large')\nelif {var_name} >= 50:\n    print('medium')\nelif {var_name} >= 10:\n    print('small')\nelse:\n    print('tiny')"
        ]

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": var_name,
        "value": value,
        "theme": theme
    }

    data["expected_output"] = expected_output

    data["required_keywords"] = [
        "if",
        "elif",
        "else",
        "print",
        ">="
    ]

    cleanup_generator_fields(data)

    return data


def generate_if_compare_constant(question_data):
    data = deepcopy(question_data)

    variable_name = random.choice(["age", "money", "score", "price", "count", "level"])
    operators = data.get("operator_candidates", COMPARISON_OPERATORS)
    operator = random.choice(operators)

    variable_value, compare_value = pick_true_comparison_values(data, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": variable_name,
        "var_value": variable_value,
        "compare_value": compare_value,
        "operator": operator,
    }

    data["question"] = data["template"].format(
        var_name=variable_name,
        var_value=variable_value,
        compare_value=compare_value,
        operator=operator,
    )

    data["expected_output"] = "OK"
    data["required_keywords"] = [variable_name, "if", "print", operator]
    data["model_answers"] = [
        f'{variable_name} = {variable_value}\nif {variable_name} {operator} {compare_value}:\n    print("OK")',
        f"{variable_name} = {variable_value}\nif {variable_name} {operator} {compare_value}:\n    print('OK')",
    ]

    cleanup_generator_fields(data)
    return data


def generate_if_else_parity(question_data):
    data = deepcopy(question_data)

    variable_name = random.choice(["age", "num", "count", "value", "score"])
    variable_value = random.randint(data.get("value_min", 1), data.get("value_max", 100))

    create_generated_base(data)

    data["generated_values"] = {
        "var_name": variable_name,
        "var_value": variable_value,
        "compare_value": 0,
    }

    data["question"] = data["template"].format(
        var_name=variable_name,
        var_value=variable_value,
    )

    expected_output = "偶数" if variable_value % 2 == 0 else "奇数"
    data["expected_output"] = expected_output
    data["required_keywords"] = [variable_name, "if", "else", "print", "%"]
    data["model_answers"] = [
        f'{variable_name} = {variable_value}\nif {variable_name} % 2 == 0:\n    print("偶数")\nelse:\n    print("奇数")',
        f"{variable_name} = {variable_value}\nif {variable_name} % 2 == 0:\n    print('偶数')\nelse:\n    print('奇数')",
    ]

    cleanup_generator_fields(data)
    return data


def generate_if_elif_else_band(question_data):
    data = deepcopy(question_data)

    score = random.randint(data.get("score_min", 0), data.get("score_max", 100))
    threshold1 = 90
    threshold2 = 70
    threshold3 = 60

    if score >= threshold1:
        expected_output = "S"
    elif score >= threshold2:
        expected_output = "A"
    elif score >= threshold3:
        expected_output = "B"
    else:
        expected_output = "C"

    create_generated_base(data)

    data["generated_values"] = {
        "score": score,
        "threshold1": threshold1,
        "threshold2": threshold2,
        "threshold3": threshold3,
    }

    data["question"] = data["template"].format(
        score=score,
        threshold1=threshold1,
        threshold2=threshold2,
        threshold3=threshold3,
    )

    data["expected_output"] = expected_output
    data["required_keywords"] = ["if", "elif", "else", "print", "score"]
    data["model_answers"] = [
        f'score = {score}\nif score >= {threshold1}:\n    print("S")\nelif score >= {threshold2}:\n    print("A")\nelif score >= {threshold3}:\n    print("B")\nelse:\n    print("C")',
        f"score = {score}\nif score >= {threshold1}:\n    print('S')\nelif score >= {threshold2}:\n    print('A')\nelif score >= {threshold3}:\n    print('B')\nelse:\n    print('C')",
    ]

    cleanup_generator_fields(data)
    return data

# =====================================
# chapter4
# =====================================

def generate_for_range_output(question_data):
    data = deepcopy(question_data)

    start = random.randint(data.get("start_min", 0), data.get("start_max", 10))
    count = random.randint(data.get("count_min", 3), data.get("count_max", 6))
    end = start + count - 1

    create_generated_base(data)

    data["question"] = data["template"].format(start=start, end=end)
    data["expected_output"] = "\n".join(str(i) for i in range(start, end + 1))
    data["model_answers"] = [
        f"for i in range({start}, {end + 1}):\n    print(i)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_for_range_sum(question_data):
    data = deepcopy(question_data)

    start = random.randint(data.get("start_min", 1), data.get("start_max", 5))
    count = random.randint(data.get("count_min", 3), data.get("count_max", 8))
    end = start + count - 1
    total = sum(range(start, end + 1))

    create_generated_base(data)

    data["question"] = data["template"].format(start=start, end=end)
    data["expected_output"] = str(total)
    data["model_answers"] = [
        f"total = 0\nfor i in range({start}, {end + 1}):\n    total += i\nprint(total)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_for_even_sum(question_data):
    data = deepcopy(question_data)

    start = random.randint(data.get("start_min", 1), data.get("start_max", 10))
    count = random.randint(data.get("count_min", 6), data.get("count_max", 12))
    end = start + count - 1
    total = sum(i for i in range(start, end + 1) if i % 2 == 0)

    create_generated_base(data)

    data["question"] = data["template"].format(start=start, end=end)
    data["expected_output"] = str(total)
    data["model_answers"] = [
        f"total = 0\nfor i in range({start}, {end + 1}):\n    if i % 2 == 0:\n        total += i\nprint(total)"
    ]

    cleanup_generator_fields(data)
    return data

# =====================================
# chapter5
# =====================================

def create_number_list(question_data, length):
    start = random.randint(
        question_data.get("number_min", 1),
        question_data.get("number_max", 50)
    )

    return [start + i for i in range(length)]


def generate_list_output(question_data):
    data = deepcopy(question_data)

    length = data.get("list_length", 3)
    values = create_number_list(data, length)

    create_generated_base(data)

    data["generated_values"] = {
        "list_value": values
    }

    data["question"] = data["template"].format(
        list_value=values
    )

    data["expected_output"] = str(values)

    data["model_answers"] = [
        f"print({values})"
    ]

    cleanup_generator_fields(data)

    return data


def apply_list_operation(values, operation):
    result = values[:]
    code_line = ""
    operation_text = ""

    if operation == "append":
        append_value = result[-1] + 1
        result.append(append_value)

        operation_text = f"{append_value} を追加"
        code_line = f"a.append({append_value})"

    elif operation == "change":
        index = random.randint(0, len(result) - 1)
        new_value = result[-1] + 10
        result[index] = new_value

        operation_text = f"index {index} を {new_value} に変更"
        code_line = f"a[{index}] = {new_value}"

    elif operation == "remove":
        remove_value = random.choice(result)
        result.remove(remove_value)

        operation_text = f"{remove_value} を削除"
        code_line = f"a.remove({remove_value})"

    else:
        raise ValueError(f"Unsupported list operation: {operation}")

    return result, operation_text, code_line


def generate_list_single_operation(question_data):
    data = deepcopy(question_data)

    length = data.get("list_length", 4)
    values = create_number_list(data, length)

    operation = random.choice(data["operations"])

    result, operation_text, code_line = apply_list_operation(
        values,
        operation
    )

    create_generated_base(data)

    data["generated_values"] = {
        "list_value": values,
        "operation": operation,
        "operation_text": operation_text
    }

    data["question"] = data["template"].format(
        list_value=values,
        operation_text=operation_text
    )

    data["expected_output"] = str(result)

    data["model_answers"] = [
        f"a = {values}\n{code_line}\nprint(a)"
    ]

    data["required_keywords"] = [
        "print"
    ]

    if operation == "append":
        data["required_keywords"].append("append")
    elif operation == "remove":
        data["required_keywords"].append("remove")

    cleanup_generator_fields(data)

    return data


def generate_list_double_operation(question_data):
    data = deepcopy(question_data)

    length = data.get("list_length", 5)
    values = create_number_list(data, length)

    operations = random.sample(
        data["operations"],
        2
    )

    result1, operation_text1, code_line1 = apply_list_operation(
        values,
        operations[0]
    )

    result2, operation_text2, code_line2 = apply_list_operation(
        result1,
        operations[1]
    )

    create_generated_base(data)

    data["generated_values"] = {
        "list_value": values,
        "operations": operations,
        "operation_text1": operation_text1,
        "operation_text2": operation_text2
    }

    data["question"] = data["template"].format(
        list_value=values,
        operation_text1=operation_text1,
        operation_text2=operation_text2
    )

    data["expected_output"] = str(result2)

    data["model_answers"] = [
        f"a = {values}\n{code_line1}\n{code_line2}\nprint(a)"
    ]

    data["required_keywords"] = [
        "print"
    ]

    for operation in operations:
        if operation == "append":
            data["required_keywords"].append("append")
        elif operation == "remove":
            data["required_keywords"].append("remove")

    cleanup_generator_fields(data)

    return data


# =====================================
# chapter6
# =====================================

def generate_debug_missing_colon(question_data):
    data = deepcopy(question_data)

    end = random.randint(
        data.get("end_min", 1),
        data.get("end_max", 10)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "end": end
    }

    data["question"] = data["template"].format(
        end=end
    )

    data["starter_code"] = f"for i in range({end + 1})\n    print(i)"
    data["expected_output"] = "\n".join(str(i) for i in range(end + 1))

    data["model_answers"] = [
        f"for i in range({end + 1}):\n    print(i)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_missing_quote(question_data):
    data = deepcopy(question_data)

    text = random.choice(data["string_candidates"])

    create_generated_base(data)

    data["generated_values"] = {
        "text": text
    }

    data["question"] = data["template"].format(
        text=text
    )

    data["starter_code"] = f"print({text})"
    data["expected_output"] = text

    data["model_answers"] = [
        f'print("{text}")',
        f"print('{text}')"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_missing_parenthesis(question_data):
    data = deepcopy(question_data)

    a = random.randint(
        data.get("a_min", 1),
        data.get("a_max", 30)
    )

    b = random.randint(
        data.get("b_min", 1),
        data.get("b_max", 30)
    )

    answer = a + b

    create_generated_base(data)

    data["generated_values"] = {
        "a": a,
        "b": b,
        "answer": answer
    }

    data["question"] = data["template"].format(
        answer=answer
    )

    data["starter_code"] = f"print({a} + {b}"
    data["expected_output"] = str(answer)

    data["model_answers"] = [
        f"print({a} + {b})"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_indent_error(question_data):
    data = deepcopy(question_data)

    text = random.choice(data["string_candidates"])

    count = random.randint(
        data.get("count_min", 2),
        data.get("count_max", 5)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "text": text,
        "count": count
    }

    data["question"] = data["template"].format(
        text=text,
        count=count
    )

    data["starter_code"] = f'for i in range({count}):\nprint("{text}")'
    data["expected_output"] = "\n".join([text] * count)

    data["model_answers"] = [
        f'for i in range({count}):\n    print("{text}")',
        f"for i in range({count}):\n    print('{text}')"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_missing_print(question_data):
    data = deepcopy(question_data)

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 100)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "number": number
    }

    data["question"] = data["template"].format(
        number=number
    )

    data["starter_code"] = f"score = {number}\nscore"
    data["expected_output"] = str(number)

    data["model_answers"] = [
        f"score = {number}\nprint(score)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_wrong_variable(question_data):
    data = deepcopy(question_data)

    a = random.randint(
        data.get("a_min", 1),
        data.get("a_max", 50)
    )

    b = random.randint(
        data.get("b_min", 1),
        data.get("b_max", 50)
    )

    answer = a + b

    create_generated_base(data)

    data["generated_values"] = {
        "a": a,
        "b": b,
        "answer": answer
    }

    data["question"] = data["template"].format(
        answer=answer
    )

    data["starter_code"] = f"a = {a}\nb = {b}\nprint(x + b)"
    data["expected_output"] = str(answer)

    data["model_answers"] = [
        f"a = {a}\nb = {b}\nprint(a + b)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_range_end_error(question_data):
    data = deepcopy(question_data)

    start = random.randint(
        data.get("start_min", 0),
        data.get("start_max", 10)
    )

    count = random.randint(
        data.get("count_min", 3),
        data.get("count_max", 6)
    )

    end = start + count - 1

    create_generated_base(data)

    data["generated_values"] = {
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        start=start,
        end=end
    )

    data["starter_code"] = f"for i in range({start}, {end}):\n    print(i)"
    data["expected_output"] = "\n".join(str(i) for i in range(start, end + 1))

    data["model_answers"] = [
        f"for i in range({start}, {end + 1}):\n    print(i)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_compare_operator_error(question_data):
    data = deepcopy(question_data)

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 50)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "number": number
    }

    data["question"] = data["template"].format(
        number=number
    )

    data["starter_code"] = f'x = {number}\nif x = {number}:\n    print("OK")'
    data["expected_output"] = "OK"

    data["model_answers"] = [
        f'x = {number}\nif x == {number}:\n    print("OK")',
        f"x = {number}\nif x == {number}:\n    print('OK')"
    ]

    cleanup_generator_fields(data)
    return data


def generate_debug_logic_condition_error(question_data):
    data = deepcopy(question_data)

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 50)
    )

    x = number + random.randint(1, 10)

    create_generated_base(data)

    data["generated_values"] = {
        "number": number,
        "x": x
    }

    data["question"] = data["template"].format(
        number=number
    )

    data["starter_code"] = f'x = {x}\nif x < {number}:\n    print("OK")'
    data["expected_output"] = "OK"

    data["model_answers"] = [
        f'x = {x}\nif x > {number}:\n    print("OK")',
        f"x = {x}\nif x > {number}:\n    print('OK')"
    ]

    cleanup_generator_fields(data)
    return data

# =====================================
# chapter7
# =====================================

def generate_input_greeting(question_data):
    data = deepcopy(question_data)

    greeting = random.choice(
        data["greeting_candidates"]
    )

    create_generated_base(data)

    data["generated_values"] = {
        "greeting": greeting
    }

    data["question"] = data["template"].format(
        greeting=greeting
    )

    data["input_data"] = "太郎"
    data["expected_output"] = f"{greeting} 太郎"

    data["model_answers"] = [
        f'name = input()\nprint("{greeting}", name)',
        f"name = input()\nprint('{greeting}', name)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_input_str(question_data):
    data = deepcopy(question_data)

    create_generated_base(data)

    data["question"] = data["template"]

    data["input_data"] = "Python"
    data["expected_output"] = "Python"

    data["model_answers"] = [
        "text = input()\nprint(text)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_input_int(question_data):
    data = deepcopy(question_data)

    create_generated_base(data)

    number = random.randint(
        data.get("input_min", 1),
        data.get("input_max", 100)
    )

    data["generated_values"] = {
        "number": number
    }

    data["question"] = data["template"]

    data["input_data"] = str(number)
    data["expected_output"] = str(number)

    data["model_answers"] = [
        "number = int(input())\nprint(number)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_input_prompt(question_data):
    data = deepcopy(question_data)

    prompt = random.choice(
        data["prompt_candidates"]
    )

    create_generated_base(data)

    data["generated_values"] = {
        "prompt": prompt
    }

    data["question"] = data["template"].format(
        prompt=prompt
    )

    data["input_data"] = "太郎"
    data["expected_output"] = "太郎"

    data["model_answers"] = [
        f'name = input("{prompt}")\nprint(name)',
        f"name = input('{prompt}')\nprint(name)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_input_add(question_data):
    data = deepcopy(question_data)

    add_value = random.randint(
        data.get("add_min", 1),
        data.get("add_max", 20)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "add_value": add_value
    }

    data["question"] = data["template"].format(
        add_value=add_value
    )

    sample_input = 10
    data["input_data"] = str(sample_input)
    answer = sample_input + add_value

    data["expected_output"] = str(answer)

    data["model_answers"] = [
        f"x = int(input())\nprint(x + {add_value})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_input_multiply(question_data):
    data = deepcopy(question_data)

    create_generated_base(data)

    sample_a = 5
    sample_b = 4

    answer = sample_a * sample_b

    data["question"] = data["template"]

    data["input_data"] = f"{sample_a}\n{sample_b}"
    data["expected_output"] = str(answer)

    data["model_answers"] = [
        "a = int(input())\nb = int(input())\nprint(a * b)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_input_sum_until_n(question_data):
    data = deepcopy(question_data)

    n = random.randint(
        data.get("n_min", 3),
        data.get("n_max", 20)
    )

    answer = sum(range(1, n + 1))

    create_generated_base(data)

    data["generated_values"] = {
        "n": n
    }

    data["question"] = data["template"]

    data["input_data"] = str(n)
    data["expected_output"] = str(answer)

    data["model_answers"] = [
        "n = int(input())\n\ntotal = 0\n\nfor i in range(1, n + 1):\n    total += i\n\nprint(total)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_input_product_until_n(question_data):
    data = deepcopy(question_data)

    n = random.randint(
        data.get("n_min", 3),
        data.get("n_max", 10)
    )

    answer = 1

    for i in range(1, n + 1):
        answer *= i

    create_generated_base(data)

    data["generated_values"] = {
        "n": n
    }

    data["question"] = data["template"]

    data["input_data"] = str(n)
    data["expected_output"] = str(answer)

    data["model_answers"] = [
        "n = int(input())\n\ntotal = 1\n\nfor i in range(1, n + 1):\n    total *= i\n\nprint(total)"
    ]

    cleanup_generator_fields(data)

    return data

# =====================================
# chapter8
# =====================================

def generate_function_print(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(
        data["function_name_candidates"]
    )

    text = random.choice(
        data["text_candidates"]
    )

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "text": text
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        text=text
    )

    data["expected_output"] = text

    data["model_answers"] = [
        f'def {function_name}():\n    print("{text}")\n\n{function_name}()',
        f"def {function_name}():\n    print('{text}')\n\n{function_name}()"
    ]

    cleanup_generator_fields(data)

    return data


def generate_function_return_calculation(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(
        data["function_name_candidates"]
    )

    operator = random.choice(
        data["operator_candidates"]
    )

    a = random.randint(
        data.get("a_min", 1),
        data.get("a_max", 30)
    )

    b = random.randint(
        data.get("b_min", 1),
        data.get("b_max", 20)
    )

    answer = calculate_answer(a, b, operator)

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "operator": operator,
        "a": a,
        "b": b
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        operator=operator,
        a=a,
        b=b
    )

    data["expected_output"] = str(answer)

    data["model_answers"] = [
        f"def {function_name}(a, b):\n    return a {operator} b\n\nprint({function_name}({a}, {b}))"
    ]

    cleanup_generator_fields(data)

    return data


def generate_function_if_return(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(
        data["function_name_candidates"]
    )

    border = random.randint(
        data.get("border_min", 50),
        data.get("border_max", 80)
    )

    score = random.randint(
        data.get("score_min", 0),
        data.get("score_max", 100)
    )

    result = "Pass" if score >= border else "Fail"

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "border": border,
        "score": score
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        border=border,
        score=score
    )

    data["expected_output"] = result

    data["model_answers"] = [
        f'def {function_name}(score):\n    if score >= {border}:\n        return "Pass"\n    else:\n        return "Fail"\n\nprint({function_name}({score}))',
        f"def {function_name}(score):\n    if score >= {border}:\n        return 'Pass'\n    else:\n        return 'Fail'\n\nprint({function_name}({score}))"
    ]

    cleanup_generator_fields(data)

    return data


def generate_function_for_print(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(
        data["function_name_candidates"]
    )

    start = random.randint(
        data.get("start_min", 1),
        data.get("start_max", 5)
    )

    count = random.randint(
        data.get("count_min", 3),
        data.get("count_max", 6)
    )

    end = start + count - 1

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        start=start,
        end=end
    )

    data["expected_output"] = "\n".join(
        str(i) for i in range(start, end + 1)
    )

    data["model_answers"] = [
        f"def {function_name}():\n    for i in range({start}, {end + 1}):\n        print(i)\n\n{function_name}()"
    ]

    cleanup_generator_fields(data)

    return data


def generate_function_sum_return(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(
        data["function_name_candidates"]
    )

    end = random.randint(
        data.get("end_min", 3),
        data.get("end_max", 10)
    )

    answer = sum(range(1, end + 1))

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "end": end
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        end=end
    )

    data["expected_output"] = str(answer)

    data["model_answers"] = [
        f"def {function_name}():\n    total = 0\n\n    for i in range(1, {end + 1}):\n        total += i\n\n    return total\n\nprint({function_name}())"
    ]

    cleanup_generator_fields(data)

    return data


def generate_function_string_return(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(
        data["function_name_candidates"]
    )

    greeting = random.choice(
        data["greeting_candidates"]
    )

    name = random.choice(
        data["name_candidates"]
    )

    result = f"{greeting} {name}"

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "greeting": greeting,
        "name": name
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        greeting=greeting,
        name=name
    )

    data["expected_output"] = result

    data["model_answers"] = [
        f'def {function_name}(name):\n    return "{greeting} " + name\n\nprint({function_name}("{name}"))',
        f"def {function_name}(name):\n    return '{greeting} ' + name\n\nprint({function_name}('{name}'))"
    ]

    cleanup_generator_fields(data)

    return data


def generate_function_even_odd(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(
        data["function_name_candidates"]
    )

    number = random.randint(
        data.get("number_min", 1),
        data.get("number_max", 50)
    )

    result = "Even" if number % 2 == 0 else "Odd"

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "number": number
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        number=number
    )

    data["expected_output"] = result

    data["model_answers"] = [
        f'def {function_name}(number):\n    if number % 2 == 0:\n        return "Even"\n    else:\n        return "Odd"\n\nprint({function_name}({number}))',
        f"def {function_name}(number):\n    if number % 2 == 0:\n        return 'Even'\n    else:\n        return 'Odd'\n\nprint({function_name}({number}))"
    ]

    cleanup_generator_fields(data)

    return data

# =====================================
# chapter9
# =====================================

def generate_string_upper(question_data):
    data = deepcopy(question_data)

    text = random.choice(data["text_candidates"])
    result = text.upper()

    create_generated_base(data)

    data["generated_values"] = {"text": text}

    data["question"] = data["template"].format(text=text)
    data["expected_output"] = result
    data["model_answers"] = [
        f'text = "{text}"\nprint(text.upper())',
        f"text = '{text}'\nprint(text.upper())"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_lower(question_data):
    data = deepcopy(question_data)

    text = random.choice(data["text_candidates"])
    result = text.lower()

    create_generated_base(data)

    data["generated_values"] = {"text": text}

    data["question"] = data["template"].format(text=text)
    data["expected_output"] = result
    data["model_answers"] = [
        f'text = "{text}"\nprint(text.lower())',
        f"text = '{text}'\nprint(text.lower())"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_len(question_data):
    data = deepcopy(question_data)

    text = random.choice(data["text_candidates"])
    result = len(text)

    create_generated_base(data)

    data["generated_values"] = {"text": text}

    data["question"] = data["template"].format(text=text)
    data["expected_output"] = str(result)
    data["model_answers"] = [
        f'text = "{text}"\nprint(len(text))',
        f"text = '{text}'\nprint(len(text))"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_replace(question_data):
    data = deepcopy(question_data)

    text, old, new = random.choice(data["replace_pairs"])
    result = text.replace(old, new)

    create_generated_base(data)

    data["generated_values"] = {
        "text": text,
        "old": old,
        "new": new
    }

    data["question"] = data["template"].format(
        text=text,
        old=old,
        new=new
    )

    data["expected_output"] = result
    data["model_answers"] = [
        f'text = "{text}"\nprint(text.replace("{old}", "{new}"))',
        f"text = '{text}'\nprint(text.replace('{old}', '{new}'))"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_concat_basic(question_data):
    data = deepcopy(question_data)

    left, right = random.choice(data["concat_pairs"])
    result = left + right

    create_generated_base(data)

    data["generated_values"] = {
        "left": left,
        "right": right
    }

    data["question"] = data["template"].format(
        left=left,
        right=right
    )

    data["expected_output"] = result
    data["model_answers"] = [
        f'left = "{left}"\nright = "{right}"\nprint(left + right)',
        f"left = '{left}'\nright = '{right}'\nprint(left + right)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_split(question_data):
    data = deepcopy(question_data)

    text, separator = random.choice(data["split_patterns"])
    result = text.split(separator)

    create_generated_base(data)

    data["generated_values"] = {
        "text": text,
        "separator": separator
    }

    data["question"] = data["template"].format(
        text=text,
        separator=separator
    )

    data["expected_output"] = str(result)
    data["model_answers"] = [
        f'text = "{text}"\nprint(text.split("{separator}"))',
        f"text = '{text}'\nprint(text.split('{separator}'))"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_strip(question_data):
    data = deepcopy(question_data)

    text = random.choice(data["text_candidates"])
    result = text.strip()

    create_generated_base(data)

    data["generated_values"] = {"text": text}

    data["question"] = data["template"].format(text=text)
    data["expected_output"] = result
    data["model_answers"] = [
        f'text = "{text}"\nprint(text.strip())',
        f"text = '{text}'\nprint(text.strip())"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_replace_upper(question_data):
    data = deepcopy(question_data)

    text, old, new = random.choice(data["replace_pairs"])
    result = text.replace(old, new).upper()

    create_generated_base(data)

    data["generated_values"] = {
        "text": text,
        "old": old,
        "new": new
    }

    data["question"] = data["template"].format(
        text=text,
        old=old,
        new=new
    )

    data["expected_output"] = result
    data["model_answers"] = [
        f'text = "{text}"\nprint(text.replace("{old}", "{new}").upper())',
        f"text = '{text}'\nprint(text.replace('{old}', '{new}').upper())"
    ]

    cleanup_generator_fields(data)
    return data


def generate_string_concat_len(question_data):
    data = deepcopy(question_data)

    left, right = random.choice(data["concat_pairs"])
    result = len(left + right)

    create_generated_base(data)

    data["generated_values"] = {
        "left": left,
        "right": right
    }

    data["question"] = data["template"].format(
        left=left,
        right=right
    )

    data["expected_output"] = str(result)
    data["model_answers"] = [
        f'left = "{left}"\nright = "{right}"\ntext = left + right\nprint(len(text))',
        f"left = '{left}'\nright = '{right}'\ntext = left + right\nprint(len(text))"
    ]

    cleanup_generator_fields(data)
    return data

# =====================================
# chapter10
# =====================================

def build_dict_string(pairs):
    items = []

    for key, value in pairs:
        if isinstance(value, str):
            items.append(f'"{key}": "{value}"')
        else:
            items.append(f'"{key}": {value}')

    return "{ " + ", ".join(items) + " }"


def generate_dict_create_one(question_data):
    data = deepcopy(question_data)

    dict_name = random.choice(
        data["dict_name_candidates"]
    )

    key, value = random.choice(
        data["key_value_pairs"]
    )

    dict_pairs = [(key, value)]

    dict_string = build_dict_string(dict_pairs)

    create_generated_base(data)

    data["generated_values"] = {
        "dict_name": dict_name,
        "key": key,
        "value": value
    }

    data["question"] = data["template"].format(
        dict_name=dict_name,
        key1=key,
        value1=value
    )

    data["expected_output"] = str(eval(dict_string))

    if isinstance(value, str):
        value_code = f'"{value}"'
    else:
        value_code = str(value)

    data["model_answers"] = [
        f'{dict_name} = {{"{key}": {value_code}}}\nprint({dict_name})'
    ]

    cleanup_generator_fields(data)

    return data


def generate_dict_create_two(question_data):
    data = deepcopy(question_data)

    dict_name = random.choice(
        data["dict_name_candidates"]
    )

    key1, value1, key2, value2 = random.choice(
        data["dict_patterns"]
    )

    dict_pairs = [
        (key1, value1),
        (key2, value2)
    ]

    dict_string = build_dict_string(dict_pairs)

    create_generated_base(data)

    data["generated_values"] = {
        "dict_name": dict_name,
        "key1": key1,
        "value1": value1,
        "key2": key2,
        "value2": value2
    }

    data["question"] = data["template"].format(
        dict_name=dict_name,
        key1=key1,
        value1=value1,
        key2=key2,
        value2=value2
    )

    data["expected_output"] = str(eval(dict_string))

    value1_code = f'"{value1}"' if isinstance(value1, str) else value1
    value2_code = f'"{value2}"' if isinstance(value2, str) else value2

    data["model_answers"] = [
        f'{dict_name} = {{"{key1}": {value1_code}, "{key2}": {value2_code}}}\nprint({dict_name})'
    ]

    cleanup_generator_fields(data)

    return data


def generate_dict_single_operation(question_data):
    data = deepcopy(question_data)

    dict_name = random.choice(
        data["dict_name_candidates"]
    )

    key1, value1, key2, value2 = random.choice(
        data["dict_patterns"]
    )

    operation = random.choice(
        data["operation_candidates"]
    )

    base_dict = {
        key1: value1,
        key2: value2
    }

    code_lines = []

    if operation == "add":
        add_key, add_value = random.choice(
            data["add_candidates"]
        )

        base_dict[add_key] = add_value

        operation_text = f'{add_key} に「{add_value}」を追加'

        add_value_code = (
            f'"{add_value}"'
            if isinstance(add_value, str)
            else add_value
        )

        code_lines.append(
            f'{dict_name}["{add_key}"] = {add_value_code}'
        )

    elif operation == "update":
        target_key = random.choice([key1, key2])

        if isinstance(base_dict[target_key], str):
            new_value = random.choice(
                data["string_update_candidates"]
            )

            value_code = f'"{new_value}"'

        else:
            new_value = random.choice(
                data["number_update_candidates"]
            )

            value_code = str(new_value)

        base_dict[target_key] = new_value

        operation_text = f'{target_key} を「{new_value}」に変更'

        code_lines.append(
            f'{dict_name}["{target_key}"] = {value_code}'
        )

    else:
        target_key = random.choice([key1, key2])

        del base_dict[target_key]

        operation_text = f'{target_key} を削除'

        code_lines.append(
            f'del {dict_name}["{target_key}"]'
        )

    create_generated_base(data)

    data["generated_values"] = {
        "dict_name": dict_name,
        "operation": operation,
    }

    dict_string = build_dict_string([
        (key1, value1),
        (key2, value2)
    ])

    data["question"] = data["template"].format(
        dict_name=dict_name,
        dict_value=dict_string,
        operation_text=operation_text
    )

    data["expected_output"] = str(base_dict)

    value1_code = f'"{value1}"' if isinstance(value1, str) else value1
    value2_code = f'"{value2}"' if isinstance(value2, str) else value2

    starter = (
        f'{dict_name} = '
        f'{{"{key1}": {value1_code}, "{key2}": {value2_code}}}'
    )

    data["model_answers"] = [
        starter + "\n" +
        "\n".join(code_lines) +
        f"\nprint({dict_name})"
    ]

    cleanup_generator_fields(data)

    return data


def generate_dict_double_operation(question_data):
    data = deepcopy(question_data)

    dict_name = random.choice(
        data["dict_name_candidates"]
    )

    key1, value1, key2, value2 = random.choice(
        data["dict_patterns"]
    )

    operations = random.sample(
        data["operation_candidates"],
        2
    )

    result_dict = {
        key1: value1,
        key2: value2
    }

    operation_texts = []
    code_lines = []

    for operation in operations:

        if operation == "add":
            add_key, add_value = random.choice(
                data["add_candidates"]
            )

            result_dict[add_key] = add_value

            operation_texts.append(
                f'{add_key} に「{add_value}」を追加'
            )

            add_value_code = (
                f'"{add_value}"'
                if isinstance(add_value, str)
                else add_value
            )

            code_lines.append(
                f'{dict_name}["{add_key}"] = {add_value_code}'
            )

        elif operation == "update":

            available_keys = list(result_dict.keys())
            target_key = random.choice(available_keys)

            if isinstance(result_dict[target_key], str):
                new_value = random.choice(
                    data["string_update_candidates"]
                )

                value_code = f'"{new_value}"'

            else:
                new_value = random.choice(
                    data["number_update_candidates"]
                )

                value_code = str(new_value)

            result_dict[target_key] = new_value

            operation_texts.append(
                f'{target_key} を「{new_value}」に変更'
            )

            code_lines.append(
                f'{dict_name}["{target_key}"] = {value_code}'
            )

        elif operation == "delete":

            available_keys = list(result_dict.keys())
            target_key = random.choice(available_keys)

            del result_dict[target_key]

            operation_texts.append(
                f'{target_key} を削除'
            )

            code_lines.append(
                f'del {dict_name}["{target_key}"]'
            )

    create_generated_base(data)

    data["generated_values"] = {
        "dict_name": dict_name,
        "operations": operations,
    }

    dict_string = build_dict_string([
        (key1, value1),
        (key2, value2)
    ])

    data["question"] = data["template"].format(
        dict_name=dict_name,
        dict_value=dict_string,
        operation_text1=operation_texts[0],
        operation_text2=operation_texts[1]
    )

    data["expected_output"] = str(result_dict)

    value1_code = f'"{value1}"' if isinstance(value1, str) else value1
    value2_code = f'"{value2}"' if isinstance(value2, str) else value2

    starter = (
        f'{dict_name} = '
        f'{{"{key1}": {value1_code}, "{key2}": {value2_code}}}'
    )

    data["model_answers"] = [
        starter + "\n" +
        "\n".join(code_lines) +
        f"\nprint({dict_name})"
    ]

    cleanup_generator_fields(data)

    return data

# =====================================
# chapter11
# =====================================

def generate_while_range_output(question_data):
    data = deepcopy(question_data)

    start = random.randint(
        data.get("start_min", 0),
        data.get("start_max", 10)
    )

    count = random.randint(
        data.get("count_min", 3),
        data.get("count_max", 6)
    )

    end = start + count - 1

    create_generated_base(data)

    data["generated_values"] = {
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        start=start,
        end=end
    )

    data["expected_output"] = "\n".join(
        str(i) for i in range(start, end + 1)
    )

    data["model_answers"] = [
        f"i = {start}\n\nwhile i <= {end}:\n    print(i)\n    i += 1"
    ]

    cleanup_generator_fields(data)

    return data


def generate_while_sum(question_data):
    data = deepcopy(question_data)

    start = random.randint(
        data.get("start_min", 1),
        data.get("start_max", 5)
    )

    count = random.randint(
        data.get("count_min", 4),
        data.get("count_max", 8)
    )

    end = start + count - 1

    answer = sum(range(start, end + 1))

    create_generated_base(data)

    data["generated_values"] = {
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        start=start,
        end=end
    )

    data["expected_output"] = str(answer)

    data["model_answers"] = [
        f"i = {start}\ntotal = 0\n\nwhile i <= {end}:\n    total += i\n    i += 1\n\nprint(total)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_while_repeat_string(question_data):
    data = deepcopy(question_data)

    text = random.choice(
        data["text_candidates"]
    )

    count = random.randint(
        data.get("count_min", 3),
        data.get("count_max", 6)
    )

    create_generated_base(data)

    data["generated_values"] = {
        "text": text,
        "count": count
    }

    data["question"] = data["template"].format(
        text=text,
        count=count
    )

    data["expected_output"] = "\n".join(
        [text] * count
    )

    data["model_answers"] = [
        f'i = 0\n\nwhile i < {count}:\n    print("{text}")\n    i += 1',
        f"i = 0\n\nwhile i < {count}:\n    print('{text}')\n    i += 1"
    ]

    cleanup_generator_fields(data)

    return data


def generate_while_multiply(question_data):
    data = deepcopy(question_data)

    start = random.randint(
        data.get("start_min", 1),
        data.get("start_max", 3)
    )

    count = random.randint(
        data.get("count_min", 3),
        data.get("count_max", 5)
    )

    end = start + count - 1

    answer = 1

    for i in range(start, end + 1):
        answer *= i

    create_generated_base(data)

    data["generated_values"] = {
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        start=start,
        end=end
    )

    data["expected_output"] = str(answer)

    data["model_answers"] = [
        f"i = {start}\ntotal = 1\n\nwhile i <= {end}:\n    total *= i\n    i += 1\n\nprint(total)"
    ]

    cleanup_generator_fields(data)

    return data


def generate_while_even_output(question_data):
    data = deepcopy(question_data)

    start = random.randint(
        data.get("start_min", 1),
        data.get("start_max", 10)
    )

    count = random.randint(
        data.get("count_min", 6),
        data.get("count_max", 12)
    )

    end = start + count - 1

    outputs = []

    for i in range(start, end + 1):
        if i % 2 == 0:
            outputs.append(str(i))

    create_generated_base(data)

    data["generated_values"] = {
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        start=start,
        end=end
    )

    data["expected_output"] = "\n".join(outputs)

    data["model_answers"] = [
        f"i = {start}\n\nwhile i <= {end}:\n    if i % 2 == 0:\n        print(i)\n\n    i += 1"
    ]

    cleanup_generator_fields(data)

    return data


def generate_while_odd_output(question_data):
    data = deepcopy(question_data)

    start = random.randint(
        data.get("start_min", 1),
        data.get("start_max", 10)
    )

    count = random.randint(
        data.get("count_min", 6),
        data.get("count_max", 12)
    )

    end = start + count - 1

    outputs = []

    for i in range(start, end + 1):
        if i % 2 != 0:
            outputs.append(str(i))

    create_generated_base(data)

    data["generated_values"] = {
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        start=start,
        end=end
    )

    data["expected_output"] = "\n".join(outputs)

    data["model_answers"] = [
        f"i = {start}\n\nwhile i <= {end}:\n    if i % 2 != 0:\n        print(i)\n\n    i += 1"
    ]

    cleanup_generator_fields(data)

    return data


def generate_while_countdown(question_data):
    data = deepcopy(question_data)

    start = random.randint(
        data.get("start_min", 5),
        data.get("start_max", 15)
    )

    count = random.randint(
        data.get("count_min", 3),
        data.get("count_max", 6)
    )

    end = start - count + 1

    create_generated_base(data)

    data["generated_values"] = {
        "start": start,
        "end": end
    }

    data["question"] = data["template"].format(
        start=start,
        end=end
    )

    data["expected_output"] = "\n".join(
        str(i) for i in range(start, end - 1, -1)
    )

    data["model_answers"] = [
        f"i = {start}\n\nwhile i >= {end}:\n    print(i)\n    i -= 1"
    ]

    cleanup_generator_fields(data)

    return data

# =====================================
# chapter12
# =====================================

def generate_math_sqrt(question_data):
    data = deepcopy(question_data)

    root = random.randint(data.get("root_min", 2), data.get("root_max", 20))
    number = root ** 2

    create_generated_base(data)

    data["generated_values"] = {"number": number}
    data["question"] = data["template"].format(number=number)
    data["expected_output"] = str(math.sqrt(number))
    data["model_answers"] = [
        f"import math\nprint(math.sqrt({number}))"
    ]

    cleanup_generator_fields(data)
    return data


def generate_math_pi(question_data):
    data = deepcopy(question_data)

    create_generated_base(data)

    data["question"] = data["template"]
    data["expected_output"] = str(math.pi)
    data["model_answers"] = [
        "import math\nprint(math.pi)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_math_floor_ceil(question_data):
    data = deepcopy(question_data)

    function_name = random.choice(data["function_candidates"])
    number = random.choice(data["number_candidates"])

    if function_name == "floor":
        answer = math.floor(number)
    else:
        answer = math.ceil(number)

    create_generated_base(data)

    data["generated_values"] = {
        "function_name": function_name,
        "number": number
    }

    data["question"] = data["template"].format(
        function_name=function_name,
        number=number
    )

    data["expected_output"] = str(answer)
    data["required_keywords"] = ["import", "math", function_name, "print"]
    data["model_answers"] = [
        f"import math\nprint(math.{function_name}({number}))"
    ]

    cleanup_generator_fields(data)
    return data


def generate_random_randint(question_data):
    data = deepcopy(question_data)

    min_value = random.choice(data["min_candidates"])
    max_value = random.choice(data["max_candidates"])

    if min_value >= max_value:
        max_value = min_value + 10

    create_generated_base(data)

    data["generated_values"] = {
        "min_value": min_value,
        "max_value": max_value
    }

    data["question"] = data["template"].format(
        min_value=min_value,
        max_value=max_value
    )

    data["expected_output"] = ""
    data["output_validator"] = f"int_range_{min_value}_{max_value}_lines1"
    data["model_answers"] = [
        f"import random\nprint(random.randint({min_value}, {max_value}))"
    ]

    cleanup_generator_fields(data)
    return data


def generate_random_shuffle(question_data):
    data = deepcopy(question_data)

    list_value = random.choice(data["list_candidates"])

    create_generated_base(data)

    data["generated_values"] = {
        "list_value": list_value
    }

    data["question"] = data["template"].format(
        list_value=list_value
    )

    data["expected_output"] = ""
    data["model_answers"] = [
        f"import random\nitems = {list_value}\nrandom.shuffle(items)\nprint(items)"
    ]

    cleanup_generator_fields(data)
    return data


def generate_time_sleep(question_data):
    data = deepcopy(question_data)

    before_text = random.choice(data["before_candidates"])
    after_text = random.choice(data["after_candidates"])
    second = random.choice(data["second_candidates"])

    create_generated_base(data)

    data["generated_values"] = {
        "before_text": before_text,
        "after_text": after_text,
        "second": second
    }

    data["question"] = data["template"].format(
        before_text=before_text,
        after_text=after_text,
        second=second
    )

    data["expected_output"] = f"{before_text}\n{after_text}"
    data["model_answers"] = [
        f'import time\nprint("{before_text}")\ntime.sleep({second})\nprint("{after_text}")',
        f"import time\nprint('{before_text}')\ntime.sleep({second})\nprint('{after_text}')"
    ]

    cleanup_generator_fields(data)
    return data


def generate_time_time(question_data):
    data = deepcopy(question_data)

    create_generated_base(data)

    data["question"] = data["template"]
    data["expected_output"] = ""
    data["model_answers"] = [
        "import time\nprint(time.time())"
    ]

    cleanup_generator_fields(data)
    return data


def generate_datetime_today(question_data):
    data = deepcopy(question_data)

    create_generated_base(data)

    data["question"] = data["template"]
    data["expected_output"] = str(datetime.date.today())
    data["model_answers"] = [
        "from datetime import date\nprint(date.today())"
    ]

    cleanup_generator_fields(data)
    return data


def generate_datetime_now(question_data):
    data = deepcopy(question_data)

    create_generated_base(data)

    data["question"] = data["template"]
    data["expected_output"] = ""
    data["model_answers"] = [
        "import datetime\nprint(datetime.datetime.now())"
    ]

    cleanup_generator_fields(data)
    return data

# =====================================
# chapter13
# =====================================

def generate_try_except_basic(question_data):
    data = deepcopy(question_data)

    error_name, error_code, error_text = random.choice(data["error_patterns"])

    create_generated_base(data)

    data["generated_values"] = {
        "error_name": error_name,
        "error_code": error_code,
        "error_text": error_text
    }

    data["question"] = data["template"].format(
        error_name=error_name,
        error_text=error_text
    )

    data["expected_output"] = error_text

    if error_name in ["SyntaxError", "IndentationError"]:
        code_line = indent_code_block(f'exec({repr(error_code)})')
    else:
        code_line = indent_code_block(error_code)

    data["model_answers"] = [
        f'try:\n{code_line}\nexcept:\n    print("{error_text}")',
        f"try:\n{code_line}\nexcept:\n    print('{error_text}')"
    ]

    cleanup_generator_fields(data)
    return data


def generate_specific_error(question_data):
    data = deepcopy(question_data)

    error_name, error_code, error_text = random.choice(data["error_patterns"])

    create_generated_base(data)

    data["generated_values"] = {
        "error_name": error_name,
        "error_code": error_code,
        "error_text": error_text
    }

    data["question"] = data["template"].format(
        error_name=error_name,
        error_text=error_text
    )

    data["expected_output"] = error_text
    data["required_keywords"] = ["try", "except", error_name, "print"]

    if error_name in ["SyntaxError", "IndentationError"]:
        code_line = indent_code_block(f'exec({repr(error_code)})')
    else:
        code_line = indent_code_block(error_code)

    data["model_answers"] = [
        f'try:\n{code_line}\nexcept {error_name}:\n    print("{error_text}")',
        f"try:\n{code_line}\nexcept {error_name}:\n    print('{error_text}')"
    ]

    cleanup_generator_fields(data)
    return data


def generate_try_except_finally(question_data):
    data = deepcopy(question_data)

    error_name, error_code = random.choice(data["error_patterns"])
    error_text = random.choice(data["error_text_candidates"])
    finally_text = random.choice(data["finally_text_candidates"])

    create_generated_base(data)

    data["generated_values"] = {
        "error_name": error_name,
        "error_code": error_code,
        "error_text": error_text,
        "finally_text": finally_text
    }

    data["question"] = data["template"].format(
        error_name=error_name,
        error_text=error_text,
        finally_text=finally_text
    )

    data["expected_output"] = f"{error_text}\n{finally_text}"

    if error_name in ["SyntaxError", "IndentationError"]:
        code_line = indent_code_block(f'exec({repr(error_code)})')
    else:
        code_line = indent_code_block(error_code)

    data["model_answers"] = [
        f'try:\n{code_line}\nexcept:\n    print("{error_text}")\nfinally:\n    print("{finally_text}")',
        f"try:\n{code_line}\nexcept:\n    print('{error_text}')\nfinally:\n    print('{finally_text}')"
    ]

    cleanup_generator_fields(data)
    return data


def generate_multiple_except(question_data):
    data = deepcopy(question_data)

    pattern = random.choice(data["multiple_error_patterns"])

    error_name1 = pattern[0]
    error_code1 = pattern[1]
    error_text1 = pattern[2]

    error_name2 = pattern[3]
    error_code2 = pattern[4]
    error_text2 = pattern[5]

    selected_error_name = random.choice([error_name1, error_name2])

    if selected_error_name == error_name1:
        selected_code = error_code1
        expected_output = error_text1
    else:
        selected_code = error_code2
        expected_output = error_text2

    create_generated_base(data)

    data["generated_values"] = {
        "error_name1": error_name1,
        "error_name2": error_name2,
        "selected_error_name": selected_error_name
    }

    data["question"] = data["template"].format(
        error_name1=error_name1,
        error_name2=error_name2
    )

    data["expected_output"] = expected_output
    data["required_keywords"] = [
        "try",
        "except",
        error_name1,
        error_name2,
        "print"
    ]

    if selected_error_name in ["SyntaxError", "IndentationError"]:
        code_line = indent_code_block(f'exec({repr(selected_code)})')
    else:
        code_line = indent_code_block(selected_code)

    data["model_answers"] = [
        f'try:\n{code_line}\nexcept {error_name1}:\n    print("{error_text1}")\nexcept {error_name2}:\n    print("{error_text2}")',
        f"try:\n{code_line}\nexcept {error_name1}:\n    print('{error_text1}')\nexcept {error_name2}:\n    print('{error_text2}')"
    ]

    cleanup_generator_fields(data)
    return data
# =====================================
# 共通処理
# =====================================

def cleanup_generator_fields(data):
    remove_keys = [
        "generator_type",
        "template",
        "number_min",
        "number_max",
        "a_min",
        "a_max",
        "b_min",
        "b_max",
        "c_min",
        "c_max",
        "string_candidates",
        "pairs",
        "operator_candidates",
        "variable_candidates",
        "left_variable_candidates",
        "right_variable_candidates",
        "start_min",
        "start_max",
        "change_min",
        "change_max",
        "x_min",
        "x_max",
        "y_min",
        "y_max",
        "count_min",
        "count_max",
        "list_length",
        "list_length_min",
        "list_length_max",
        "operations",
        "end_min",
        "end_max",
        "greeting_candidates",
        "prompt_candidates",
        "input_min",
        "input_max",
        "add_min",
        "add_max",
        "n_min",
        "n_max",
        "function_name_candidates",
        "text_candidates",
        "score_min",
        "score_max",
        "border_min",
        "border_max",
        "greeting_candidates",
        "name_candidates",
        "replace_pairs",
        "concat_pairs",
        "split_patterns",
        "dict_name_candidates",
        "key_value_pairs",
        "dict_patterns",
        "operation_candidates",
        "add_candidates",
        "string_update_candidates",
        "number_update_candidates",
        "text_candidates",
        "root_min",
        "root_max",
        "function_candidates",
        "number_candidates",
        "min_candidates",
        "max_candidates",
        "list_candidates",
        "before_candidates",
        "after_candidates",
        "second_candidates",
        "error_patterns",
        "error_text_candidates",
        "finally_text_candidates",
        "multiple_error_patterns",
    ]

    for key in remove_keys:
        data.pop(key, None)


GENERATOR_MAP = {
    "print_number": generate_print_number,
    "print_string": generate_print_string,
    "calculation": generate_calculation,
    "addition": generate_addition,
    "string_concat": generate_string_concat,
    "mixed_output": generate_mixed_output,
    "mixed_concat_output": generate_mixed_concat_output,
    "mixed_calculation_output": generate_mixed_calculation_output,

    "variable_number": generate_variable_number,
    "variable_string": generate_variable_string,
    "variable_update": generate_variable_update,
    "variable_short_update": generate_variable_short_update,
    "two_variable_calculation": generate_two_variable_calculation,
    "three_variable_calculation": generate_three_variable_calculation,

    "if_compare_only": generate_if_compare_only,
    "if_else_compare": generate_if_else_compare,
    "if_elif_else_compare": generate_if_elif_else_compare,
    "if_compare_constant": generate_if_compare_constant,
    "if_else_parity": generate_if_else_parity,
    "if_elif_else_band": generate_if_elif_else_band,

    "for_range_output": generate_for_range_output,
    "for_range_sum": generate_for_range_sum,
    "for_even_sum": generate_for_even_sum,

    "list_output": generate_list_output,
    "list_single_operation": generate_list_single_operation,
    "list_double_operation": generate_list_double_operation,

    "debug_missing_colon": generate_debug_missing_colon,
    "debug_missing_quote": generate_debug_missing_quote,
    "debug_missing_parenthesis": generate_debug_missing_parenthesis,
    "debug_indent_error": generate_debug_indent_error,
    "debug_missing_print": generate_debug_missing_print,
    "debug_wrong_variable": generate_debug_wrong_variable,
    "debug_range_end_error": generate_debug_range_end_error,
    "debug_compare_operator_error": generate_debug_compare_operator_error,
    "debug_logic_condition_error": generate_debug_logic_condition_error,

    "input_greeting": generate_input_greeting,
    "input_str": generate_input_str,
    "input_int": generate_input_int,
    "input_prompt": generate_input_prompt,
    "input_add": generate_input_add,
    "input_multiply": generate_input_multiply,
    "input_sum_until_n": generate_input_sum_until_n,
    "input_product_until_n": generate_input_product_until_n,

    "function_print": generate_function_print,
    "function_return_calculation": generate_function_return_calculation,
    "function_if_return": generate_function_if_return,
    "function_for_print": generate_function_for_print,
    "function_sum_return": generate_function_sum_return,
    "function_string_return": generate_function_string_return,
    "function_even_odd": generate_function_even_odd,

    "string_upper": generate_string_upper,
    "string_lower": generate_string_lower,
    "string_len": generate_string_len,
    "string_replace": generate_string_replace,
    "string_concat_basic": generate_string_concat_basic,
    "string_split": generate_string_split,
    "string_strip": generate_string_strip,
    "string_replace_upper": generate_string_replace_upper,
    "string_concat_len": generate_string_concat_len,

    "dict_create_one": generate_dict_create_one,
    "dict_create_two": generate_dict_create_two,
    "dict_single_operation": generate_dict_single_operation,
    "dict_double_operation": generate_dict_double_operation,

    "while_range_output": generate_while_range_output,
    "while_sum": generate_while_sum,
    "while_repeat_string": generate_while_repeat_string,
    "while_multiply": generate_while_multiply,
    "while_even_output": generate_while_even_output,
    "while_odd_output": generate_while_odd_output,
    "while_countdown": generate_while_countdown,

    "math_sqrt": generate_math_sqrt,
    "math_pi": generate_math_pi,
    "math_floor_ceil": generate_math_floor_ceil,
    "random_randint": generate_random_randint,
    "random_shuffle": generate_random_shuffle,
    "time_sleep": generate_time_sleep,
    "time_time": generate_time_time,
    "datetime_today": generate_datetime_today,
    "datetime_now": generate_datetime_now,

    "try_except_basic": generate_try_except_basic,
    "specific_error": generate_specific_error,
    "try_except_finally": generate_try_except_finally,
    "multiple_except": generate_multiple_except,
}


def generate_question(question_data):
    generator_type = question_data.get("generator_type")

    if not generator_type:
        return question_data

    generator = GENERATOR_MAP.get(generator_type)

    if not generator:
        return question_data

    return generator(question_data)