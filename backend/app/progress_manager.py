#日時取得のためのライブラリ読み込み
from datetime import datetime

#DB接続関数のインポート
from backend.db import get_connection


#usernameからuser_idを取得する関数
def get_user_id(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return user["id"]

    return None

#回答結果を一つの学習データとしてまとめる関数
def create_result_record(user_id, question_data, is_correct, submitted_code, actual_output):
    return {
        "user_id": user_id,
        "question_id": question_data["id"],
        "chapter": question_data["chapter"],
        "difficulty": question_data["difficulty"],
        "is_correct": is_correct,
        "submitted_code": submitted_code,
        "actual_output": actual_output,
        "answered_at": datetime.now().isoformat(timespec="seconds")
    }

#回答結果をデータベースに保存する関数
def append_progress(record):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO answer_logs (
            user_id,
            question_id,
            chapter,
            difficulty,
            is_correct,
            submitted_code,
            actual_output,
            answered_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["user_id"],
        record["question_id"],
        record["chapter"],
        record["difficulty"],
        1 if record["is_correct"] else 0,
        record["submitted_code"],
        record["actual_output"],
        record["answered_at"]
    ))

    conn.commit()
    conn.close()

#ユーザーの回答履歴をデータベースから読み込む関数
def load_progress(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM answer_logs WHERE user_id = ?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

#chapterごとの正答率を計算する関数
def get_chapter_stats(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            chapter,
            COUNT(*) AS total,
            SUM(is_correct) AS correct
        FROM answer_logs
        WHERE user_id = ?
        GROUP BY chapter
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return {
        row["chapter"]: {
            "total": row["total"],
            "correct": row["correct"]
        }
        for row in rows
    }

#difficultyごとの正答率を計算する関数
def get_difficulty_stats(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            difficulty,
            COUNT(*) AS total,
            SUM(is_correct) AS correct
        FROM answer_logs
        WHERE user_id = ?
        GROUP BY difficulty
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return {
        row["difficulty"]: {
            "total": row["total"],
            "correct": row["correct"]
        }
        for row in rows
    }