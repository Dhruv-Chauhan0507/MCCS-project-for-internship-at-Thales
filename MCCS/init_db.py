from VAULT.vault.DB_init import init_vault_db
from RBAC.init_rbac_db import init_rbac_db


def initialize_all_databases():
    print("[-] Initializing databases...")
    init_vault_db()
    init_rbac_db()
    print("[✓] All databases initialized successfully.")
