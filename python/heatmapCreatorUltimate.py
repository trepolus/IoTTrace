import csv
import gmplot
import random
from datetime import datetime
import time
import shutil
import os

'''
This Program can create different maps and paths out of a taxi.csv file
'''

"""This is the filePath you have to specify"""
filePath = '../data/taxi-medium-bigbig.csv'

'''This is the List containing all taxi data we work with'''
masterList = list()

googleApiKey = "AIzaSyBFwc7dZAAcAR4AkVl6RrDam68JUWYoQKQ"

def timeChanger(timeToChange):
    timeFormat = datetime.strptime(timeToChange, "%Y-%m-%d %H:%M:%S")

    seconds = time.mktime(timeFormat.timetuple())
    return seconds


def timeChangerDayTime(timeToChange):
    timeOfDay = datetime.strptime(timeToChange, "%Y-%m-%d %H:%M:%S").time()
    timeOfDay = timeOfDay.hour
    return timeOfDay

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

'''leave this if you want to have a sorted list (after taxiID)'''
#masterList = sort(masterList)


'''allTrips: wether a passengersInTaxi should be considered or not, plots ALL trips'''
'''passengersInTaxi: wether all the datasets with or without passengers should be plotted'''

def createTripHeatmap(folderPath, allTrips, passengersInTaxi, initalMapZoom, timeDifference, radius):

    # create all timeDifference Lists
    latitudeLists = list()
    longitudeLists = list()

    startTime = 0

    while startTime < 24:
        latitudeLists.append(list())
        longitudeLists.append(list())

        startTime = startTime + timeDifference

    # decide which limit is appropriate
    limit = len(masterList) - 1
    start = 0
    #limit = 20000

    for k in range(start, limit):
        latitude = float(masterList[k][3])
        longitude = float(masterList[k][2])
        passengers = int(masterList[k][7])
        timeOfDay = timeChangerDayTime(masterList[k][6])

        listIndex = int(timeOfDay / timeDifference)

        if allTrips:
            latitudeLists[listIndex].append(latitude)
            longitudeLists[listIndex].append(longitude)
        else:
            if passengersInTaxi:
                if passengers > 0:
                    latitudeLists[listIndex].append(latitude)
                    longitudeLists[listIndex].append(longitude)
            else:
                if passengers == 0:
                    latitudeLists[listIndex].append(latitude)
                    longitudeLists[listIndex].append(longitude)

    startTime = 0
    index = 0

    while startTime < 24:
        gmap = gmplot.GoogleMapPlotter(31.230347, 121.473873, initalMapZoom, apikey=googleApiKey)

        # gmap parameters: latitude, longitude, treshold, radius, gradient, opacity, dissipating
        gmap.heatmap(latitudeLists[index], longitudeLists[index], 10, radius, None, 0.6, True)
        if (startTime + timeDifference) < 24:
            url = str(folderPath) + "_from_" + str(startTime) + "_to_" + str(startTime + timeDifference) + ".html"
        else:
            url = str(folderPath) + "_from_" + str(startTime) + "_to_24.html"

        gmap.draw(url)
        startTime = startTime + timeDifference
        index = index + 1

folderName = "heatmaps"

if os.path.exists(folderName):
    shutil.rmtree(folderName)
os.makedirs(folderName)

outPutFilepath = folderName + "/ShanghaiHeatMap"

'''parameters: filepath / name, show all trips, if alltrips is false next param: no passengers(false)/passengers(true),'''
'''zoomfactor, timeDifference of heatmaps(1 - 24, only ints), radius'''
createTripHeatmap(outPutFilepath, False, True, 11, 3, 15)

print("Heatmaps created")

