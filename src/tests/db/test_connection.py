from pathlib import Path

import duckdb
import pytest

from src.db import connection

SCHEMA_PATH = Path(__file__).parent.parent.parent / "db" / "schema.sql"


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Point connection.DB_PATH at a throwaway db with the real schema applied."""
    db_path = tmp_path / "test.duckdb"
    schema_sql = SCHEMA_PATH.read_text()
    with duckdb.connect(str(db_path)) as conn:
        conn.execute(schema_sql)
    monkeypatch.setattr(connection, "DB_PATH", str(db_path))
    return db_path


def test_get_connection_can_write(temp_db):
    conn = connection.get_connection()
    try:
        conn.execute(
            "INSERT INTO feeds (feed_name, competitor) VALUES ('test-feed', 'Makita')"
        )
        rows = conn.execute("SELECT feed_name FROM feeds").fetchall()
        assert rows == [("test-feed",)]
    finally:
        conn.close()


def test_get_read_connection_rejects_writes(temp_db):
    conn = connection.get_read_connection()
    try:
        with pytest.raises(duckdb.Error):
            conn.execute(
                "INSERT INTO feeds (feed_name, competitor) VALUES ('test-feed', 'Makita')"
            )
    finally:
        conn.close()


def test_write_feed_then_read_feed_round_trip(temp_db):
    feed_data = [
        {
            "competitor": "Makita",
            "category": "accessories",
            "query": '"Makita" new power tool accessories',
            "extra_params": "{}",
        }
    ]

    write_conn = connection.get_connection()
    connection.write_feed(write_conn, "makita-feed", feed_data)
    write_conn.close()

    read_conn = connection.get_read_connection()
    rows = connection.read_feed(read_conn, "makita-feed")
    read_conn.close()

    assert len(rows) == 1
    assert rows[0]["competitor"] == "Makita"
