# -*- coding: utf-8 -*-
import argparse

from influxdb import InfluxDBClient


def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'root'
    password = 'root'

    """This is the database name if you want to specify it"""
    dbname = 'taxi0228'

    client = InfluxDBClient(host, port, user, password, dbname)



    query = 'SELECT * FROM "' + dbname + '"."autogen"."' + dbname + '"  GROUP BY id ORDER BY DESC LIMIT 100'


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