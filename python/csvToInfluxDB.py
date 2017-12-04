# -*- coding: utf-8 -*-
import argparse
import csv
import geohash

from influxdb import InfluxDBClient
from datetime import datetime
import time


def timeChanger(timeToChange):
    timeFormat = datetime.strptime(timeToChange, "%Y-%m-%d %H:%M:%S")

    nanoTime = time.mktime(timeFormat.timetuple())
    nanoTime = nanoTime * 1000000000

    return nanoTime


def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'root'
    password = 'root'

    """This is the database name if you want to specify it"""
    dbname = 'taxi0228'

    client = InfluxDBClient(host, port, user, password, dbname)

    """Drop previous database (if not needed comment out following two lines) and create new database"""
    print("Drop database: " + dbname)
    client.drop_database(dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    """ Collections to hold csv data"""
    id = list()
    taxiID = list()
    longitude = list()
    latitude = list()
    speed = list()
    angle = list()
    datetime = list()
    status = list()
    extendedStatus = list()
    reversed = list()
    query = 'SELECT * FROM "' + dbname + '"."autogen"."' + dbname + '"  GROUP BY id ORDER BY DESC LIMIT 100'

    """This is the filePath you have to specify"""
    filePath = '../data/taxi0228.csv'

    print("Writing data to InfluxDB.......")

    with open(filePath, newline='') as f:
        reader = csv.reader(f)
        rownum = 0

        for row in reader:
            '''
            # remove comment brackets if you just want to read in certain lines, e.g. the first 1000
            if rownum >= 200:
                break
            '''
            column = 0
            for col in row:

                if column == 0:
                    id.append(col)
                if column == 1:
                    taxiID.append(col)
                if column == 2:
                    longitude.append(col)
                if column == 3:
                    latitude.append(col)
                if column == 4:
                    speed.append(col)
                if column == 5:
                    angle.append(col)
                if column == 6:
                    datetime.append(col)
                if column == 7:
                    status.append(col)
                if column == 8:
                    extendedStatus.append(col)
                if column == 9:
                    reversed.append(col)

                column = column + 1

            geohash1 = geohash.encode(float(latitude[rownum]), float(longitude[rownum]))

            json_body = [
                {
                    "measurement": "taxi0228",
                    "tags": {
                        "region": "shanghai",
                        "geohash": geohash1
                    },
                    "time": int(timeChanger(datetime[rownum])),
                    "fields": {
                        "id": int(id[rownum]),
                        "taxiID": taxiID[rownum],
                        "longitude": longitude[rownum],
                        "latitude": latitude[rownum],
                        "speed": int(speed[rownum]),
                        "angle": int(angle[rownum]),
                        "datetime": datetime[rownum],
                        "status": int(status[rownum]),
                        "extendedStatus": int(extendedStatus[rownum]),
                        "reversed": int(reversed[rownum])
                    }
                }
            ]
            client.write_points(json_body)
            """remove " # " if you want to print out every line"""
            # print("Write points: {0}".format(json_body))
            rownum = rownum + 1

    """ print out last 100 lines to check if data is in InfluxDB"""
    print("Data was successfully commited!\n\n")
    print("Get the last 100 rows in database: \n")
    print("Querying data: " + query)
    result = client.query(query)
    for row in result:
        for col in row:
            print(col)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
