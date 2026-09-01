import sqlite3
import bcrypt
from datetime import datetime

DB_NAME = "bank.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            balance REAL DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            amount REAL,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                  (username, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_login(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[1]):
        return row[0]  # user_id
    return None

def get_balance(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = c.fetchone()[0]
    conn.close()
    return balance

def update_balance(user_id, new_balance):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))
    conn.commit()
    conn.close()

def add_transaction(user_id, t_type, amount):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO transactions (user_id, type, amount, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, t_type, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT type, amount, timestamp FROM transactions WHERE user_id=? ORDER BY id DESC",
              (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_id_by_username(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None