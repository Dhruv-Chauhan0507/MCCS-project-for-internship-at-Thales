-- Table to store vault users and their roles
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'User', 'Auditor')),
    created_at TEXT NOT NULL
);


-- Table to store keys metadata and encrypted key data
CREATE TABLE IF NOT EXISTS keys (
    key_id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT NOT NULL,
    key_type TEXT NOT NULL,       -- 'AES' or 'RSA'
    algorithm TEXT NOT NULL,      -- 'AES-256', 'RSA-2048'
    key_size INTEGER NOT NULL,
    owner TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    encrypted_key BLOB NOT NULL,
    metadata TEXT,                -- optional JSON string for additional info
    FOREIGN KEY (owner) REFERENCES users(username)
);

-- Table to store access logs
CREATE TABLE IF NOT EXISTS access_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    key_id INTEGER,
    action TEXT NOT NULL,         -- 'CREATE', 'READ', 'DELETE', etc.
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT,                  -- 'SUCCESS', 'FAILED', etc.
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (key_id) REFERENCES keys(key_id)
);


CREATE TABLE IF NOT EXISTS credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password_enc TEXT NOT NULL,
    owner TEXT NOT NULL,
    created_at TEXT,
    last_used TEXT,
    access_count INTEGER,
    metadata TEXT,
    rotation_flag BOOLEAN DEFAULT 0
);


-- Table 1: Roles
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

-- Table 2: Users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);
