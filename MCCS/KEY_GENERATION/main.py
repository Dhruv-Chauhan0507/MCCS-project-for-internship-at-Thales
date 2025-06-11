from KEY_GENERATION.keygen.rsa_keygen import generate_rsa_key_pair
from KEY_GENERATION.keygen.aes_keygen import generate_aes_key
from KEY_GENERATION.keygen.utils import log
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RSA_DIR = BASE_DIR / "KEY_GENERATION" / "keys" / "rsa"
AES_DIR = BASE_DIR / "KEY_GENERATION" / "keys" / "aes"


def main():
    log("🚀 Starting Key Generation Test")

    try:
        rsa_metadata = generate_rsa_key_pair(
            key_size=2048,
            owner="admin",
            directory=str(RSA_DIR)
        )
        log(f"🔐 RSA Key Metadata: {rsa_metadata}")
    except Exception as e:
        log(f"❌ RSA Key Generation Failed: {e}")

    try:
        aes_metadata = generate_aes_key(
            key_size=256,
            owner="admin",
            directory=str(AES_DIR)
        )
        log(f"🔐 AES Key Metadata: {aes_metadata}")
    except Exception as e:
        log(f"❌ AES Key Generation Failed: {e}")

    log("✅ Key Generation Test Completed")

if __name__ == "__main__":
    main()
