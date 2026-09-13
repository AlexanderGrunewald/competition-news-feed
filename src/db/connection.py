import duckdb as db
from typing import Optional, Any, List

DB_PATH = "data/database/newsFeed.duckdb"
def get_connection(**kwargs: Optional[Any]) -> db.DuckDBPyConnection:
    return db.connect(DB_PATH, read_only=False, config=kwargs)

def get_read_connection(**kwargs: Optional[Any]) -> db.DuckDBPyConnection:
    return db.connect(DB_PATH, read_only=True, config=kwargs)
