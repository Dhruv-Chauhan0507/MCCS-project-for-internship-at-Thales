import sqlite3
import os

DB_PATH = "VAULT/DB/vault.db"

def initialize_vault_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Ensure DB directory exists

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the vault_keys table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_type TEXT NOT NULL,
            key_data BLOB NOT NULL,
            owner TEXT NOT NULL,
            usage TEXT,
            created_at TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()
    print("[✓] Vault database initialized successfully at", DB_PATH)


def initialize_credentials_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password_enc TEXT NOT NULL,
            owner TEXT NOT NULL,
            created_at TEXT,
            last_used TEXT,
            access_count INTEGER,
            metadata TEXT,
            rotation_flag BOOLEAN DEFAULT 0
        );
    ''')

    conn.commit()
    conn.close()
    print("[✓] credentials table initialized.")

if __name__ == '__main__:':
    initialize_credentials_table()
    initialize_vault_db()
