#JSONを扱うためのモジュールをインポート
import json

#問題データをJSONファイルから読み込む関数
def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

#全ての問題をまとめる
def get_chapters():
    return {
        1: {
            "name": "出力と基本",
            "questions": load_questions("questions/chapter1.json")
        },
        2: {
            "name": "変数",
            "questions": load_questions("questions/chapter2.json")
        },
        3: {
            "name": "条件分岐",
            "questions": load_questions("questions/chapter3.json")
        },
        4: {
            "name": "ループ",
            "questions": load_questions("questions/chapter4.json")
        },
        5: {
            "name": "リスト",
            "questions": load_questions("questions/chapter5.json")
        },
        6: {
            "name": "デバッグ",
            "questions": load_questions("questions/chapter6.json")
        },
        7: {
            "name": "input",
            "questions": load_questions("questions/chapter7.json")
        },
        8: {
            "name": "関数",
            "questions": load_questions("questions/chapter8.json")
        },
        9: {
            "name": "文字列",
            "questions": load_questions("questions/chapter9.json")
        },
        10: {
            "name": "辞書",
            "questions": load_questions("questions/chapter10.json")
        },
        11: {
            "name": "while",
            "questions": load_questions("questions/chapter11.json")
        },
        12: {
            "name": "import",
            "questions": load_questions("questions/chapter12.json")
        },
        13: {
            "name": "例外処理",
            "questions": load_questions("questions/chapter13.json")
        },
    }