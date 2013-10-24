#!/bin/python

from bs4 import BeautifulSoup
import urllib
from dataParse import DataParse 
from dataSave import DataSave

#gather every station from url
urlStations = 'http://www.romma.fr/index.php'
path = ''

#Permits different version of storage for the data
currentDataVersion = 1
dataVersion = {}

#organize /rename data
dataVersion[1] = ['obsDate','obsHour','obsTemperature','oneHourVarTemp',
'rainFromMidnight','deltaTemp','minTemp','rainIntensity','maxTemp',
'maxRainIntensity','humidity','pression','roseePoint','pressionVarLastThreeHour',
'minHumidity','hourMinHumidity','minPression','hourMinPression','maxHumidity',
'hourMaxHumidity','maxPression','hourMaxPression','sun','maxSun','windChillTemp',
'avgWind','windDirection','maxWindLastTen','maxWindMidnight','maxWindHour']


urllist = DataParse.getStations()

#Test urls
#url = 'http://www.romma.fr/station_24.php?id=%206'
#url = 'http://www.romma.fr/station_24.php?id=%2066'
#url = 'http://www.romma.fr/station_24.php?id=%2072'


########################################
#                                      #
#   COLLECT RAW DATAS / SAVE TO FILES  #
#                                      #
########################################

for stationName in urllist:
    print stationName
    result = DataParse.getDatas(urllist[stationName],False)
    if (len(result)>0):
        result['StationName'] = stationName
        result['Version'] = currentDataVersion #First version of data saved, to be defined
    else:
        print 'skipping'+stationName
    #DataSave.saveStation(result,path,dataVersion[currentDataVersion])
    print result