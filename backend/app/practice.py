from backend.app.sandbox import run_in_sandbox


MAX_PRACTICE_CODE_LENGTH = 8000


def sanitize_practice_request(data):
    if not isinstance(data, dict):
        return None, None, "不正なリクエストです"

    code = data.get("code")

    if not isinstance(code, str):
        return None, None, "code は文字列で指定してください"

    normalized_code = code.replace("\r\n", "\n").replace("\r", "\n")

    if not normalized_code.strip():
        return None, None, "実行するコードを入力してください"

    if len(normalized_code) > MAX_PRACTICE_CODE_LENGTH:
        return None, None, f"コードが長すぎます（最大 {MAX_PRACTICE_CODE_LENGTH} 文字）"

    input_data = data.get("input_data")

    if input_data is None:
        normalized_input_data = None
    elif isinstance(input_data, str):
        normalized_input_data = input_data.replace("\r\n", "\n").replace("\r", "\n")
    else:
        return None, None, "input_data は文字列で指定してください"

    return normalized_code, normalized_input_data, None


def execute_practice_code(code, input_data=None):
    success, output, error = run_in_sandbox(code, input_data=input_data)

    return {
        "success": bool(success),
        "output": output or "",
        "error": None if success else (error or "実行エラーが発生しました")
    }
