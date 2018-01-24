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


"""This is the filePath you have to specify"""
filePath = '../data/taxi-medium-big.csv'

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

def createMultipleMapsSortedByTaxiID(folderPath):

    latitudeList = list()
    longitudeList = list()

    '''define TimeRange in seconds'''
    timeRange = 600

    googleApiKey = "AIzaSyBFwc7dZAAcAR4AkVl6RrDam68JUWYoQKQ"
    gmap = gmplot.GoogleMapPlotter(31.138049, 121.479736, 12, apikey=googleApiKey)
    k = 0
    countTrips = 0

    for k in range(0, 3000):
    #use following line if you want to iterate over the whole list
    #for row in masterList:
        latitude = float(masterList[k][3])
        longitude = float(masterList[k][2])

        latitudeList.append(latitude)
        longitudeList.append(longitude)

        if k + 1 < len(masterList):

            currentTaxiID = masterList[k][1]
            nextTaxiID = masterList[k + 1][1]

            time1 = timeChanger(masterList[k][6])
            time2 = timeChanger(masterList[k + 1][6])
            timedif = time2 - time1

            if (currentTaxiID != nextTaxiID) or (timedif >= timeRange or timedif <= -timeRange):

                '''use randomColor if you want to have a colorful output'''
                r = lambda: random.randint(0, 255)
                randomColor = '#%02X%02X%02X' % (r(), r(), r())
                '''draw lines'''
                gmap.plot(latitudeList, longitudeList, "#0000FF", edge_width=5)
                '''draw points'''
                gmap.scatter(latitudeList, longitudeList, '#FF0000', size=50, marker=False)
                '''draw heatmap'''
                gmap.heatmap(latitudeList, longitudeList)

                countTrips = countTrips + 1
                latitudeList = list()
                longitudeList = list()

                if (currentTaxiID != nextTaxiID):
                    url = str(folderPath) + '/taxiID_' + str(currentTaxiID) + "_Trips_" + str(countTrips) + ".html"
                    gmap.draw(url)
                    gmap = gmplot.GoogleMapPlotter(31.138049, 121.479736, 12, apikey=googleApiKey)
                    countTrips = 0
                    latitudeList = list()
                    longitudeList = list()
        elif k+1 is len(masterList):
            gmap.draw(url)

        '''use this if you want to print latitudes or if you do not use for(range), it is important to increase k '''
         #print(latitudeList[k], longitudeList[k])
         #k = k + 1

def createOneMapWithAllTrips(folderPath, showPassengers):

    latitudeList = list()
    longitudeList = list()
    plotcolor = "#FF0000"

    '''define TimeRange in seconds'''
    timeRange = 600

    googleApiKey = "AIzaSyBFwc7dZAAcAR4AkVl6RrDam68JUWYoQKQ"
    gmap = gmplot.GoogleMapPlotter(31.138049, 121.479736, 12, apikey=googleApiKey)
    k = 0

    for k in range(0, len(masterList)-1):
        # use following line if you want to iterate over the whole list
        #for row in masterList:
        latitude = float(masterList[k][3])
        longitude = float(masterList[k][2])

        latitudeList.append(latitude)
        longitudeList.append(longitude)

        if k + 1 < len(masterList):

            currentTaxiID = masterList[k][1]
            nextTaxiID = masterList[k + 1][1]

            time1 = timeChanger(masterList[k][6])
            time2 = timeChanger(masterList[k + 1][6])
            timedif = time2 - time1

            if (currentTaxiID != nextTaxiID) or (timedif >= timeRange or timedif <= -timeRange):

                '''use randomColor if you want to have a colorful output'''
                if (showPassengers):
                    plotcolor = "#0000FF"

                    # if no passenger, make line red!
                    if masterList[k][7] == 0:
                        plotcolor = "#FF0000"
                else:
                    r = lambda: random.randint(0, 255)
                    randomColor = '#%02X%02X%02X' % (r(), r(), r())
                    plotcolor = randomColor

                '''draw lines'''
                gmap.plot(latitudeList, longitudeList, plotcolor, edge_width=1)
                '''draw points'''
                #gmap.scatter(latitudeList, longitudeList, '#FF0000', size=50, marker=False)
                '''draw heatmap'''
                gmap.heatmap(latitudeList, longitudeList)

                latitudeList = list()
                longitudeList = list()


        '''use this if you want to print latitudes or if you do not use for(range), it is important to increase k '''
        # print(latitudeList[k], longitudeList[k])
        # k = k + 1
    url = str(folderPath) + ".html"
    gmap.draw(url)

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

    #decide which limit is appropriate
    #limit = len(masterList)-1
    start = 0
    limit = 20000

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

        if k + 1 < len(masterList):

            currentTaxiID = masterList[k][1]
            nextTaxiID = masterList[k + 1][1]

            #time1 = timeChanger(masterList[k][6]) # gets already set at the beginning
            time2 = timeChanger(masterList[k + 1][6])
            timedif = time2 - time1

            if (currentTaxiID != nextTaxiID) or (timedif >= timeRange or timedif <= -timeRange):

                if (passengersInTaxi):
                    plotcolor = "#0000FF"
                else:
                    plotcolor = "#FF0000"

                if len(latitudeList) != 0 and len(longitudeList) != 0:
                    '''draw lines'''
                    #gmap.plot(latitudeList, longitudeList, plotcolor, edge_width=1)
                    '''draw points'''
                    #gmap.scatter(latitudeList, longitudeList, '#FF0000', size=50, marker=False)
                    '''draw heatmap'''
                    # gmap parameters: latitude, longitude, treshold, radius, gradient, opacity, dissipating
                    gmap.heatmap(latitudeList, longitudeList, 10, 10, None, 0.6, True)

                latitudeList = list()
                longitudeList = list()


        '''use this if you want to print latitudes or if you do not use for(range), it is important to increase k '''
        # print(latitudeList[k], longitudeList[k])
    url = "heatmaps/" + str(folderPath) + ".html"
    gmap.draw(url)

def createOneMapWithSpeedsZero(folderPath):

    latitudeList = list()
    longitudeList = list()
    speed = list()

    '''define TimeRange in seconds'''
    timeRange = 600

    googleApiKey = "AIzaSyBFwc7dZAAcAR4AkVl6RrDam68JUWYoQKQ"
    gmap = gmplot.GoogleMapPlotter(31.138049, 121.479736, 12, apikey=googleApiKey)
    k = 0

    for k in range(0, 10000):
        # use following line if you want to iterate over the whole list
        # for row in masterList:
        latitude = float(masterList[k][3])
        longitude = float(masterList[k][2])
        speed = int(masterList[k][4])

        latitudeList.append(latitude)
        longitudeList.append(longitude)

        if speed == 0:

            if k + 1 < len(masterList):

                currentTaxiID = masterList[k][1]
                nextTaxiID = masterList[k + 1][1]

                time1 = timeChanger(masterList[k][6])
                time2 = timeChanger(masterList[k + 1][6])
                timedif = time2 - time1

                if (currentTaxiID != nextTaxiID) or (timedif >= timeRange or timedif <= -timeRange):

                    '''use randomColor if you want to have a colorful output'''
                    #r = lambda: random.randint(0, 255)
                    #randomColor = '#%02X%02X%02X' % (r(), r(), r())
                    '''draw lines'''
                    #gmap.plot(latitudeList, longitudeList, randomColor, edge_width=5)
                    '''draw points'''
                    gmap.scatter(latitudeList, longitudeList, currentTaxiID, marker=True)
                    '''draw heatmap'''
                    gmap.heatmap(latitudeList, longitudeList)

                    latitudeList = list()
                    longitudeList = list()


        '''use this if you want to print latitudes or if you do not use for(range), it is important to increase k '''
        # print(latitudeList[k], longitudeList[k])
        # k = k + 1
    url = str(folderPath) + ".html"
    gmap.draw(url)

'''set filePath for multiple maps, old maps get deleted, new ones created'''

outPutFilepath = "maps"

if os.path.exists(outPutFilepath):
    shutil.rmtree("maps")
os.makedirs(outPutFilepath)

"""
#creates multiple maps into outputPath
createMultipleMapsSortedByTaxiID(outPutFilepath)
print("Success, Maps created!")
"""

'''create a Map of all the trips'''
#outPutFilepath = "maps"
#outPutFilepath = "ShanghaiMegaMap_medium_small"
'''include false/true if you want to show a difference between cabs with passengers or without'''
#createOneMapWithAllTrips(outPutFilepath, True)
#print("Success, MegaMap created!")

'''create a Map of all the trips
outPutFilepath = "ShanghaiSpeedsZeroMap"
createOneMapWithSpeedsZero(outPutFilepath)
print("Success, SpeedsZeroMap created!")
'''

'''create a HeatMap of al trips with or without passengers'''
outPutFilepath = "ShanghaiHeatMap"

'''parameters: filename, passengers(True/False), zoomsize of Map'''
#True puts out a map with passengers, False without
#createTripHeatmap(outPutFilepath, True, 12, 1, 2)
#print("Success, HeatMap created!")

'''this section creats heatmapsNoPassengers based on '''
starttime = 0
endtime = 3

if os.path.exists("heatmaps"):
    shutil.rmtree("heatmaps")
os.makedirs("heatmaps")

while starttime < 24:
    outPutFilepath = "ShanghaiHeatMap_hour" + str(starttime) + "to" + str(endtime)
    createTripHeatmap(outPutFilepath, True, False, 12, starttime, endtime)
    starttime = starttime + 3
    endtime = endtime + 3
print("Heatmaps created")

'''some examples how to plot a map'''
# gmap.plot(latitudeList, longitudeList, 'cornflowerblue', edge_width=2)
# gmap.scatter(latitudeList, longitudeList, '#FF0000', size=55, marker=False)
# gmap.scatter(latitudeList, longitudeList,, 'k', marker=True)
# gmap.heatmap(latitudeList, longitudeList,)

#gmap.draw("maps/shanghai3.html")
