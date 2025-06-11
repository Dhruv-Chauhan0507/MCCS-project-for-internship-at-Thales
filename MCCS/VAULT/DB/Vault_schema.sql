-- VAULT schema

CREATE TABLE IF NOT EXISTS keys (
    key_id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT NOT NULL,
    key_type TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    key_size INTEGER NOT NULL,
    owner INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    encrypted_key BLOB NOT NULL,
    metadata TEXT,
    FOREIGN KEY (owner) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS access_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    key_id INTEGER,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (key_id) REFERENCES keys(key_id)
);

CREATE TABLE IF NOT EXISTS credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password_enc TEXT NOT NULL,
    owner INTEGER NOT NULL,
    created_at TEXT,
    last_used TEXT,
    access_count INTEGER,
    metadata TEXT,
    rotation_flag BOOLEAN DEFAULT 0,
    FOREIGN KEY (owner) REFERENCES users(id)
);

