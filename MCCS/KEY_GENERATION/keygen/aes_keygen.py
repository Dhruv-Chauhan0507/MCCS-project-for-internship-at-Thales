import os
from cryptography.hazmat.primitives.ciphers import algorithms
from KEY_GENERATION.keygen.utils import build_key_metadata, log
DEFAULT_DIR = os.path.join(os.path.dirname(__file__), "..", "keys", "rsa")

def generate_aes_key(key_size=256, owner="admin", directory="/KEY_GENERATION/keys"):
    if key_size not in [128, 192, 256]:
        raise ValueError("AES key size must be 128, 192, or 256 bits")

    # Generate random AES key
    key = os.urandom(32)  # Convert bits to bytes
    cipher = algorithms.AES(key)

    # Build metadata
    metadata = build_key_metadata(algorithm=f"AES-{key_size}", owner=owner)
    key_id = metadata["key_id"]

    # Save key to file
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/aes_key_{key_id}.bin", "wb") as key_file:
        key_file.write(key)

    log(f"AES-{key_size} key generated with ID {key_id}")
    return metadata
