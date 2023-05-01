import aiomysql
from sqlitedict import SqliteDict
from contextlib import asynccontextmanager
from aiomysql import DictCursor


@asynccontextmanager
async def get_connection():
    user = "hydrostation-api"
    password = ""
    host = "hydrostation-private-db-1.canw8fprhd3c.us-east-1.rds.amazonaws.com"
    port = 3306
    database = "hydrostation"

    conn = await aiomysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        db=database,
        autocommit=True,
        cursorclass=DictCursor
    )

    try:
        yield conn
    finally:
        conn.close()


total_db = SqliteDict("data_store/local_db", autocommit=True, tablename="total_db")
station_db = SqliteDict("data_store/station_db", autocommit=True, tablename="station_db")

# init total_db
if "total_count" not in total_db:
    total_db["total_count"] = 0
