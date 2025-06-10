from cryptography.fernet import Fernet
from datetime import datetime

# Sample static key (Replace this for actual use — store securely!)
FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

def encrypt_data(data: bytes) -> bytes:
    return fernet.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    return fernet.decrypt(token)

def build_key_metadata(key_type, owner, usage):
    return {
        "key_type": key_type,
        "owner": owner,
        "usage": usage,
        "created_at": datetime.utcnow().isoformat()
    }