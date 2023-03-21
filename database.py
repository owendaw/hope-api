from pymysql import connect
from pymysql.cursors import DictCursor
from sqlitedict import SqliteDict

user = "hydrostation_api"
password = ""
# host = "hydrostation-public-db-1.canw8fprhd3c.us-east-1.rds.amazonaws.com"
host = "hydrostation-private-db-1.canw8fprhd3c.us-east-1.rds.amazonaws.com"

port = 3306
database = "hydrostation"

connection = connect(host=host,
                     port=port,
                     user=user,
                     password=password,
                     database=database,
                     cursorclass=DictCursor)

total_db = SqliteDict("data_store/local_db", autocommit=True, tablename="total_db")
station_db = SqliteDict("data_store/station_db", autocommit=True, tablename="station_db")

# init total_db
if "total_count" not in total_db:
    total_db["total_count"] = 0
