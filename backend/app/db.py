import sqlite3
from datetime import datetime
from .models import CommentIn

DB_PATH = "./smokefree.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nick TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def get_comments():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nick, content, created_at FROM comments ORDER BY id DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "nick": r[1], "content": r[2], "created_at": r[3]} for r in rows]

def add_comment(comment: CommentIn):
    now = datetime.utcnow().isoformat() + "Z"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO comments (nick, content, created_at) VALUES (?, ?, ?)", (comment.nick, comment.content, now))
    conn.commit()
    rowid = c.lastrowid
    conn.close()
    return {"id": rowid, "nick": comment.nick, "content": comment.content, "created_at": now}
