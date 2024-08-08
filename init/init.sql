CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    hash TEXT NOT NULL,
    table_id SMALLINT NOT NULL,
    sit_id SMALLINT NOT NULL,
    price INT NOT NULL,
    scans INT DEFAULT 0
);