import duckdb as db
from typing import Optional, Any, List

DB_PATH = "data/database/newsFeed.duckdb"
def get_connection(**kwargs: Optional[Any]) -> db.DuckDBPyConnection:
    return db.connect(DB_PATH, read_only=False, config=kwargs)

def get_read_connection(**kwargs: Optional[Any]) -> db.DuckDBPyConnection:
    return db.connect(DB_PATH, read_only=True, config=kwargs)

def read_feed(conn: db.DuckDBPyConnection, feed_name: str) -> List[dict]:
    query = f"SELECT * FROM feeds WHERE feed_name = '{feed_name}'"
    result = conn.execute(query).fetch_df()  # Use 'records' to get a list of dicts
    return result.to_dict(orient="records")

def write_feed(
    conn: db.DuckDBPyConnection, 
    feed_name: str, 
    feed_data: List[dict],
) -> None:
    required_keys = {
        "id",
        "competitor",
        "category",
        "query",
        "extra_params",
        "created_at",
    }
    
    error_msg = (
        "Each feed item must contain: "
        "'id', 'competitor', 'category', "
        "'query', 'extra_params', and 'created_at'."
    )

    if not all(required_keys.issubset(item) for item in feed_data):
        raise ValueError(error_msg)

    feed_tuples = [
        (
            feed_name,
            item["id"],
            item["competitor"],
            item["category"],
            item["query"],
            item["extra_params"],
            item["created_at"],
        )
        for item in feed_data
    ]
    conn.executemany(
        "INSERT INTO feeds (feed_name, id, competitor, category, query, extra_params, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        feed_tuples,
    )
