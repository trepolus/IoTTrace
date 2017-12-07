
import csv
import gmplot
import random
from datetime import datetime
import time
import shutil
import os
import pandas as pd
from math import radians, cos, sin, asin, sqrt


'''
This Program can sort a taxi.csv file after TaxiID, create a csv file out of it and calculate Distance between Trips
'''

def timeChanger(timeToChange):
    timeFormat = datetime.strptime(timeToChange, "%Y-%m-%d %H:%M:%S")

    seconds = time.mktime(timeFormat.timetuple())
    return seconds

'''
This sorts the csv File after taxiID's
'''

def sort(taxiList):
    less = []
    equal = []
    greater = []

    if len(taxiList) > 1:
        pivot = taxiList[0][1]
        for x in taxiList:
            if x[1] < pivot:
                less.append(x)
            elif x[1] == pivot:
                equal.append(x)
            else:
                greater.append(x)
        return sort(less) + equal + sort(greater)  # Just use the + operator to join lists
    else:
        return taxiList


"""This is the filePath you have to specify"""
filePath = '../data/taxi0228.csv'

'''This is the List containing all taxi data we work with'''
masterList = list()

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
        rowList = list()
        for col in row:
            rowList.append(col)
            column = column + 1
        masterList.append(rowList)
        rownum = rownum + 1

masterList = sort(masterList)
i = 0

# You can use this for printing the List
def printMasterlist():
    for tempList in masterList:
        output = ""
        for column in tempList:
            output = output + column + " "
            print("Row", i, ":", output)
        i = i + 1

def createCSV(list, name):
    df = pd.DataFrame(list)
    df.to_csv(name + '.csv', index=False, header=False)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Code from: https://tinyurl.com/y8zc4qap
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371000* c
    return m

def createDistanceCSV ():
    distanceList = list()
    firstLine = list()

    firstLine.append("taxiID")
    firstLine.append("trip")
    firstLine.append("distance")
    firstLine.append("points")


    distanceList.append(firstLine)

    pointList = list()

    '''define TimeRange in seconds'''
    timeRange = 600

    k = 0
    countTrips = 0

    for row in masterList:
        # use following line if you want to iterate over the whole list
        # for row in masterList:
        points = list()
        latitude = float(masterList[k][3])
        longitude = float(masterList[k][2])

        points.append(longitude)
        points.append(latitude)

        pointList.append(points)

        if k + 1 < len(masterList):

            currentTaxiID = masterList[k][1]
            nextTaxiID = masterList[k + 1][1]

            time1 = timeChanger(masterList[k][6])
            time2 = timeChanger(masterList[k + 1][6])
            timedif = time2 - time1

            if (currentTaxiID != nextTaxiID) or (timedif >= timeRange or timedif <= -timeRange):
                distance = 0
                counter = 0

                for lonLat in pointList:
                    if counter + 1 < len(pointList):
                        distance = distance + haversine(lonLat[0], lonLat[1], pointList[counter+1][0], pointList[counter+1][1])
                    counter = counter + 1

                countTrips = countTrips + 1
                dataList = list()
                dataList.append(currentTaxiID)
                dataList.append(countTrips)
                dataList.append(str(int(distance)) + "m")
                dataList.append(counter)

                distanceList.append(dataList)

                pointList = list()


                if (currentTaxiID != nextTaxiID):
                    countTrips = 0

        k = k + 1
    createCSV(distanceList, "distances")
#createCSV(masterList, "taxiIDSorted2")
createDistanceCSV()