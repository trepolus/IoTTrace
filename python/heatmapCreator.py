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
filePath = '../data/taxi_heatmap.csv'

'''This is the List containing all taxi data we work with'''
masterList = list()

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

def createTripHeatmap(folderPath, allTrips, passengersInTaxi, initalMapZoom, startTime, endTime):
    latitudeList = list()
    longitudeList = list()
    plotcolor = "#FF0000"

    '''define TimeRange in seconds'''
    timeRange = 600

    googleApiKey = "AIzaSyBFwc7dZAAcAR4AkVl6RrDam68JUWYoQKQ"
    gmap = gmplot.GoogleMapPlotter(31.230347, 121.473873, initalMapZoom, apikey=googleApiKey)

    # decide which limit is appropriate
    limit = len(masterList) - 1
    start = 0
    #limit = 20000

    for k in range(start, limit):
        latitude = float(masterList[k][3])
        longitude = float(masterList[k][2])
        passengers = int(masterList[k][7])
        time1 = timeChanger(masterList[k][6])
        timeOfDay = timeChangerDayTime(masterList[k][6])

        if (timeOfDay >= startTime and timeOfDay < endTime):
            if allTrips:
                latitudeList.append(latitude)
                longitudeList.append(longitude)
            else:
                if passengersInTaxi:
                    if passengers > 0:
                        latitudeList.append(latitude)
                        longitudeList.append(longitude)
                else:
                    if passengers == 0:
                        latitudeList.append(latitude)
                        longitudeList.append(longitude)

    if len(latitudeList) != 0 and len(longitudeList) != 0:
        gmap.heatmap(latitudeList, longitudeList, 10, 10, None, 0.6, True)
    url = "heatmaps/" + str(folderPath) + ".html"
    gmap.draw(url)

'''this section creats heatmapsNoPassengers based on '''
starttime = 0
endtime = 3

if os.path.exists("heatmaps"):
    shutil.rmtree("heatmaps")
os.makedirs("heatmaps")

while starttime < 24:
    outPutFilepath = "ShanghaiHeatMap_hour" + str(starttime) + "to" + str(endtime)
    createTripHeatmap(outPutFilepath, False, False, 12, starttime, endtime)
    starttime = starttime + 3
    endtime = endtime + 3
print("Heatmaps created")

