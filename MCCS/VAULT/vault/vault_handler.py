import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime
from VAULT.utils_vault import encrypt_data, decrypt_data, build_key_metadata
from config import DB_PATH





# Store key with metadata in Vault
def store_key_in_vault(key_type, key_bytes, owner, usage):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    encrypted_key = encrypt_data(key_bytes)
    metadata = build_key_metadata(key_type, owner, usage)

    cursor.execute('''
        INSERT INTO vault_keys (key_type, key_data, owner, usage, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        key_type,
        encrypted_key,
        owner,
        usage,
        metadata["created_at"]
    ))

    conn.commit()
    conn.close()
    print(f"[✓] Stored {key_type} key in vault for owner '{owner}'.")

# Retrieve key by ID or owner
def retrieve_key_from_vault(key_id=None, owner=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if key_id:
        cursor.execute("SELECT key_data FROM vault_keys WHERE id = ?", (key_id,))
    elif owner:
        cursor.execute("SELECT key_data FROM vault_keys WHERE owner = ?", (owner,))
    else:
        raise ValueError("Must provide either key_id or owner.")

    result = cursor.fetchone()
    conn.close()

    if result:
        return decrypt_data(result[0])
    else:
        print("[!] Key not found.")
        return None

# Delete key by ID
def delete_key_from_vault(key_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM vault_keys WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()

    print(f"[✗] Key with ID {key_id} deleted from vault.")


