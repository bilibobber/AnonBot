CREATE TABLE IF NOT EXISTS correspondence (
    user_id BIGINT NOT NULL PRIMARY KEY,
    user_name VARCHAR(33),
    correspondence JSONB DEFAULT '[]'::jsonb,
    is_admin BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS admins (
    user_id BIGINT NOT NULL PRIMARY KEY ,
    user_name VARCHAR(33)
);