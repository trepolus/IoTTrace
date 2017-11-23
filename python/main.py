# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse
import csv

from influxdb import InfluxDBClient

def main(host='localhost', port=8086):

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
    i = 0

    with open('../data/taxi0228.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            colnum = 0
            for col in row:

                if colnum == 0:
                    id.append(col)
                if colnum == 1:
                    taxiID.append(col)
                if colnum == 2:
                    longitude.append(col)
                if colnum == 3:
                    latitude.append(col)
                if colnum == 4:
                    speed.append(col)
                if colnum == 5:
                    angle.append(col)
                if colnum == 6:
                    datetime.append(col)
                if colnum == 7:
                    status.append(col)
                if colnum == 8:
                    extendedStatus.append(col)
                if colnum == 9:
                    reversed.append(col)

                colnum = colnum + 1


    """Instantiate a connection to the InfluxDB."""
    user = 'root'
    password = 'root'
    dbname = 'taxi0228'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    query = 'select value from cpu_load_short;'

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    for index in range (0, 1000):

        json_body = [
            {
                "measurement": "taxi0228",
                "tags": {
                    "host": "server01",
                    "region": "france"
                },
               # "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "id": id[index],
                    "taxiID": taxiID[index],
                    "longitude": longitude[index],
                    "latitude": latitude[index],
                    "speed": speed[index],
                    "angle": angle[index],
                    "datetime": datetime[index],
                    "status": status[index],
                    "extendedStatus": extendedStatus[index],
                    "reversed": reversed[index]
                }
            }
        ]
        print("Write points: {0}".format(json_body))
        client.write_points(json_body)

'''

   # print("Create a retention policy")
   # client.create_retention_policy('awesome_policy', '3d', 3, default=True)

  #  print("Switch user: " + dbuser)
   # client.switch_user(dbuser, dbuser_password)

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    print("Querying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))
   
    print("Switch user: " + user)
    client.switch_user(user, password)

    print("Drop database: " + dbname)
    client.drop_database(dbname)
'''

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