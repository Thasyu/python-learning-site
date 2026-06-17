#ユーザーの復習キューを管理するモジュール
import json
import sqlite3

from backend.db import get_connection


#復習問題一覧取得関数
def load_review_queue(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT question_id, question_snapshot FROM review_queue WHERE user_id = ?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


#復習キューへ問題を追加する関数
def add_to_review_queue(user_id, question_data):
    conn = get_connection()
    cursor = conn.cursor()

    question_snapshot = json.dumps(question_data, ensure_ascii=False)

    try:
        cursor.execute(
            """
            INSERT INTO review_queue (
                user_id,
                question_id,
                question_snapshot
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                question_data["id"],
                question_snapshot
            )
        )
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" not in str(e):
            conn.close()
            raise

    conn.commit()
    conn.close()


#復習キューから問題を削除する関数
def remove_from_review_queue(user_id, question_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM review_queue WHERE user_id = ? AND question_id = ?",
        (user_id, question_id)
    )

    conn.commit()
    conn.close()