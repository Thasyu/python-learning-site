#jsonを扱うためのモジュール
import json

#日時を扱うためのモジュールをインポート
from datetime import datetime

#データベース接続用の関数をインポート
from backend.db import get_connection

#現在の学習状態を保存・更新する関数
def save_study_session(user_id, payload):
    conn = get_connection()
    cursor = conn.cursor()

    updated_at = datetime.now().isoformat(timespec="seconds")
    question_ids_json = json.dumps(payload["question_ids"], ensure_ascii=False)
    answered_ids_json = json.dumps(payload["answered_question_ids"], ensure_ascii=False)
    question_snapshot_json = json.dumps(payload.get("question_snapshot") or [], ensure_ascii=False)

    cursor.execute(
        """
        SELECT id
        FROM study_sessions
        WHERE user_id = ?
        ORDER BY updated_at DESC, id DESC
        LIMIT 1
        """,
        (user_id,)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            """
            UPDATE study_sessions
            SET chapter = ?,
                mode = ?,
                review_mode = ?,
                question_ids = ?,
                question_snapshot = ?,
                current_question_index = ?,
                correct_count = ?,
                answered_question_ids = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                payload["chapter"],
                payload["mode"],
                1 if payload["review_mode"] else 0,
                question_ids_json,
                question_snapshot_json,
                payload["current_question_index"],
                payload["correct_count"],
                answered_ids_json,
                updated_at,
                existing["id"]
            )
        )
    else:
        cursor.execute(
            """
            INSERT INTO study_sessions (
                user_id,
                chapter,
                mode,
                review_mode,
                question_ids,
                question_snapshot,
                current_question_index,
                correct_count,
                answered_question_ids,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                payload["chapter"],
                payload["mode"],
                1 if payload["review_mode"] else 0,
                question_ids_json,
                question_snapshot_json,
                payload["current_question_index"],
                payload["correct_count"],
                answered_ids_json,
                updated_at
            )
        )

    conn.commit()
    conn.close()

#最新の学習状態を取得する関数
def get_latest_study_session(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM study_sessions
        WHERE user_id = ?
        ORDER BY updated_at DESC, id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    session = dict(row)
    session["review_mode"] = bool(session["review_mode"])

    try:
        session["question_ids"] = json.loads(session["question_ids"])
    except json.JSONDecodeError:
        session["question_ids"] = []

    try:
        session["answered_question_ids"] = json.loads(session["answered_question_ids"])
    except json.JSONDecodeError:
        session["answered_question_ids"] = []

    try:
        session["question_snapshot"] = json.loads(session.get("question_snapshot") or "[]")
    except json.JSONDecodeError:
        session["question_snapshot"] = []

    return session

#保存済み学習状態を削除する関数
def delete_study_session(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM study_sessions WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()
