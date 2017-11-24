# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse
import csv

from influxdb import InfluxDBClient


def main(host='localhost', port=8086):

    """Instantiate a connection to the InfluxDB."""
    user = 'root'
    password = 'root'
    dbname = 'taxi0228'

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Drop database: " + dbname)
    client.drop_database(dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    """ Read and categorise data from given csv file"""
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
    query = 'SELECT * FROM "' + dbname + '"."autogen"."' + dbname + '"  GROUP BY * ORDER BY DESC LIMIT 100'

    print("Writing data to InfluxDB.......")

    with open('../data/taxi0228.csv', newline='') as f:
        reader = csv.reader(f)
        rownum = 0

        for row in reader:
            if rownum >= 1000:
                break
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

            json_body = [
                {
                    "measurement": "taxi0228",
                    "tags": {
                        "region": "shanghai"
                    },
                    "fields": {
                        "id": id[rownum],
                        "taxiID": taxiID[rownum],
                        "longitude": longitude[rownum],
                        "latitude": latitude[rownum],
                        "speed": speed[rownum],
                        "angle": angle[rownum],
                        "datetime": datetime[rownum],
                        "status": status[rownum],
                        "extendedStatus": extendedStatus[rownum],
                        "reversed": reversed[rownum]
                    }
                }
            ]
            client.write_points(json_body)
            #print("Write points: {0}".format(json_body))
            rownum = rownum + 1

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