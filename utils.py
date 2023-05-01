import logging
from database import total_db, station_db


async def fetch_stations(conn):
    print("Fetching All Stations...")
    async with conn.cursor() as cursor:
        sql_string = "SELECT stationId, piSerial FROM hydrostations"
        await cursor.execute(sql_string)
        result = await cursor.fetchall()

    print("Success")
    print("Adding Stations to station_db...")

    for station in result:
        station_id = station["stationId"]
        # If there is a new station, add it to our total_db
        if station_id not in total_db:
            print(f"[New station detected. Station {station_id}]")
            total_db[station_id] = 0

        station_db[station["piSerial"]] = station_id

    print(station_db)
    print("Success")

    return


async def update_count(payload: dict):
    try:
        total_db["total_count"] += payload["quantity"]
        station_id = station_db[payload["piSerial"]]
        total_db[station_id] += payload["quantity"]
    except Exception as e:
        logging.error(f"Error in update_count: {e}")
    return


async def update_db_server(conn, payload: dict):
    """
    This function sends our payload to the MySQL DB server and adds a row to the Refills table
    :param payload:
    :return: bool
    """
    try:
        async with conn.cursor() as cursor:
            placeholders = ', '.join(['%s'] * len(payload))
            columns = ', '.join(payload.keys())
            sql_string = "INSERT INTO refills (%s) VALUES (%s)" % (columns, placeholders)
            await cursor.execute(sql_string, list(payload.values()))
    except Exception as e:
        logging.error(f"Error in update_db_server: {e}")


async def get_station_count(station_id: int):
    if station_id == 0:
        return total_db["total_count"]

    if station_id not in total_db:
        return -1

    return total_db[station_id]
