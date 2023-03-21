from database import connection
from database import total_db, station_db


def fetch_stations():
    print("Fetching All Stations...")
    if not connection.open:
        connection.ping(reconnect=True)

    with connection:
        with connection.cursor() as cursor:
            sql_string = "SELECT stationId, piSerial FROM hydrostations"
            cursor.execute(sql_string)
            result = cursor.fetchall()

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


def update_count(payload: dict):
    total_db["total_count"] += payload["quantity"]
    station_id = station_db[payload["piSerial"]]
    total_db[station_id] += payload["quantity"]
    return


def update_db_server(payload: dict):
    """
    This function sends our payload to the MySQL DB server and adds a row to the Refills table
    :param payload:
    :return: bool
    """

    if not connection.open:
        connection.ping(reconnect=True)

    with connection:
        with connection.cursor() as cursor:
            placeholders = ', '.join(['%s'] * len(payload))
            columns = ', '.join(payload.keys())
            # data_values = ', '.join(payload.values())
            sql_string = "INSERT INTO refills (%s) VALUES (%s)" % (columns, placeholders)
            cursor.execute(sql_string, list(payload.values()))

        connection.commit()
        # Add some error handeling here
    # if cursor.rowcount == 1:
    #     return True
    # else:
    #     return False
    return


def get_station_count(station_id: int):
    if station_id == 0:
        return total_db["total_count"]

    if station_id not in total_db:
        return -1

    return total_db[station_id]