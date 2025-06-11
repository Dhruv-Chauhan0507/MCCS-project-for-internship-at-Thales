import sqlite3

DB_PATH = 'VAULT/DB/vault.db'


def verify_tables(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables found in DB:")
    for table in tables:
        print(f" - {table[0]}")

    conn.close()


if __name__ == "__main__":
    verify_tables("vault.db")