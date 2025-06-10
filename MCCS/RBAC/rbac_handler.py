import sqlite3
from datetime import datetime
import bcrypt

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "VAULT", "DB", "vault.db")

DB_PATH = "VAULT/DB/vault.db"

# --- USER REGISTRATION ---
def register_user(username, password, role='User'):
    if role not in ['Admin', 'User', 'Auditor']:
        raise ValueError("Invalid role. Must be Admin, User, or Auditor.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Hash the password
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, created_at)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_pw, role, datetime.utcnow().isoformat()))
        conn.commit()
        print(f"[✓] User '{username}' registered with role '{role}'.")
    except sqlite3.IntegrityError:
        print("[!] Username already exists.")
    finally:
        conn.close()

# --- USER LOGIN ---
def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(password.encode(), result[0]):
        print(f"[✓] Login successful for user '{username}'.")
        return True
    else:
        print("[!] Invalid username or password.")
        return False

# --- GET ROLE ---
def get_user_role(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        print("[!] User not found.")
        return None

# --- ROLE CHECKER DECORATOR (Optional) ---
def require_role(required_role):
    def decorator(func):
        def wrapper(username, *args, **kwargs):
            role = get_user_role(username)
            if role == required_role:
                return func(username, *args, **kwargs)
            else:
                print(f"[!] Access denied: '{username}' does not have '{required_role}' privileges.")
        return wrapper
    return decorator

# --- PERMISSION CHECK ---
def check_permission(username, credential_id):
    """
    Checks if the given user has access to the credential.
    Admins have full access; others only to their own credentials.
    """
    role = get_user_role(username)
    if role == "Admin":
        return True  # Admins can access all

    # For other roles, verify ownership
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT owner_id FROM credentials WHERE id = ?", (credential_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        print("[!] Credential not found.")
        return False

    owner_id = result[0]
    return owner_id == username



