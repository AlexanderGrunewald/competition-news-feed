-- DuckDB schema for the competitor news feed database.
-- Run via `pixi run init-db` (also runs automatically before `pixi run start`).
-- Idempotent: safe to re-run against an existing database.

CREATE SEQUENCE IF NOT EXISTS seq_feed_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_run_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_article_id START 1;

-- A saved feed configuration (from the Create Feed page).
CREATE TABLE IF NOT EXISTS feeds (
    id           INTEGER PRIMARY KEY DEFAULT nextval('seq_feed_id'),
    feed_name    VARCHAR NOT NULL,
    competitor   VARCHAR NOT NULL,
    category     VARCHAR,
    query        VARCHAR,
    extra_params JSON,
    created_at   TIMESTAMP DEFAULT current_timestamp
);

-- One row per time a feed is executed against Tavily.
CREATE TABLE IF NOT EXISTS runs (
    id           INTEGER PRIMARY KEY DEFAULT nextval('seq_run_id'),
    feed_id      INTEGER NOT NULL REFERENCES feeds(id),
    executed_at  TIMESTAMP DEFAULT current_timestamp,
    result_count INTEGER
);

-- Unique articles, deduped by URL across runs and feeds.
CREATE TABLE IF NOT EXISTS articles (
    id             INTEGER PRIMARY KEY DEFAULT nextval('seq_article_id'),
    url            VARCHAR NOT NULL UNIQUE,
    title          VARCHAR,
    content        VARCHAR,
    raw_content    VARCHAR,
    published_date VARCHAR,
    first_seen_at  TIMESTAMP DEFAULT current_timestamp
);

-- Which articles showed up in which run, and with what relevance score.
CREATE TABLE IF NOT EXISTS run_articles (
    run_id     INTEGER NOT NULL REFERENCES runs(id),
    article_id INTEGER NOT NULL REFERENCES articles(id),
    score      DOUBLE,
    PRIMARY KEY (run_id, article_id)
);
