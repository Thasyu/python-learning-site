#コードを解析するためのモジュール
import ast

#入出力を制限するためのモジュール
import io

#処理の流れを制御するためのモジュール
import contextlib

#標準ライブラリを読み込むモジュール。
import multiprocessing

#許可された組み込み関数のセット
BASE_ALLOWED_BUILTINS = {
    "print": print,
    "range": range,
    "len": len,
    "int": int,
    "str": str,
    "bool": bool,
    "float": float,
    "type": type,
    "SyntaxError": SyntaxError,
    "NameError": NameError,
    "TypeError": TypeError,
    "IndexError": IndexError,
    "ValueError": ValueError,
    "ZeroDivisionError": ZeroDivisionError,
    "IndentationError": IndentationError,
}

DISALLOWED_NAMES = {
    "eval",
    "exec",
    "__import__",
    "compile",
    "globals",
    "locals",
    "vars",
    "help",
    "dir",
}

ALLOWED_MODULES = {
    "math",
    "random",
    "time",
    "datetime",
}

DISALLOWED_NODES = (
    ast.With,
    ast.ClassDef,
    ast.Lambda,
    ast.Global,
    ast.Nonlocal,
)

#コードを解析して使用禁止の構文や名前が含まれていないか確認する関数
def validate_code(code: str, allow_input=False):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        error_type_name = type(e).__name__
        return False, f"{error_type_name}: {e}"
    
    for node in ast.walk(tree):
        if isinstance(node, DISALLOWED_NODES):
            return False, f"使用できない構文が含まれています: {type(node).__name__}"
        
        if isinstance(node, ast.Name):
            if node.id in DISALLOWED_NAMES:
                return False, f"使用できない名前が含まれています: {node.id}"

            if not allow_input and node.id == "input":
                return False, "inputはこの問題では使用できません"
        
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in DISALLOWED_NAMES:
                    return False, f"使用できない関数呼び出しが含まれています: {node.func.id}"
                
                if not allow_input and node.func.id == "input":
                    return False, "inputはこの問題では使用できません"
                
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in ALLOWED_MODULES:
                    return False, f"使用できないモジュールです: {alias.name}"

        if isinstance(node, ast.ImportFrom):
            if node.module not in ALLOWED_MODULES:
                return False, f"使用できないモジュールです: {node.module}"
            
    return True, None

#コードを安全に実行するための関数
def _execute_code(code, return_dict, input_data=None):
    output_buffer = io.StringIO()

    allowed_builtins = BASE_ALLOWED_BUILTINS.copy()

    # Restrict import targets to whitelisted modules only.
    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".")[0]
        if root not in ALLOWED_MODULES:
            raise ImportError(f"使用できないモジュールです: {name}")
        return __import__(name, globals, locals, fromlist, level)

    allowed_builtins["__import__"] = safe_import

    if input_data is not None:
        inputs = input_data.split("\n")
        input_iter = iter(inputs)

        def fake_input(prompt=""):
            try:
                return next(input_iter)
            except StopIteration:
                return ""
            
        allowed_builtins["input"] = fake_input

    safe_globals = {
        "__builtins__": allowed_builtins
    }

    safe_locals = {}

    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, safe_globals, safe_locals)
        
        return_dict["success"] = True
        return_dict["output"] = output_buffer.getvalue().strip()
        return_dict["error"] = None

    except Exception as e:
        return_dict["success"] = False
        return_dict["output"] = ""
        error_type_name = type(e).__name__
        return_dict["error"] = f"{error_type_name}: {e}"

#サンドボックス環境でコードを安全に実行する関数
def run_in_sandbox(code: str, timeout=4, input_data=None):
    allow_input = input_data is not None

    is_valid, error_message = validate_code(code, allow_input=allow_input)
    if not is_valid:
        return False, "", error_message
    
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    process = multiprocessing.Process(
        target=_execute_code,
        args=(code, return_dict, input_data)
    )

    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return False, "", "実行時間が長すぎます（無限ループの可能性）"
    
    return(
        return_dict.get("success", False),
        return_dict.get("output", ""),
        return_dict.get("error", None)
    )