# SQLiteライブラリ読み込み
import sqlite3

#Pathlibを使ってDBファイルのパスを管理
from pathlib import Path

DB_PATH = Path("data/app.db")

#DB接続関数
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#アプリで必要なDBテーブルを全部作成する初期化関数
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        display_name TEXT UNIQUE NOT NULL
            CHECK (trim(display_name) <> '')
            CHECK (display_name = trim(display_name)),
        avatar_url TEXT,
        bio TEXT NOT NULL DEFAULT '',
        email TEXT UNIQUE NOT NULL
            CHECK (trim(email) <> '')
            CHECK (instr(email, '@') > 1)
            CHECK (email NOT GLOB '*[ \t\r\n]*'),
        password TEXT NOT NULL,
        created_at TEXT NOT NULL,
        is_deleted INTEGER NOT NULL DEFAULT 0,
        deleted_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answer_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        chapter INTEGER NOT NULL,
        difficulty INTEGER NOT NULL,
        is_correct INTEGER NOT NULL,
        submitted_code TEXT,
        actual_output TEXT,
        answered_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        question_snapshot TEXT,
        UNIQUE(user_id, question_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        used_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_change_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        new_email TEXT NOT NULL,
        token_hash TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        used_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        mode TEXT NOT NULL,
        review_mode INTEGER NOT NULL,
        question_ids TEXT NOT NULL,
        question_snapshot TEXT,
        current_question_index INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        answered_question_ids TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    create_indexes(cursor)

    conn.commit()
    conn.close()

#DB検索を高速化するindexを作る関数
def create_indexes(cursor):
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_answer_logs_user_id
    ON answer_logs(user_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_review_queue_user_id
    ON review_queue(user_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_tokens_token
    ON tokens(token)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_token
    ON password_reset_tokens(token)
    """)

    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_email_change_tokens_token_hash
    ON email_change_tokens(token_hash)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_email_change_tokens_user_id
    ON email_change_tokens(user_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_study_sessions_user_id
    ON study_sessions(user_id)
    """)

#指定したテーブルが存在するか確認する関数
def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,)
    )
    return cursor.fetchone() is not None

#指定したテーブルに必要なカラムが全て存在するか確認する関数
def table_has_columns(cursor, table_name, required_columns):
    if not table_exists(cursor, table_name):
        return False

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = {row["name"] for row in cursor.fetchall()}

    return required_columns.issubset(columns)


def get_table_columns(cursor, table_name):
    if not table_exists(cursor, table_name):
        return set()

    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row["name"] for row in cursor.fetchall()}


def foreign_key_targets(cursor, table_name):
    if not table_exists(cursor, table_name):
        return []

    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    return [row["table"] for row in cursor.fetchall()]


def table_references_users_correctly(cursor, table_name):
    targets = foreign_key_targets(cursor, table_name)

    # users を参照するFKが users 以外へ向いていれば再構築が必要
    for target in targets:
        if target.startswith("users") and target != "users":
            return False

    return True


def rebuild_table(cursor, table_name, create_sql, insert_sql):
    temp_old_name = f"{table_name}_old"

    if table_exists(cursor, temp_old_name):
        cursor.execute(f"DROP TABLE {temp_old_name}")

    cursor.execute(f"ALTER TABLE {table_name} RENAME TO {temp_old_name}")
    cursor.execute(create_sql)
    cursor.execute(insert_sql.format(old_table=temp_old_name))
    cursor.execute(f"DROP TABLE {temp_old_name}")


def create_tokens_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)


def create_answer_logs_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answer_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        chapter INTEGER NOT NULL,
        difficulty INTEGER NOT NULL,
        is_correct INTEGER NOT NULL,
        submitted_code TEXT,
        actual_output TEXT,
        answered_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)


def create_review_queue_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        question_snapshot TEXT,
        UNIQUE(user_id, question_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)


def create_study_sessions_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        mode TEXT NOT NULL,
        review_mode INTEGER NOT NULL,
        question_ids TEXT NOT NULL,
        question_snapshot TEXT,
        current_question_index INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        answered_question_ids TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)


def create_password_reset_tokens_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        used_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)


def create_email_change_tokens_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_change_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        new_email TEXT NOT NULL,
        token_hash TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        used_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

#既存DBを新しい構造へ更新する関数
def migrate_db():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.execute("PRAGMA foreign_keys = OFF")

        users_rebuilt = migrate_users_table(cursor)

        migrate_tokens_table(cursor, force_rebuild=users_rebuilt)
        migrate_answer_logs_table(cursor, force_rebuild=users_rebuilt)
        migrate_review_queue_table(cursor, force_rebuild=users_rebuilt)
        migrate_study_sessions_table(cursor, force_rebuild=users_rebuilt)
        migrate_password_reset_tokens_table(cursor, force_rebuild=users_rebuilt)
        migrate_email_change_tokens_table(cursor, force_rebuild=users_rebuilt)

        create_indexes(cursor)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.close()


def migrate_users_table(cursor):
    if not table_exists(cursor, "users"):
        return False

    column_names = get_table_columns(cursor, "users")

    if (
        "email" in column_names
        and "created_at" in column_names
        and "display_name" in column_names
        and "avatar_url" in column_names
        and "bio" in column_names
        and "is_deleted" in column_names
        and "deleted_at" in column_names
    ):
        return False

    created_at_select = (
        "COALESCE(u.created_at, REPLACE(datetime('now'), ' ', 'T'))"
        if "created_at" in column_names
        else "REPLACE(datetime('now'), ' ', 'T')"
    )

    display_name_select = (
        "COALESCE(NULLIF(trim(u.display_name), ''), u.username)"
        if "display_name" in column_names
        else "u.username"
    )

    avatar_url_select = (
        "NULLIF(trim(u.avatar_url), '')"
        if "avatar_url" in column_names
        else "NULL"
    )

    bio_select = (
        "COALESCE(trim(u.bio), '')"
        if "bio" in column_names
        else "''"
    )

    is_deleted_select = (
        "CASE WHEN COALESCE(u.is_deleted, 0) = 1 THEN 1 ELSE 0 END"
        if "is_deleted" in column_names
        else "0"
    )

    deleted_at_select = (
        "u.deleted_at"
        if "deleted_at" in column_names
        else "NULL"
    )

    rebuild_table(
        cursor,
        table_name="users",
        create_sql="""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        display_name TEXT UNIQUE NOT NULL
            CHECK (trim(display_name) <> '')
            CHECK (display_name = trim(display_name)),
        avatar_url TEXT,
        bio TEXT NOT NULL DEFAULT '',
        email TEXT UNIQUE NOT NULL
            CHECK (trim(email) <> '')
            CHECK (instr(email, '@') > 1)
            CHECK (email NOT GLOB '*[ \t\r\n]*'),
        password TEXT NOT NULL,
        created_at TEXT NOT NULL,
        is_deleted INTEGER NOT NULL DEFAULT 0,
        deleted_at TEXT
    )
    """,
        insert_sql=f"""
    INSERT INTO users (id, username, display_name, avatar_url, bio, email, password, created_at, is_deleted, deleted_at)
    SELECT
        u.id,
        u.username,
        {display_name_select} AS display_name,
        {avatar_url_select} AS avatar_url,
        {bio_select} AS bio,
        CASE
            WHEN trim(COALESCE(u.email, '')) = '' THEN LOWER(u.username || '@local.invalid')
            ELSE u.email
        END AS email,
        u.password,
        {created_at_select} AS created_at,
        {is_deleted_select} AS is_deleted,
        {deleted_at_select} AS deleted_at
    FROM {{old_table}} u
    """
    )

    return True


def migrate_answer_logs_table(cursor, force_rebuild=False):
    required_columns = {
        "id",
        "user_id",
        "question_id",
        "chapter",
        "difficulty",
        "is_correct",
        "submitted_code",
        "actual_output",
        "answered_at"
    }

    if not table_exists(cursor, "answer_logs"):
        create_answer_logs_table(cursor)
        return

    columns_ok = required_columns.issubset(get_table_columns(cursor, "answer_logs"))
    fk_ok = table_references_users_correctly(cursor, "answer_logs")

    if columns_ok and fk_ok and not force_rebuild:
        return

    rebuild_table(
        cursor,
        table_name="answer_logs",
        create_sql="""
    CREATE TABLE answer_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        chapter INTEGER NOT NULL,
        difficulty INTEGER NOT NULL,
        is_correct INTEGER NOT NULL,
        submitted_code TEXT,
        actual_output TEXT,
        answered_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """,
        insert_sql="""
    INSERT INTO answer_logs (
        id, user_id, question_id, chapter, difficulty,
        is_correct, submitted_code, actual_output, answered_at
    )
    SELECT
        a.id, a.user_id, a.question_id, a.chapter, a.difficulty,
        a.is_correct, a.submitted_code, a.actual_output, a.answered_at
    FROM {old_table} a
    INNER JOIN users u ON u.id = a.user_id
    """
    )


def migrate_review_queue_table(cursor, force_rebuild=False):
    required_columns = {
        "id",
        "user_id",
        "question_id",
        "question_snapshot"
    }

    if not table_exists(cursor, "review_queue"):
        create_review_queue_table(cursor)
        return

    columns_ok = required_columns.issubset(get_table_columns(cursor, "review_queue"))
    fk_ok = table_references_users_correctly(cursor, "review_queue")

    if columns_ok and fk_ok and not force_rebuild:
        return

    rebuild_table(
        cursor,
        table_name="review_queue",
        create_sql="""
    CREATE TABLE review_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        question_snapshot TEXT,
        UNIQUE(user_id, question_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """,
        insert_sql="""
    INSERT INTO review_queue (id, user_id, question_id)
    SELECT
        MIN(r.id) AS id,
        r.user_id,
        r.question_id
    FROM {old_table} r
    INNER JOIN users u ON u.id = r.user_id
    GROUP BY r.user_id, r.question_id
    """
    )


def migrate_tokens_table(cursor, force_rebuild=False):
    required_columns = {
        "id",
        "user_id",
        "token",
        "created_at",
        "expires_at"
    }

    if not table_exists(cursor, "tokens"):
        create_tokens_table(cursor)
        return

    columns = get_table_columns(cursor, "tokens")
    columns_ok = required_columns.issubset(columns)
    fk_ok = table_references_users_correctly(cursor, "tokens")

    if columns_ok and fk_ok and not force_rebuild:
        return

    rebuild_table(
        cursor,
        table_name="tokens",
        create_sql="""
    CREATE TABLE tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """,
        insert_sql="""
    INSERT INTO tokens (id, user_id, token, created_at, expires_at)
    SELECT
        t.id,
        t.user_id,
        t.token,
        t.created_at,
        COALESCE(
            t.expires_at,
            REPLACE(datetime(t.created_at, '+7 days'), ' ', 'T'),
            datetime('now', '+7 days')
        ) AS expires_at
    FROM {old_table} t
    INNER JOIN users u ON u.id = t.user_id
    """
    )


def migrate_study_sessions_table(cursor, force_rebuild=False):
    required_columns = {
        "id",
        "user_id",
        "chapter",
        "mode",
        "review_mode",
        "question_ids",
        "question_snapshot",
        "current_question_index",
        "correct_count",
        "answered_question_ids",
        "updated_at"
    }

    if not table_exists(cursor, "study_sessions"):
        create_study_sessions_table(cursor)
        return

    column_names = get_table_columns(cursor, "study_sessions")
    columns_ok = required_columns.issubset(column_names)
    fk_ok = table_references_users_correctly(cursor, "study_sessions")

    if columns_ok and fk_ok and not force_rebuild:
        return

    question_snapshot_select = (
        "s.question_snapshot"
        if "question_snapshot" in column_names
        else "NULL"
    )

    rebuild_table(
        cursor,
        table_name="study_sessions",
        create_sql="""
    CREATE TABLE study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        mode TEXT NOT NULL,
        review_mode INTEGER NOT NULL,
        question_ids TEXT NOT NULL,
        question_snapshot TEXT,
        current_question_index INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        answered_question_ids TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """,
        insert_sql="""
    INSERT INTO study_sessions (
        id, user_id, chapter, mode, review_mode,
        question_ids, question_snapshot, current_question_index, correct_count,
        answered_question_ids, updated_at
    )
    SELECT
        s.id, s.user_id, s.chapter, s.mode, s.review_mode,
        s.question_ids, {question_snapshot_select}, s.current_question_index, s.correct_count,
        s.answered_question_ids, s.updated_at
    FROM {{old_table}} s
    INNER JOIN users u ON u.id = s.user_id
    """.format(question_snapshot_select=question_snapshot_select)
    )


def migrate_password_reset_tokens_table(cursor, force_rebuild=False):
    required_columns = {
        "id",
        "user_id",
        "token",
        "expires_at",
        "created_at",
        "used_at"
    }

    if not table_exists(cursor, "password_reset_tokens"):
        create_password_reset_tokens_table(cursor)
        return

    columns_ok = required_columns.issubset(get_table_columns(cursor, "password_reset_tokens"))
    fk_ok = table_references_users_correctly(cursor, "password_reset_tokens")

    if columns_ok and fk_ok and not force_rebuild:
        return

    rebuild_table(
        cursor,
        table_name="password_reset_tokens",
        create_sql="""
    CREATE TABLE password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        used_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """,
        insert_sql="""
    INSERT INTO password_reset_tokens (
        id, user_id, token, expires_at, created_at, used_at
    )
    SELECT
        p.id, p.user_id, p.token, p.expires_at, p.created_at, p.used_at
    FROM {old_table} p
    INNER JOIN users u ON u.id = p.user_id
    """
    )


def migrate_email_change_tokens_table(cursor, force_rebuild=False):
    required_columns = {
        "id",
        "user_id",
        "new_email",
        "token_hash",
        "expires_at",
        "created_at",
        "used_at"
    }

    if not table_exists(cursor, "email_change_tokens"):
        create_email_change_tokens_table(cursor)
        return

    columns_ok = required_columns.issubset(get_table_columns(cursor, "email_change_tokens"))
    fk_ok = table_references_users_correctly(cursor, "email_change_tokens")

    if columns_ok and fk_ok and not force_rebuild:
        return

    rebuild_table(
        cursor,
        table_name="email_change_tokens",
        create_sql="""
    CREATE TABLE email_change_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        new_email TEXT NOT NULL,
        token_hash TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        used_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """,
        insert_sql="""
    INSERT INTO email_change_tokens (
        id, user_id, new_email, token_hash, expires_at, created_at, used_at
    )
    SELECT
        e.id, e.user_id, e.new_email, e.token_hash, e.expires_at, e.created_at, e.used_at
    FROM {old_table} e
    INNER JOIN users u ON u.id = e.user_id
    """
    )