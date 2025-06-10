from KEY_GENERATION.keygen.rsa_keygen import generate_rsa_key_pair
from KEY_GENERATION.keygen.aes_keygen import generate_aes_key
from KEY_GENERATION.keygen.utils import log


def main():
    log("🚀 Starting Key Generation Test")

    try:
        rsa_metadata = generate_rsa_key_pair(
            key_size=2048,
            owner="admin",
            directory="/Users/dhruvchauhan/PycharmProjects/MCCS/KEY_GENERATION/keys/rsa"
        )
        log(f"🔐 RSA Key Metadata: {rsa_metadata}")
    except Exception as e:
        log(f"❌ RSA Key Generation Failed: {e}")

    try:
        aes_metadata = generate_aes_key(
            key_size=256,
            owner="admin",
            directory="/Users/dhruvchauhan/PycharmProjects/MCCS/KEY_GENERATION/keys/aes"
        )
        log(f"🔐 AES Key Metadata: {aes_metadata}")
    except Exception as e:
        log(f"❌ AES Key Generation Failed: {e}")

    log("✅ Key Generation Test Completed")

if __name__ == "__main__":
    main()
