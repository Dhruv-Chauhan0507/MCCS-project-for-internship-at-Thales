from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from KEY_GENERATION.keygen.utils import build_key_metadata, log
import os

DEFAULT_DIR = os.path.join(os.path.dirname(__file__), "..", "keys", "rsa")

def generate_rsa_key_pair(key_size=2048, owner="admin", directory ="/KEY_GENERATION/keys"):
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()

    # Serialize keys to PEM
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Build metadata
    metadata = build_key_metadata(algorithm="RSA", owner=owner)
    key_id = metadata["key_id"]

    # Save keys
    import os
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/rsa_private_{key_id}.pem", "wb") as priv_file:
        priv_file.write(private_pem)
    with open(f"{directory}/rsa_public_{key_id}.pem", "wb") as pub_file:
        pub_file.write(public_pem)

    log(f"RSA key pair generated with ID {key_id}")
    return metadata

