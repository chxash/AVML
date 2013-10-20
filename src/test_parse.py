#!/bin/python

from bs4 import BeautifulSoup
import urllib
from dataParse import DataParse 

#url = 'http://romma.fr/#ui-tabs-2'
#Le versoud
#url = 'http://www.romma.fr/station_24.php?id=%206'
#url = 'http://www.romma.fr/station_24.php?id=%2066'
url = 'http://www.romma.fr/station_24.php?id=%2072'
try:
    filehandle = urllib.urlopen(url, proxies={})
except urllib.HTTPError, e:
    print 'Oops failed to load url'+url
soup = BeautifulSoup(filehandle)


#########################
#                       #
#   COLLECT RAW DATAS   #
#                       #
#########################

#Tag h3
iter=soup.find(id="affichage_simple").find_next('h3')

#Day and Hour
txtToParse = iter.get_text()
obsDate = DataParse.convertDate(txtToParse)

hourIndex = txtToParse[37:].index(':')
obsHour = txtToParse[37+hourIndex-2:37+hourIndex+3]

print('obsDate : '+obsDate)
print('obsHour : '+obsHour)

#Temperature / OneHourVarTemp / RainFromMidnight
iter = iter.next_sibling.next_sibling.find_next('tr').next_sibling.next_sibling
obsTemperature = iter.contents[1].contents[0].get_text()
print('obsTemperature : '+obsTemperature)

oneHourVarTemp = DataParse.ParseCut(iter.contents[3].contents[1],'C',2)
print('oneHourVarTemp : '+oneHourVarTemp)

rainFromMidnight = iter.contents[5].contents[1].get_text()
print('rainFromMidnight : '+rainFromMidnight)

#Delta Temperature 24h / min Temperature / Rain intensity
iter = iter.next_sibling.next_sibling
deltaTemp = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
print('deltaTemp : '+deltaTemp)


iter = iter.next_sibling.next_sibling
minTemp = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
print('minTemp : '+minTemp)

rainIntensity = DataParse.ParseCut(iter.contents[3].contents[1],'m',1)
print('rainIntensity : '+rainIntensity)

#Max Temperature from 0h / Max Rain Intensity from 0h
iter = iter.next_sibling.next_sibling

maxTemp = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
print('maxTemp : '+maxTemp)

maxRainIntensity = DataParse.ParseCut(iter.contents[3].contents[1],'m',1)
print('maxRainIntensity : '+maxRainIntensity)

#Humidity / Pression
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling

humidity = iter.contents[1].contents[0].get_text()
print('humidity : '+humidity)

pression = iter.contents[5].contents[0].get_text()
print('pression : '+pression)

#Rosee Point 
iter = iter.next_sibling.next_sibling
roseePoint = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
print('roseePoint : '+roseePoint)

#Pression Var (3h) 
iter = iter.next_sibling.next_sibling
if (len(iter.contents[3].contents)>1):
    pressionVarLastThreeHour=DataParse.ParseTrunk(iter.contents[3].contents[1],4)
    pressionVarLastThreeHour=pressionVarLastThreeHour[1 if pressionVarLastThreeHour[0]=='+' else 0:]
else:
    pressionVarLastThreeHour='---'
print('pressionVarLastThreeHour : '+pressionVarLastThreeHour)

#Min Humidity / Pression since midnight 
#And hour of event
iter = iter.next_sibling.next_sibling
minHumidity=DataParse.ParseTrunk(iter.contents[1].contents[1],2)
print('minHumidity : '+minHumidity)

hourMinHumidity=DataParse.ParseHour(iter.contents[1].contents[2])
print('hourMinHumidity : '+hourMinHumidity)

if (len(iter.contents[3].contents)>1):
    minPression=DataParse.ParseTrunk(iter.contents[3].contents[1],4)
    hourMinPression=DataParse.ParseHour(iter.contents[3].contents[2])
else:
    minPression='---'
    hourMinPression='---'
    
print('minPression : '+minPression)
print('hourMinPression : '+hourMinPression)

#Max Humidity / Pression since midnight
#And hour of event
iter = iter.next_sibling.next_sibling
maxHumidity = DataParse.ParseTrunk(iter.contents[1].contents[1],2)
print('maxHumidity : '+maxHumidity)

hourMaxHumidity=DataParse.ParseHour(iter.contents[1].contents[2])
print('hourMaxHumidity : '+hourMaxHumidity)

if (len(iter.contents[3].contents)>1):
    maxPression=DataParse.ParseTrunk(iter.contents[3].contents[1],4)
    hourMaxPression=DataParse.ParseHour(iter.contents[3].contents[2])
else:
    maxPression='---'
    hourMaxPression='---'
print('maxPression : '+maxPression)


print('hourMaxPression : '+hourMaxPression)

#Sun
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
findSun = iter.contents[1].contents[1]
sun = findSun.get_text()
print('sun : '+sun)

#max Sun / wind chill Temperature
iter = iter.next_sibling.next_sibling
maxSun=DataParse.ParseCut(iter.contents[1].contents[1],'w',1)
print('maxSun : '+maxSun)

windChillTemp = iter.contents[3].contents[1].get_text()
print('windChillTemp : '+windChillTemp)

#Average Wind
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
avgWind = iter.contents[1].contents[1].get_text()
print('avgWind : '+avgWind)

#TODO rose des vents ?

#Direction
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling
windDirection = iter.contents[1].contents[1].get_text()
print('windDirection : '+windDirection)


#Max Wind last 10 min
iter = iter.next_sibling.next_sibling
maxWindLastTen = DataParse.ParseCut(iter.contents[1].contents[1],'k',1)
print('maxWindLastTen : '+maxWindLastTen)

#Max Wind since midnight / Hour
iter = iter.next_sibling.next_sibling
maxWindMidnight = DataParse.ParseCut(iter.contents[1].contents[1],'k',1)
print('maxWindMidnight : '+maxWindMidnight)

maxWindHour=DataParse.ParseHour(iter.contents[1].contents[2])
print('maxWindHour : '+maxWindHour)


#####################
#                   #
#   SAVE TO FILES   #
#                   #
#####################