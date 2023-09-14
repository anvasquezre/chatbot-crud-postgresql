CREATE TABLE IF NOT EXISTS sessions (
    session_id CHAR(36) PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ended_at TIMESTAMP WITH TIME ZONE,
    user_email TEXT,
    user_name TEXT,
    user_role TEXT,
    data_use_consent BOOLEAN NOT NULL,
);

CREATE TABLE IF NOT EXISTS messages (
    message_id CHAR(36) PRIMARY KEY UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    exchange TEXT NOT NULL,
    message_type CHAR(1) NOT NULL,
    session_id CHAR(36),
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

