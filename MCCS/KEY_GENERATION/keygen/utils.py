# imports
import uuid
from datetime import datetime

# key id generation


def generate_key_id():
    """Generate a UUID string to be used as a key ID."""
    return str(uuid.uuid4())

# utc timestamp


def get_utc_timestamp():
    """Return the current UTC timestamp as an ISO string."""
    return datetime.utcnow().isoformat()

# key meta data


def build_key_metadata(algorithm: str, owner: str = "admin") -> dict:
    """Create a metadata dictionary for keys."""
    return {
        "key_id": generate_key_id(),
        "algorithm": algorithm,
        "owner": owner,
        "created_at": get_utc_timestamp()
    }

# logging


def log(message: str):
    """Basic timestamped logger for dev use."""
    print(f"[{get_utc_timestamp()}] {message}")
