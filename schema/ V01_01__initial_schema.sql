CREATE TABLE IF NOT EXISTS chat_bot_context (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name_ varchar(255),
    role_ varchar(255) NOT NULL,
    content text NOT NULL,
    created_at timestamp NOT NULL
)