import sqlite3

DB_NAME = "database.db"


def get_db_connection():
    """Return a sqlite3 connection with row access by column name."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _column_exists(conn, table, column):
    cols = [row["name"] for row in conn.execute(f"PRAGMA table_info({table})")]
    return column in cols


def init_db():
    """Create tables if they don't already exist, and migrate older DBs safely."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            subscription TEXT NOT NULL DEFAULT 'Free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL DEFAULT 'event',
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    # --- Lightweight migration for databases created before these columns existed ---
    if not _column_exists(conn, "users", "subscription"):
        cur.execute("ALTER TABLE users ADD COLUMN subscription TEXT NOT NULL DEFAULT 'Free'")

    if not _column_exists(conn, "bookings", "category"):
        cur.execute("ALTER TABLE bookings ADD COLUMN category TEXT NOT NULL DEFAULT 'event'")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")