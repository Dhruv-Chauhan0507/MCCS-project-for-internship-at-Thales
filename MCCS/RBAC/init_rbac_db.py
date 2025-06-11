import os
import sqlite3
from config import DB_PATH

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "VAULT", "DB", "vault.db")

def init_rbac_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL
        )


    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')



    conn.commit()
    conn.close()
    print("[✓] RBAC tables initialized in Vault DB")
