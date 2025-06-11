import sqlite3
from datetime import datetime
from VAULT.utils_vault import encrypt_data, decrypt_data
from RBAC.rbac_handler import check_permission
from config import DB_PATH

# --- STORE CREDENTIAL ---
def store_credential(username, cred_name, plain_password, metadata=None):
    if not check_permission(username, "store_credential"):
        print("[!] Access denied: insufficient permissions.")
        return

    encrypted_pw = encrypt_data(plain_password)
    created_at = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO credentials (name, password_enc, owner, created_at, metadata, access_count, last_used)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cred_name, encrypted_pw, username, created_at, str(metadata), 0, None))
        conn.commit()
        print(f"[✓] Credential '{cred_name}' stored successfully.")
    except Exception as e:
        print("[!] Error storing credential:", str(e))
    finally:
        conn.close()

# --- GET CREDENTIAL ---
def get_credential(username, cred_id):
    if not check_permission(username, "get_credential"):
        print("[!] Access denied: insufficient permissions.")
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT name, password_enc, owner, access_count FROM credentials WHERE id = ?', (cred_id,))
        row = cursor.fetchone()

        if row:
            name, enc_pw, owner, count = row

            if owner != username:
                print("[!] Unauthorized: credential does not belong to user.")
                return None

            decrypted_pw = decrypt_data(enc_pw)

            # Update usage metadata
            cursor.execute('''
                UPDATE credentials SET last_used = ?, access_count = ? WHERE id = ?
            ''', (datetime.utcnow().isoformat(), count + 1, cred_id))
            conn.commit()

            return {"name": name, "password": decrypted_pw}
        else:
            print("[!] Credential not found.")
            return None

    except Exception as e:
        print("[!] Error retrieving credential:", str(e))
        return None
    finally:
        conn.close()

# --- DELETE CREDENTIAL ---
def delete_credential(username, cred_id):
    if not check_permission(username, "delete_credential"):
        print("[!] Access denied: insufficient permissions.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT owner FROM credentials WHERE id = ?', (cred_id,))
        row = cursor.fetchone()

        if row and row[0] == username:
            cursor.execute('DELETE FROM credentials WHERE id = ?', (cred_id,))
            conn.commit()
            print(f"[✓] Credential ID {cred_id} deleted.")
        else:
            print("[!] Credential not found or not owned by user.")
    finally:
        conn.close()

# --- LIST CREDENTIALS (User's Only) ---
def list_credentials(username):
    if not check_permission(username, "list_credentials"):
        print("[!] Access denied: insufficient permissions.")
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id, name, created_at, last_used FROM credentials WHERE owner = ?', (username,))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print("[!] Error listing credentials:", str(e))
        return []
    finally:
        conn.close()

# --- UPDATE CREDENTIAL ---
def update_credential(username, cred_id, new_name=None, new_password=None, new_metadata=None):
    if not check_permission(username, "update_credential"):
        print("[!] Access denied: insufficient permissions.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verify ownership
        cursor.execute('SELECT owner FROM credentials WHERE id = ?', (cred_id,))
        row = cursor.fetchone()

        if not row:
            print("[!] Credential not found.")
            return
        if row[0] != username:
            print("[!] Unauthorized: credential does not belong to user.")
            return

        updates = []
        values = []

        if new_name:
            updates.append("name = ?")
            values.append(new_name)

        if new_password:
            encrypted_pw = encrypt_data(new_password)
            updates.append("password_enc = ?")
            values.append(encrypted_pw)

        if new_metadata is not None:
            updates.append("metadata = ?")
            values.append(str(new_metadata))

        if not updates:
            print("[!] No updates provided.")
            return

        # Always update last_used if something is modified
        updates.append("last_used = ?")
        values.append(datetime.utcnow().isoformat())

        values.append(cred_id)

        update_query = f"UPDATE credentials SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(update_query, values)
        conn.commit()
        print(f"[✓] Credential ID {cred_id} updated successfully.")

    except Exception as e:
        print("[!] Error updating credential:", str(e))
    finally:
        conn.close()
