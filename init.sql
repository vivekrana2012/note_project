CREATE TABLE IF NOT EXISTS youtube (
    video_id      TEXT PRIMARY KEY,
    url           TEXT,
    title         TEXT,
    publish_date  TEXT,
    thumbnail     TEXT,
    keywords      TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);