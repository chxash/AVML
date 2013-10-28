#!/bin/python

from bs4 import BeautifulSoup
import urllib
from dataParse import DataParse 
from dataSave import DataSave

#gather every station from url
urlStations = 'http://www.romma.fr/index.php'

#TODO different path regarding location
path = 'C:/Users/Ash/Desktop/AVML/src/dataSave/'

#Permits different version of storage for the data
currentDataVersion = 1
dataVersion = {}

#TODO : organize /rename data
dataVersion[1] = ['obsDate','obsHour',
'obsTemperature','oneHourVarTemp','deltaTemp','minTemp','maxTemp','windChillTemp',
'rainFromMidnight','rainIntensity','maxRainIntensity',
'humidity','roseePoint','minHumidity','hourMinHumidity','maxHumidity','hourMaxHumidity',
'pression','pressionVarLastThreeHour','minPression','hourMinPression','maxPression','hourMaxPression',
'sun','maxSun',
'avgWind','windDirection','maxWindLastTen','maxWindMidnight','maxWindHour']


urllist = DataParse.getStations()

########################################
#                                      #
#   COLLECT RAW DATAS / SAVE TO FILES  #
#                                      #
########################################

okStations = []
skippedStations = []

for stationName in urllist:
    print stationName
    result = DataParse.getDatas('http://www.romma.fr/'+urllist[stationName][2:],False)
    if (len(result)>0):
        result['StationName'] = stationName
        result['Version'] = currentDataVersion #First version of data saved, to be defined
        DataSave.saveStation(result,path,dataVersion[currentDataVersion])
        okStations.append(stationName)
    else:
        #TODO list of skipped stations + save ?
        print 'skipping'+stationName
        skippedStations.append(stationName)
DataSave.saveSummary(path,currentDataVersion,okStations,skippedStations)

test = DataParse.getBRADept(38,True)
#print result