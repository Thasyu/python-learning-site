# jsonを扱うためのモジュールをインポート
import json
import random

#ファイル・フォルダの操作を行うためのモジュールをインポート
import os

#正規表現を扱うためのモジュールをインポート
import re
import hashlib
import imghdr

#ログを記録するためのモジュールをインポート
import logging

#安全なランダム文字列を生成するためのモジュールをインポート
import secrets

#SQLiteデータベースを扱うためのモジュールをインポート
import sqlite3

#日時を扱うためのモジュールをインポート
from datetime import datetime, timedelta

#URLパラメータを安全に作成するためのモジュールをインポート
from urllib.parse import urlencode

#.envファイルの環境変数を読み込むための関数をインポート
from dotenv import load_dotenv

#webフレームワークのflaskをインポート
from flask import Flask, jsonify, request, send_from_directory

#CORSを有効にするためのflask_corsからCORSをインポート
from flask_cors import CORS

#学習の進捗や統計情報を提供する関数のインポート
from backend.app.progress_manager import (
    load_progress,
    get_chapter_stats,
    get_difficulty_stats,
    create_result_record,
    append_progress
    )

#復習キューの情報を提供する関数のインポート
from backend.app.review import (
    load_review_queue,
    add_to_review_queue,
    remove_from_review_queue
    )

#採点機能のための関数のインポート
from backend.app.judge import judge

#学習セッションの管理関数のインポート
from backend.app.study_session import (
    save_study_session,
    get_latest_study_session,
    delete_study_session
)
from backend.app.practice import sanitize_practice_request, execute_practice_code

#パスワード再設定メール送信機能関数のインポート
from backend.mail import send_password_reset_email, send_email_change_confirmation

#ユーザーデータの管理関数のインポート
from backend.db import get_connection, init_db, migrate_db  

#パスワードをハッシュ化するための関数のインポート
from werkzeug.security import generate_password_hash

#パスワードが正しいか確認するための関数のインポート
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

#問題生成機能のための関数のインポート
from backend.app.question_generator import generate_question

#Flaskアプリケーションの土台を作成
app = Flask(__name__)

#CORSを有効にする
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

#.envファイルから環境変数を読み込む
load_dotenv()

#ログ出力の設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

#ファイル専用のログ出力オブジェクトを作成
logger = logging.getLogger(__name__)

#トークン期限切れ時に使うエラーメッセージを定義
TOKEN_EXPIRED_MESSAGE = "認証の有効期限が切れています。再ログインしてください。"

#問題データが入っているフォルダ名を定義
QUESTIONS_DIR = "questions"

#読み込んだ問題データを一時的に保存するための変数を定義
QUESTIONS_CACHE = []

#問題idから問題データを高速検索するための辞書を定義
QUESTIONS_BY_ID = {}

QUESTION_MODE_PLANS = {
    "recommended": {1: 4, 2: 3, 3: 3},
    "beginner": {1: 10},
    "intermediate": {2: 10},
    "advanced": {3: 10},
}

MODE_ALIASES = {
    "easy": "beginner",
    "normal": "intermediate",
    "hard": "advanced",
}

STUDY_MIN_CHAPTER = 1
STUDY_MAX_CHAPTER = 13
STUDY_LAYOUT_MIGRATED_AT = datetime(2026, 6, 8, 0, 0, 0)

#パスワード再設定用トークンの有効期限を30分に設定しているコード
PASSWORD_RESET_TOKEN_LIFETIME_MINUTES = 30
EMAIL_CHANGE_TOKEN_LIFETIME_MINUTES = 30
EMAIL_CHANGE_REQUEST_RATE_LIMIT = 5
EMAIL_CHANGE_REQUEST_RATE_WINDOW_MINUTES = 30
PASSWORD_CHANGE_RATE_LIMIT = 5
PASSWORD_CHANGE_RATE_WINDOW_MINUTES = 15
PASSWORD_CHANGE_ATTEMPTS = {}
DISPLAY_NAME_MAX_LENGTH = 30
BIO_MAX_LENGTH = 160
MAX_AVATAR_FILE_SIZE = 2 * 1024 * 1024
ALLOWED_AVATAR_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp"
}
ALLOWED_AVATAR_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}
IMAGE_KIND_TO_EXTENSION = {
    "png": ".png",
    "jpeg": ".jpg",
    "webp": ".webp"
}
AVATAR_URL_PREFIX = "/uploads/avatars/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AVATAR_UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "avatars")

#パスワード再設定ページのURLを設定しているコード
PASSWORD_RESET_PAGE_URL = os.getenv(
    "PASSWORD_RESET_PAGE_URL",
    "http://127.0.0.1:5500/pages/reset-password.html"
)

EMAIL_CHANGE_CONFIRM_PAGE_URL = os.getenv(
    "EMAIL_CHANGE_CONFIRM_PAGE_URL",
    "http://127.0.0.1:5500/pages/confirm-email-change.html"
)

#メールアドレス形式が正しいか確認するための正規表現
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)

#学習の進捗や統計情報を提供する関数
def get_progress_summary(user_id):
    progress_data = load_progress(user_id)
    parsed_progress = []

    for record in progress_data:
        answered_at = record.get("answered_at")

        try:
            answered_at_dt = datetime.fromisoformat(answered_at)
        except (TypeError, ValueError):
            continue

        parsed_progress.append({
            **record,
            "answered_at_dt": answered_at_dt
        })

    parsed_progress.sort(key=lambda record: record["answered_at_dt"], reverse=True)

    total_answers = len(progress_data)
    total_correct = sum(1 for record in progress_data if record["is_correct"])
    accuracy = (total_correct / total_answers) * 100 if total_answers > 0 else 0
    review_count = len(load_review_queue(user_id))

    active_dates = sorted(
        {record["answered_at_dt"].date() for record in parsed_progress},
        reverse=True
    )
    today = datetime.now().date()
    current_streak = 0

    if active_dates and active_dates[0] >= today - timedelta(days=1):
        expected_date = active_dates[0]

        for active_date in active_dates:
            if active_date == expected_date:
                current_streak += 1
                expected_date -= timedelta(days=1)
                continue

            if active_date < expected_date:
                break

    longest_streak = 0
    working_streak = 0
    previous_date = None

    for active_date in sorted(active_dates):
        if previous_date is None or active_date == previous_date + timedelta(days=1):
            working_streak += 1
        elif active_date != previous_date:
            working_streak = 1

        previous_date = active_date
        longest_streak = max(longest_streak, working_streak)

    recent_activity = [
        {
            "question_id": record["question_id"],
            "chapter": record["chapter"],
            "difficulty": record["difficulty"],
            "is_correct": bool(record["is_correct"]),
            "answered_at": record["answered_at"]
        }
        for record in parsed_progress[:6]
    ]

    recent_window = parsed_progress[:10]
    recent_accuracy = 0

    if recent_window:
        recent_accuracy = round(
            sum(1 for record in recent_window if record["is_correct"]) / len(recent_window) * 100,
            1
        )

    recent_week_answers = sum(
        1
        for record in parsed_progress
        if record["answered_at_dt"].date() >= today - timedelta(days=6)
    )

    return {
        "total_answers": total_answers,
        "total_correct": total_correct,
        "accuracy": round(accuracy, 1),
        "review_count": review_count,
        "active_days": len(active_dates),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "recent_accuracy": recent_accuracy,
        "recent_week_answers": recent_week_answers,
        "last_activity_at": parsed_progress[0]["answered_at"] if parsed_progress else None,
        "recent_activity": recent_activity
    }

#HTTPヘッダーからBearer Tokenを取り出す関数
def extract_bearer_token():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1].strip()
    return token if token else None

#tokenからuser_idを取得する関数
def get_user_id_from_token(token):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT t.user_id, t.expires_at, COALESCE(u.is_deleted, 0) AS is_deleted
        FROM tokens t
        LEFT JOIN users u ON u.id = t.user_id
        WHERE t.token = ?
        """,
        (token,)
    )

    row = cursor.fetchone()

    if not row:
        conn.close()
        return None, False

    if row["is_deleted"] == 1:
        cursor.execute(
            "DELETE FROM tokens WHERE token = ?",
            (token,)
        )
        conn.commit()
        conn.close()
        return None, False

    try:
        expires_at = datetime.fromisoformat(row["expires_at"])
    except ValueError:
        expires_at = None

    if expires_at is None or datetime.now() >= expires_at:
        cursor.execute(
            "DELETE FROM tokens WHERE token = ?",
            (token,)
        )
        conn.commit()
        conn.close()
        return None, True

    conn.close()
    return row["user_id"], False

#現在ログイン中の user_id を取得する関数
def get_current_user_id():
    token = extract_bearer_token()

    if not token:
        return None, "認証が必要です"

    user_id, is_expired = get_user_id_from_token(token)

    if is_expired:
        return None, TOKEN_EXPIRED_MESSAGE

    if not user_id:
        return None, "認証が必要です"

    return user_id, None

#ログイン用tokenを生成してDBへ保存する関数
def create_token_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    created_at = now.isoformat(timespec="seconds")
    expires_at = (now + timedelta(days=7)).isoformat(timespec="seconds")

    token = None
    for _ in range(5):
        candidate = secrets.token_hex(32)
        try:
            cursor.execute(
                "INSERT INTO tokens (user_id, token, created_at, expires_at) VALUES (?, ?, ?, ?)",
                (user_id, candidate, created_at, expires_at)
            )
            conn.commit()
            token = candidate
            break
        except sqlite3.IntegrityError:
            continue

    conn.close()
    return token

#パスワード再設定用tokenを生成してDB保存する関数
def create_password_reset_token(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    created_at = now.isoformat(timespec="seconds")
    expires_at = (now + timedelta(minutes=PASSWORD_RESET_TOKEN_LIFETIME_MINUTES)).isoformat(timespec="seconds")

    token = None
    for _ in range(5):
        candidate = secrets.token_urlsafe(48)
        try:
            cursor.execute(
                "INSERT INTO password_reset_tokens (user_id, token, expires_at, created_at, used_at) VALUES (?, ?, ?, ?, NULL)",
                (user_id, candidate, expires_at, created_at)
            )
            token = candidate
            break
        except sqlite3.IntegrityError:
            continue

    conn.commit()
    conn.close()
    return token


def hash_secure_token(raw_token):
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def create_email_change_token(user_id, new_email):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    created_at = now.isoformat(timespec="seconds")
    expires_at = (now + timedelta(minutes=EMAIL_CHANGE_TOKEN_LIFETIME_MINUTES)).isoformat(timespec="seconds")

    token = None
    for _ in range(5):
        candidate = secrets.token_urlsafe(48)
        token_hash = hash_secure_token(candidate)
        try:
            cursor.execute(
                "INSERT INTO email_change_tokens (user_id, new_email, token_hash, expires_at, created_at, used_at) VALUES (?, ?, ?, ?, ?, NULL)",
                (user_id, new_email, token_hash, expires_at, created_at)
            )
            token = candidate
            break
        except sqlite3.IntegrityError:
            continue

    conn.commit()
    conn.close()
    return token


def delete_email_change_token_by_raw_token(raw_token):
    token_hash = hash_secure_token(raw_token)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM email_change_tokens WHERE token_hash = ?",
        (token_hash,)
    )
    conn.commit()
    conn.close()


def invalidate_user_auth_state(user_id, cursor):
    cursor.execute(
        "DELETE FROM tokens WHERE user_id = ?",
        (user_id,)
    )
    cursor.execute(
        "DELETE FROM password_reset_tokens WHERE user_id = ?",
        (user_id,)
    )
    cursor.execute(
        "DELETE FROM email_change_tokens WHERE user_id = ?",
        (user_id,)
    )


def prune_password_change_attempts(user_id):
    now = datetime.now()
    window = timedelta(minutes=PASSWORD_CHANGE_RATE_WINDOW_MINUTES)
    attempts = PASSWORD_CHANGE_ATTEMPTS.get(user_id, [])
    attempts = [attempt for attempt in attempts if now - attempt < window]
    PASSWORD_CHANGE_ATTEMPTS[user_id] = attempts
    return attempts


def record_password_change_attempt(user_id):
    attempts = prune_password_change_attempts(user_id)
    attempts.append(datetime.now())
    PASSWORD_CHANGE_ATTEMPTS[user_id] = attempts


def is_password_change_rate_limited(user_id):
    attempts = prune_password_change_attempts(user_id)
    return len(attempts) >= PASSWORD_CHANGE_RATE_LIMIT

#パスワード再設定ページ用URLを作成する関数
def build_password_reset_url(token):
    query = urlencode({"token": token})
    return f"{PASSWORD_RESET_PAGE_URL}?{query}"


def build_email_change_confirm_url(token):
    query = urlencode({"token": token})
    return f"{EMAIL_CHANGE_CONFIRM_PAGE_URL}?{query}"

#全ての問題データを読み込む関数
def load_all_questions():
    global QUESTIONS_CACHE, QUESTIONS_BY_ID

    all_questions = []

    for filename in sorted(os.listdir(QUESTIONS_DIR)):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(QUESTIONS_DIR, filename)

        try:
            with open(filepath, "r", encoding="UTF-8") as f:
                questions = json.load(f)

            if not isinstance(questions, list):
                logger.warning("[questions] %s failed: root is not a list", filename)
                continue

            all_questions.extend(questions)
            logger.info("[questions] %s loaded: %d", filename, len(questions))

        except Exception as error:
            logger.error("[questions] %s failed: %r", filename, error)
            continue

    QUESTIONS_CACHE = all_questions
    QUESTIONS_BY_ID = {
        question["id"]: question
        for question in QUESTIONS_CACHE
        if "id" in question
    }

    logger.info("[startup] loaded questions: %d", len(QUESTIONS_CACHE))

    return QUESTIONS_CACHE

#問題キャッシュを再読み込みするための関数
def reload_questions_cache():
    return load_all_questions()

#問題IDから問題データを取得する関数
def get_question_by_id(question_id):
    return QUESTIONS_BY_ID.get(question_id)


def build_questions_for_mode(chapter, mode):
    chapter_questions = [
        q for q in QUESTIONS_CACHE
        if q.get("chapter") == chapter
    ]
    seen_questions = set()

    def generate_unique_question(base_question, max_attempts=50):
        for _ in range(max_attempts):
            generated_question = generate_question(base_question)
            question_text = generated_question.get("question", "")

            if question_text not in seen_questions:
                seen_questions.add(question_text)
                QUESTIONS_BY_ID[generated_question["id"]] = generated_question
                return generated_question

        return None

    if chapter not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13):
        generated_questions = []

        for q in chapter_questions:
            question = generate_unique_question(q)

            if question is not None:
                generated_questions.append(question)

        return generated_questions

    normalized_mode = (mode or "").strip().lower()
    normalized_mode = MODE_ALIASES.get(normalized_mode, normalized_mode)
    plan = QUESTION_MODE_PLANS.get(normalized_mode, QUESTION_MODE_PLANS["recommended"])

    selected_questions = []

    for difficulty, count in plan.items():
        candidates = [
            q for q in chapter_questions
            if q.get("difficulty") == difficulty
        ]

        if not candidates:
            continue

        added_count = 0
        attempts = 0
        max_attempts = max(count * 100, 100)

        while added_count < count and attempts < max_attempts:
            base_question = random.choice(candidates)
            generated_question = generate_unique_question(base_question)
            attempts += 1

            if generated_question is None:
                continue

            selected_questions.append(generated_question)
            added_count += 1

    return selected_questions

#問題配信時に公開してよい項目だけへ変換する関数
def to_public_question_dto(question):
    return {
        "id": question["id"],
        "chapter": question["chapter"],
        "category": question["category"],
        "difficulty": question["difficulty"],
        "question": question["question"],
        "starter_code": question.get("starter_code", ""),
        "ending_code": question.get("ending_code", ""),
        "judge_type": question.get("judge_type", ""),
        "expected_output": question.get("expected_output"),
        "required_keywords": question.get("required_keywords", []),
        "input_data": question.get("input_data", ""),
        "explanation": question.get("explanation", ""),
        "model_answers": question.get("model_answers", []),
        "hints": question.get("hints", []),
        "generated_values": question.get("generated_values")
    }

#study_session保存用データが正しい形か確認する関数
def validate_study_session_payload(data):
    required_fields = [
        "chapter",
        "mode",
        "review_mode",
        "question_ids",
        "question_snapshot",
        "current_question_index",
        "correct_count",
        "answered_question_ids"
    ]

    if not data:
        return "不正なリクエスト"

    for field in required_fields:
        if field not in data:
            return f"{field}がありません"

    if not isinstance(data["chapter"], int):
        return "chapterは整数である必要があります"

    if data["chapter"] < STUDY_MIN_CHAPTER or data["chapter"] > STUDY_MAX_CHAPTER:
        return "chapterの値が不正です"

    if not isinstance(data["mode"], str) or not data["mode"].strip():
        return "modeは文字列である必要があります"

    if not isinstance(data["review_mode"], bool):
        return "review_modeは真偽値である必要があります"

    if not isinstance(data["question_ids"], list):
        return "question_idsは配列である必要があります"

    if not isinstance(data["question_snapshot"], list):
        return "question_snapshotは配列である必要があります"

    if not isinstance(data["current_question_index"], int):
        return "current_question_indexは整数である必要があります"

    if not isinstance(data["correct_count"], int):
        return "correct_countは整数である必要があります"

    if not isinstance(data["answered_question_ids"], list):
        return "answered_question_idsは配列である必要があります"

    if any(not isinstance(question_id, str) for question_id in data["question_ids"]):
        return "question_idsの要素は文字列である必要があります"

    if any(not isinstance(question_id, str) for question_id in data["answered_question_ids"]):
        return "answered_question_idsの要素は文字列である必要があります"

    if any(not isinstance(question, dict) for question in data["question_snapshot"]):
        return "question_snapshotの要素はオブジェクトである必要があります"

    snapshot_ids = [question.get("id") for question in data["question_snapshot"]]

    if any(not isinstance(question_id, str) for question_id in snapshot_ids):
        return "question_snapshot.idは文字列である必要があります"

    if snapshot_ids != data["question_ids"]:
        return "question_idsとquestion_snapshotの内容が一致しません"

    return None


def is_valid_study_session(session):
    if not session:
        return False

    chapter = session.get("chapter")
    if not isinstance(chapter, int):
        return False

    if chapter < STUDY_MIN_CHAPTER or chapter > STUDY_MAX_CHAPTER:
        return False

    question_ids = session.get("question_ids")
    if not isinstance(question_ids, list):
        return False

    question_snapshot = session.get("question_snapshot")
    if not isinstance(question_snapshot, list):
        return False

    if len(question_snapshot) == 0:
        return False

    snapshot_ids = [question.get("id") for question in question_snapshot if isinstance(question, dict)]

    if len(snapshot_ids) != len(question_snapshot):
        return False

    if any(not isinstance(question_id, str) for question_id in snapshot_ids):
        return False

    if snapshot_ids != question_ids:
        return False

    updated_at = session.get("updated_at")
    try:
        updated_at_dt = datetime.fromisoformat(updated_at)
    except (TypeError, ValueError):
        return False

    # Drop sessions created before chapter migration to avoid wrong resume mapping.
    if updated_at_dt < STUDY_LAYOUT_MIGRATED_AT:
        return False

    for question_id in question_ids:
        if not isinstance(question_id, str):
            return False

    return True

#ログインID(username)に使用してよい文字の正規表現
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

#ユーザーIDの制約を確認する関数
def validate_username(username):
    if not isinstance(username, str):
        return "ログインIDは1〜20文字で入力してください。"

    if not 1 <= len(username) <= 20:
        return "ログインIDは1〜20文字で入力してください。"

    if re.search(r"\s", username):
        return "ログインIDに空白は使えません。"

    if not USERNAME_PATTERN.fullmatch(username):
        return "ログインIDは英数字と_のみ使用できます。"

    return None


def validate_display_name(display_name):
    if not isinstance(display_name, str):
        return "ニックネームは1〜30文字で入力してください。"

    if not display_name.strip():
        return "ニックネームを入力してください。"

    if display_name != display_name.strip():
        return "ニックネームの前後に空白は使えません。"

    if len(display_name) > DISPLAY_NAME_MAX_LENGTH:
        return "ニックネームは30文字以内で入力してください。"

    if re.search(r"[\x00-\x1f\x7f]", display_name):
        return "ニックネームに制御文字は使えません。"

    if "<" in display_name or ">" in display_name:
        return "ニックネームに使用できない文字が含まれています。"

    return None


def sanitize_bio(bio):
    if bio is None:
        return "", None

    if not isinstance(bio, str):
        return None, "自己紹介は文字列で入力してください。"

    trimmed_bio = bio.strip()

    if len(trimmed_bio) > BIO_MAX_LENGTH:
        return None, f"自己紹介は{BIO_MAX_LENGTH}文字以内で入力してください。"

    if re.search(r"[\x00-\x1f\x7f]", trimmed_bio):
        return None, "自己紹介に制御文字は使えません。"

    if "<" in trimmed_bio or ">" in trimmed_bio:
        return None, "自己紹介に使用できない文字が含まれています。"

    return trimmed_bio, None


def make_avatar_url(filename):
    return f"{AVATAR_URL_PREFIX}{filename}"


def get_avatar_path_from_url(avatar_url):
    if not isinstance(avatar_url, str) or not avatar_url.startswith(AVATAR_URL_PREFIX):
        return None

    filename = avatar_url[len(AVATAR_URL_PREFIX):]
    safe_filename = secure_filename(filename)

    if not safe_filename or safe_filename != filename:
        return None

    avatar_path = os.path.abspath(os.path.join(AVATAR_UPLOAD_DIR, safe_filename))
    base_path = os.path.abspath(AVATAR_UPLOAD_DIR)

    if os.path.commonpath([avatar_path, base_path]) != base_path:
        return None

    return avatar_path


def remove_avatar_file_if_exists(avatar_url):
    avatar_path = get_avatar_path_from_url(avatar_url)

    if avatar_path and os.path.isfile(avatar_path):
        try:
            os.remove(avatar_path)
        except OSError:
            logger.warning("[avatar] failed to remove old avatar file: %s", avatar_path)

#パスワードの制約を確認する関数
def validate_password(password):
    if not isinstance(password, str):
        return "パスワードは4〜32文字で入力してください。"

    if not 4 <= len(password) <= 32:
        return "パスワードは4〜32文字で入力してください。"

    if re.search(r"\s", password):
        return "パスワードに空白は使えません。"

    has_alpha = re.search(r"[A-Za-z]", password) is not None
    has_digit = any(character.isdigit() for character in password)

    if not has_alpha or not has_digit:
        return "パスワードには英字と数字を両方含めてください。"

    return None

#メールアドレスが正しい形式かチェックする関数
def validate_email(email):
    if not isinstance(email, str) or not email.strip():
        return "メールアドレスを入力してください。"

    if email != email.strip() or re.search(r"\s", email):
        return "メールアドレスに空白は使えません。"

    if "@" not in email:
        return "メールアドレスの形式が正しくありません。"

    local_part, _, domain_part = email.rpartition("@")
    if not local_part or not domain_part:
        return "メールアドレスの形式が正しくありません。"

    if not EMAIL_PATTERN.fullmatch(email):
        return "メールアドレスの形式が正しくありません。"

    return None

@app.route("/progress/summary")
def progress_summary():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    return jsonify(get_progress_summary(user_id))


@app.route("/me")
def me():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, display_name, avatar_url, bio, email, created_at FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"message": "ユーザーが存在しません"}), 404

    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "avatar_url": user["avatar_url"],
        "bio": user["bio"] or "",
        "email": user["email"],
        "created_at": user["created_at"]
    })


@app.route("/profile/display-name", methods=["POST"])
def update_display_name():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    data = request.json

    if not isinstance(data, dict) or "display_name" not in data:
        return jsonify({"message": "不正なリクエスト"}), 400

    display_name = data["display_name"]
    display_name_error = validate_display_name(display_name)

    if display_name_error:
        return jsonify({"message": display_name_error}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, display_name FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "ユーザーが存在しません"}), 404

    if display_name == user["display_name"]:
        conn.close()
        return jsonify({
            "message": "変更はありません。",
            "display_name": user["display_name"]
        })

    cursor.execute(
        "SELECT 1 FROM users WHERE lower(display_name) = lower(?) AND id != ? LIMIT 1",
        (display_name, user_id)
    )

    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "このニックネームはすでに使われています。"}), 400

    try:
        cursor.execute(
            "UPDATE users SET display_name = ? WHERE id = ?",
            (display_name, user_id)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "このニックネームはすでに使われています。"}), 400

    conn.close()

    return jsonify({
        "message": "ニックネームを更新しました。",
        "display_name": display_name,
        "username": user["username"]
    })


@app.route("/profile/bio", methods=["POST"])
def update_bio():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    data = request.json

    if not isinstance(data, dict) or "bio" not in data:
        return jsonify({"message": "不正なリクエスト"}), 400

    bio, bio_error = sanitize_bio(data.get("bio"))

    if bio_error:
        return jsonify({"message": bio_error}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, bio FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "ユーザーが存在しません"}), 404

    if bio == (user["bio"] or ""):
        conn.close()
        return jsonify({
            "message": "変更はありません。",
            "bio": bio
        })

    cursor.execute(
        "UPDATE users SET bio = ? WHERE id = ?",
        (bio, user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "message": "自己紹介を更新しました。",
        "bio": bio
    })


@app.route("/uploads/avatars/<path:filename>")
def serve_avatar(filename):
    safe_filename = secure_filename(filename)

    if not safe_filename or safe_filename != filename:
        return jsonify({"message": "画像が見つかりません。"}), 404

    avatar_path = get_avatar_path_from_url(make_avatar_url(safe_filename))

    if not avatar_path or not os.path.isfile(avatar_path):
        return jsonify({"message": "画像が見つかりません。"}), 404

    return send_from_directory(AVATAR_UPLOAD_DIR, safe_filename)


@app.route("/profile/avatar", methods=["POST"])
def upload_avatar():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    avatar_file = request.files.get("avatar")

    if not avatar_file or not avatar_file.filename:
        return jsonify({"message": "画像ファイルを選択してください。"}), 400

    if avatar_file.mimetype not in ALLOWED_AVATAR_MIME_TYPES:
        return jsonify({"message": "対応していない画像形式です。png/jpg/jpeg/webp を使用してください。"}), 400

    original_name = secure_filename(avatar_file.filename)
    extension = os.path.splitext(original_name)[1].lower()

    if not original_name or extension not in ALLOWED_AVATAR_EXTENSIONS:
        return jsonify({"message": "対応していない画像形式です。png/jpg/jpeg/webp を使用してください。"}), 400

    avatar_file.stream.seek(0, os.SEEK_END)
    file_size = avatar_file.stream.tell()
    avatar_file.stream.seek(0)

    if file_size <= 0:
        return jsonify({"message": "空のファイルはアップロードできません。"}), 400

    if file_size > MAX_AVATAR_FILE_SIZE:
        return jsonify({"message": "画像サイズが大きすぎます。2MB以下にしてください。"}), 400

    file_header = avatar_file.stream.read(512)
    avatar_file.stream.seek(0)
    detected_kind = imghdr.what(None, file_header)
    detected_extension = IMAGE_KIND_TO_EXTENSION.get(detected_kind)

    if not detected_extension:
        return jsonify({"message": "画像ファイルの形式を確認できませんでした。"}), 400

    normalized_extension = ".jpg" if extension == ".jpeg" else extension
    if normalized_extension != detected_extension:
        return jsonify({"message": "画像の拡張子と内容が一致しません。"}), 400

    os.makedirs(AVATAR_UPLOAD_DIR, exist_ok=True)
    random_filename = f"u{user_id}_{secrets.token_hex(16)}{detected_extension}"
    avatar_path = os.path.join(AVATAR_UPLOAD_DIR, random_filename)
    avatar_url = make_avatar_url(random_filename)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, avatar_url FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "ユーザーが存在しません"}), 404

    try:
        avatar_file.save(avatar_path)

        cursor.execute(
            "UPDATE users SET avatar_url = ? WHERE id = ?",
            (avatar_url, user_id)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        if os.path.isfile(avatar_path):
            os.remove(avatar_path)
        conn.close()
        logger.exception("[avatar] failed to save avatar file")
        return jsonify({"message": "画像の保存に失敗しました。"}), 500

    conn.close()

    old_avatar_url = user["avatar_url"]
    if old_avatar_url and old_avatar_url != avatar_url:
        remove_avatar_file_if_exists(old_avatar_url)

    logger.info("[avatar] user_id=%s updated avatar", user_id)

    return jsonify({
        "message": "プロフィール画像を更新しました。",
        "avatar_url": avatar_url
    })


@app.route("/progress/chapter")
def chapter_stats():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    return jsonify(get_chapter_stats(user_id))


@app.route("/progress/difficulty")
def difficulty_stats():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    return jsonify(get_difficulty_stats(user_id))

@app.route("/questions/chapter")
def questions_by_chapter():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    chapter = request.args.get("chapter", type=int)
    mode = request.args.get("mode", default="recommended", type=str)

    if chapter is None:
        return jsonify({"message": "chapterがありません"}), 400

    chapter_questions = build_questions_for_mode(chapter, mode)

    public_questions = [
        to_public_question_dto(question)
        for question in chapter_questions
    ]

    return jsonify(public_questions)


#ユーザーの回答を受け取り、採点して結果を返すエンドポイント
@app.route("/submit", methods=["POST"])
def submit_answer():
    data = request.json

    user_id, auth_error = get_current_user_id()
    if not user_id:
        return jsonify({"message": auth_error}), 401

    if (
        not data
        or "question_id" not in data
        or "user_code" not in data
    ):
        return jsonify({"message": "不正なリクエスト"}), 400

    question_id = data["question_id"]
    user_code = data["user_code"]

    question_data = get_question_by_id(question_id)
    if not question_data:
        return jsonify({"message": "問題が存在しません"}), 404

    is_correct, message, actual_output = judge(question_data, user_code)

    record = create_result_record(
        user_id=user_id,
        question_data=question_data,
        is_correct=is_correct,
        submitted_code=user_code,
        actual_output=actual_output
    )

    append_progress(record)

    if is_correct:
        remove_from_review_queue(user_id, question_data["id"])

    else:
        add_to_review_queue(user_id, question_data)

    return jsonify({
        "is_correct": is_correct,
        "message": message,
        "actual_output": actual_output,
        "explanation": question_data.get("explanation", ""),
        "model_answers": question_data.get("model_answers", []),
        "expected_output": question_data.get("expected_output", ""),
        "input_data": question_data.get("input_data", "")
    })


@app.route("/practice/run", methods=["POST"])
def run_practice_code():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    data = request.get_json(silent=True)
    code, input_data, validation_error = sanitize_practice_request(data)

    if validation_error:
        return jsonify({"message": validation_error}), 400

    result = execute_practice_code(code, input_data=input_data)
    return jsonify(result)

#復習キューに入っている問題の情報を提供するエンドポイント
@app.route("/questions/review")
def review_questions():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    review_items = load_review_queue(user_id)

    review_questions = []

    for item in review_items:
        snapshot = item.get("question_snapshot")

        if not snapshot:
            continue

        try:
            question_data = json.loads(snapshot)
        except json.JSONDecodeError:
            continue

        QUESTIONS_BY_ID[question_data["id"]] = question_data

        review_questions.append(
            to_public_question_dto(question_data)
        )

    return jsonify(review_questions)


@app.route("/study-session/save", methods=["POST"])
def save_current_study_session():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    data = request.json
    error_message = validate_study_session_payload(data)

    if error_message:
        return jsonify({"message": error_message}), 400

    save_study_session(user_id, data)

    return jsonify({"message": "学習セッションを保存しました"})


@app.route("/study-session/latest")
def get_current_study_session():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    session = get_latest_study_session(user_id)

    if session and not is_valid_study_session(session):
        delete_study_session(user_id)
        session = None

    return jsonify({"session": session})


@app.route("/study-session", methods=["DELETE"])
def clear_current_study_session():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    delete_study_session(user_id)

    return jsonify({"message": "学習セッションを削除しました"})

#ユーザー登録
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify({"message": "不正なリクエスト"}), 400

    username = data["username"]
    raw_display_name = data.get("display_name")
    display_name = username if raw_display_name is None else raw_display_name
    bio, bio_error = sanitize_bio(data.get("bio", ""))
    email = data["email"]
    password = data["password"]

    username_error = validate_username(username)
    if username_error:
        return jsonify({"message": username_error}), 400

    display_name_error = validate_display_name(display_name)
    if display_name_error:
        return jsonify({"message": display_name_error}), 400

    if bio_error:
        return jsonify({"message": bio_error}), 400

    password_error = validate_password(password)
    if password_error:
        return jsonify({"message": password_error}), 400

    email_error = validate_email(email)
    if email_error:
        return jsonify({"message": email_error}), 400

    hashed_password = generate_password_hash(password)
    created_at = datetime.now().isoformat(timespec="seconds")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,)
    )

    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "このユーザー名はすでに使われています。"}), 400

    cursor.execute(
        "SELECT 1 FROM users WHERE email = ?",
        (email,)
    )

    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "このメールアドレスはすでに使われています。"}), 400

    cursor.execute(
        "SELECT 1 FROM users WHERE display_name = ?",
        (display_name,)
    )

    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "このニックネームはすでに使われています。"}), 400

    try:
        cursor.execute(
            "INSERT INTO users (username, display_name, bio, email, password, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (username, display_name, bio, email, hashed_password, created_at)
        )

        conn.commit()
        return jsonify({"message": "登録成功"})

    except sqlite3.IntegrityError:
        return jsonify({"message": "このユーザー名またはメールアドレスはすでに使われています。"}), 400

    finally:
        conn.close()


@app.route("/password/request-reset", methods=["POST"])
def request_password_reset():
    data = request.json

    success_message = "該当するアカウントが存在する場合、再設定メールを送信しました。"

    if not data or "identifier" not in data:
        return jsonify({"message": success_message})

    identifier = data["identifier"]

    if not isinstance(identifier, str) or not identifier.strip():
        return jsonify({"message": success_message})

    identifier = identifier.strip()

    if re.search(r"\s", identifier):
        return jsonify({"message": success_message})

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ? OR email = ? LIMIT 1",
        (identifier, identifier)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": success_message})

    cursor.execute(
        "DELETE FROM password_reset_tokens WHERE user_id = ? AND used_at IS NULL",
        (user["id"],)
    )
    conn.commit()
    conn.close()

    token = create_password_reset_token(user["id"])
    if not token:
        return jsonify({"message": "再設定メールの送信に失敗しました。"}), 500

    reset_url = build_password_reset_url(token)

    try:
        send_password_reset_email(user["email"], reset_url)

    except Exception:
        logger.exception("[mail] failed to send password reset email")

        return jsonify({
            "message": "再設定メールの送信に失敗しました。"
        }), 500

    return jsonify({"message": success_message})


@app.route("/email-change/request", methods=["POST"])
def request_email_change():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    data = request.json

    if not data or "new_email" not in data or "current_password" not in data:
        return jsonify({"message": "不正なリクエスト"}), 400

    new_email = data["new_email"]
    current_password = data["current_password"]

    email_error = validate_email(new_email)
    if email_error:
        return jsonify({"message": email_error}), 400

    if not isinstance(current_password, str) or not current_password:
        return jsonify({"message": "現在のパスワードを入力してください。"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, display_name, email, password FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "ユーザーが存在しません"}), 404

    if not check_password_hash(user["password"], current_password):
        conn.close()
        return jsonify({"message": "現在のパスワードが正しくありません。"}), 400

    if new_email.lower() == user["email"].lower():
        conn.close()
        return jsonify({"message": "現在のメールアドレスとは異なるアドレスを入力してください。"}), 400

    cursor.execute(
        "SELECT 1 FROM users WHERE lower(email) = lower(?) AND id != ? LIMIT 1",
        (new_email, user_id)
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "このメールアドレスはすでに使われています。"}), 400

    window_start = (datetime.now() - timedelta(minutes=EMAIL_CHANGE_REQUEST_RATE_WINDOW_MINUTES)).isoformat(timespec="seconds")
    cursor.execute(
        "SELECT COUNT(*) AS count FROM email_change_tokens WHERE user_id = ? AND created_at >= ?",
        (user_id, window_start)
    )
    recent_requests = cursor.fetchone()["count"]

    if recent_requests >= EMAIL_CHANGE_REQUEST_RATE_LIMIT:
        conn.close()
        return jsonify({
            "message": "リクエストが多すぎます。しばらくしてから再試行してください。"
        }), 429

    cursor.execute(
        "DELETE FROM email_change_tokens WHERE user_id = ? AND used_at IS NULL",
        (user_id,)
    )
    conn.commit()
    conn.close()

    token = create_email_change_token(user_id, new_email)

    if not token:
        return jsonify({"message": "確認メールの作成に失敗しました。"}), 500

    confirm_url = build_email_change_confirm_url(token)

    try:
        send_email_change_confirmation(new_email, user["display_name"] or user["username"], confirm_url, EMAIL_CHANGE_TOKEN_LIFETIME_MINUTES)
    except Exception:
        logger.exception("[mail] failed to send email change confirmation")
        delete_email_change_token_by_raw_token(token)
        return jsonify({"message": "確認メールの送信に失敗しました。"}), 500

    return jsonify({
        "message": "確認メールを送信しました。メール内リンクを開いて変更を確定してください。"
    })


@app.route("/email-change/confirm", methods=["GET", "POST"])
def confirm_email_change():
    if request.method == "GET":
        token = request.args.get("token", "")
    else:
        data = request.json
        token = data.get("token", "") if isinstance(data, dict) else ""

    if not isinstance(token, str) or not token.strip() or re.search(r"\s", token):
        return jsonify({"message": "無効なリンクです。"}), 400

    token_hash = hash_secure_token(token)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, user_id, new_email, expires_at, used_at FROM email_change_tokens WHERE token_hash = ?",
        (token_hash,)
    )
    change_token = cursor.fetchone()

    if not change_token:
        conn.close()
        return jsonify({"message": "無効なリンクです。"}), 400

    if change_token["used_at"]:
        conn.close()
        return jsonify({"message": "このリンクはすでに使用されています。"}), 400

    try:
        expires_at = datetime.fromisoformat(change_token["expires_at"])
    except ValueError:
        conn.close()
        return jsonify({"message": "無効なリンクです。"}), 400

    if datetime.now() >= expires_at:
        conn.close()
        return jsonify({"message": "リンクの有効期限が切れています。"}), 400

    cursor.execute(
        "SELECT id FROM users WHERE lower(email) = lower(?) AND id != ? LIMIT 1",
        (change_token["new_email"], change_token["user_id"])
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "このメールアドレスはすでに使われています。"}), 400

    used_at = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (change_token["new_email"], change_token["user_id"])
    )

    cursor.execute(
        "UPDATE email_change_tokens SET used_at = ? WHERE id = ?",
        (used_at, change_token["id"])
    )

    cursor.execute(
        "DELETE FROM email_change_tokens WHERE user_id = ? AND used_at IS NULL",
        (change_token["user_id"],)
    )

    invalidate_user_auth_state(change_token["user_id"], cursor)

    conn.commit()
    conn.close()

    return jsonify({
        "message": "メールアドレスを変更しました。再ログインしてください。",
        "relogin_required": True
    })


@app.route("/password/reset/confirm", methods=["POST"])
def confirm_password_reset():
    data = request.json

    if not data or "token" not in data or "new_password" not in data:
        return jsonify({"message": "不正なリクエスト"}), 400

    token = data["token"]
    new_password = data["new_password"]

    if not isinstance(token, str) or not token.strip() or re.search(r"\s", token):
        return jsonify({"message": "不正なトークンです。"}), 400

    password_error = validate_password(new_password)
    if password_error:
        return jsonify({"message": password_error}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, user_id, expires_at, used_at FROM password_reset_tokens WHERE token = ?",
        (token,)
    )
    reset_token = cursor.fetchone()

    if not reset_token:
        conn.close()
        return jsonify({"message": "無効なリンクです。"}), 400

    if reset_token["used_at"]:
        conn.close()
        return jsonify({"message": "このリンクはすでに使用されています。"}), 400

    try:
        expires_at = datetime.fromisoformat(reset_token["expires_at"])
    except ValueError:
        conn.close()
        return jsonify({"message": "無効なリンクです。"}), 400

    if datetime.now() >= expires_at:
        conn.close()
        return jsonify({"message": "リンクの有効期限が切れています"}), 400

    hashed_password = generate_password_hash(new_password)
    cursor.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (hashed_password, reset_token["user_id"])
    )

    invalidate_user_auth_state(reset_token["user_id"], cursor)

    conn.commit()
    conn.close()

    return jsonify({
        "message": "パスワードを再設定しました。再ログインしてください。",
        "relogin_required": True
    })


@app.route("/password/change", methods=["POST"])
def change_password():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    if is_password_change_rate_limited(user_id):
        return jsonify({"message": "変更回数が多すぎます。しばらく待ってから再試行してください。"}), 429

    data = request.json

    if not data or "current_password" not in data or "new_password" not in data or "confirm_password" not in data:
        record_password_change_attempt(user_id)
        return jsonify({"message": "不正なリクエスト"}), 400

    current_password = data["current_password"]
    new_password = data["new_password"]
    confirm_password = data["confirm_password"]

    if not all(isinstance(value, str) for value in [current_password, new_password, confirm_password]):
        record_password_change_attempt(user_id)
        return jsonify({"message": "パスワードは文字列で入力してください。"}), 400

    if not current_password or not new_password or not confirm_password:
        record_password_change_attempt(user_id)
        return jsonify({"message": "パスワードを入力してください。"}), 400

    if current_password != current_password.strip() or new_password != new_password.strip() or confirm_password != confirm_password.strip():
        record_password_change_attempt(user_id)
        return jsonify({"message": "パスワードの前後に空白は使えません。"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        record_password_change_attempt(user_id)
        return jsonify({"message": "ユーザーが存在しません"}), 404

    if not check_password_hash(user["password"], current_password):
        conn.close()
        record_password_change_attempt(user_id)
        return jsonify({"message": "現在のパスワードが正しくありません。"}), 400

    password_error = validate_password(new_password)
    if password_error:
        conn.close()
        record_password_change_attempt(user_id)
        return jsonify({"message": password_error}), 400

    if new_password != confirm_password:
        conn.close()
        record_password_change_attempt(user_id)
        return jsonify({"message": "新しいパスワードが一致しません。"}), 400

    if check_password_hash(user["password"], new_password):
        conn.close()
        record_password_change_attempt(user_id)
        return jsonify({"message": "新しいパスワードは現在のパスワードと同じにできません。"}), 400

    hashed_password = generate_password_hash(new_password)
    updated_at = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (hashed_password, user_id)
    )

    conn.commit()
    conn.close()

    PASSWORD_CHANGE_ATTEMPTS.pop(user_id, None)

    logger.info("[password-change] user_id=%s password changed at %s", user_id, updated_at)

    return jsonify({
        "message": "パスワードを変更しました。ログイン状態は維持されています。",
        "relogin_required": False
    })

#ユーザーログイン
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "不正なリクエスト"}), 400

    identifier = data["username"]
    password = data["password"]

    if not isinstance(identifier, str) or not identifier.strip():
        return jsonify({"message": "ユーザー名またはメールアドレスを入力してください。"}), 400

    if not isinstance(password, str):
        return jsonify({"message": "ユーザー名またはパスワードが違います"}), 401

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? OR lower(email) = lower(?)",
        (identifier.strip(), identifier.strip())
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({
            "message": "ユーザー名またはパスワードが違います"
        }), 401

    if user["is_deleted"] == 1:
        return jsonify({
            "message": "このアカウントは削除されています。"
        }), 403

    if check_password_hash(user["password"], password):
        token = create_token_for_user(user["id"])

        if not token:
            return jsonify({"message": "トークン発行に失敗しました"}), 500

        return jsonify({
            "message": "ログイン成功",
            "token": token
        })

    return jsonify({
        "message": "ユーザー名またはパスワードが違います"
    }), 401


@app.route("/logout", methods=["POST"])
def logout():
    token = extract_bearer_token()

    if not token:
        return jsonify({"message": "認証が必要です"}), 401

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tokens WHERE token = ?",
        (token,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "ログアウトしました"})

#ユーザーアカウント削除
@app.route("/account/delete", methods=["POST"])
def delete_account():
    user_id, auth_error = get_current_user_id()

    if not user_id:
        return jsonify({"message": auth_error}), 401

    data = request.json
    if not isinstance(data, dict):
        return jsonify({"message": "不正なリクエスト"}), 400

    current_password = data.get("current_password")
    confirmation = data.get("confirmation")

    if not isinstance(current_password, str) or not current_password:
        return jsonify({"message": "現在のパスワードを入力してください。"}), 400

    if not isinstance(confirmation, str) or confirmation != "DELETE":
        return jsonify({"message": "確認文字列は DELETE と完全一致で入力してください。"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email, display_name, password, COALESCE(is_deleted, 0) AS is_deleted
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        conn.close()

        return jsonify({
            "message": "ユーザーが存在しません"
        }), 404

    if user["is_deleted"] == 1:
        conn.close()
        return jsonify({"message": "このアカウントはすでに削除済みです。"}), 400

    if not check_password_hash(user["password"], current_password):
        conn.close()
        return jsonify({"message": "現在のパスワードが正しくありません。"}), 400

    try:
        now = datetime.now()
        deleted_at = now.isoformat(timespec="seconds")
        suffix = now.strftime("%Y%m%d%H%M%S")

        archived_username = f"deleted_{user_id}_{user['username']}_{suffix}"
        archived_email = f"deleted_{user_id}_{user['email']}"
        archived_display_name = f"deleted_user_{user_id}"

        cursor.execute(
            """
            UPDATE users
            SET
                is_deleted = 1,
                deleted_at = ?,
                username = ?,
                email = ?,
                display_name = ?
            WHERE id = ?
            """,
            (
                deleted_at,
                archived_username,
                archived_email,
                archived_display_name,
                user_id
            )
        )

        invalidate_user_auth_state(user_id, cursor)

        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        logger.exception("[account-delete] failed to soft-delete user")
        return jsonify({"message": "アカウント削除に失敗しました。"}), 500

    conn.close()

    return jsonify({
        "message": "アカウントを削除しました。",
        "deleted": True,
        "relogin_required": True
    })

#サーバー起動時に必要な初期化処理をまとめて実行する関数
def setup_startup():
    os.makedirs(AVATAR_UPLOAD_DIR, exist_ok=True)

    init_db()
    logger.info("[startup] db initialized")

    migrate_db()
    logger.info("[startup] migration completed")

    reload_questions_cache()

#アプリ起動時の初期設定をまとめて実行する関数呼び出し
setup_startup()

#現在デバッグモードかどうかを判定するコード
DEBUG_MODE = os.getenv("FLASK_DEBUG") == "1"

#現在のデバッグモード状態をログ出力するコード
logger.info("[startup] debug mode: %s", DEBUG_MODE)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)