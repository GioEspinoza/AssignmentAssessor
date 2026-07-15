CREATE TABLE IF NOT EXISTS users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(320) NOT NULL UNIQUE,
    password_hash BYTEA NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    task_name VARCHAR(255) NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    estimated_hours NUMERIC(8, 2),
    hours_used NUMERIC(8, 2),
    completion_status BOOLEAN NOT NULL DEFAULT FALSE,
    difficulty_level SMALLINT NOT NULL CHECK (difficulty_level BETWEEN 1 AND 5),
    due_date VARCHAR(10),
    date_completed VARCHAR(10),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (
            completion_status
            AND hours_used IS NOT NULL
            AND date_completed IS NOT NULL
        )
        OR (
            NOT completion_status
            AND estimated_hours IS NOT NULL
            AND due_date IS NOT NULL
        )
    )
);

CREATE INDEX IF NOT EXISTS tasks_user_id_idx ON tasks(user_id);
