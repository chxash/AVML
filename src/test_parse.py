#!/bin/python

from bs4 import BeautifulSoup
import urllib

#url = 'http://romma.fr/#ui-tabs-2'
#Le versoud
url = 'http://www.romma.fr/station_24.php?id=%206'
try:
    filehandle = urllib.urlopen(url, proxies={})
except urllib.HTTPError, e:
    print 'Oops failed to load url'+url
soup = BeautifulSoup(filehandle)


#Tag h3
iter=soup.find(id="affichage_simple").find_next('h3')

txtToParse = iter.get_text()


#########################
#                       #
#   COLLECT RAW DATAS   #
#                       #
#########################


#Day and Hour
print(txtToParse[30:])
day = txtToParse[30:32]
month = txtToParse[33:37].upper()
yearIndex = txtToParse[37:].index('2')
year = txtToParse[37+yearIndex:41+yearIndex]
print(day+' '+month+' '+year)
print ()
if (month=='JANV'):
    obsDate = day+'/01/'+year
elif (month == 'FEVR'):
    obsDate = day+'/01/'+year
elif (month == 'MARS'):
    obsDate = day+'/03/'+year
elif (month == 'AVRI'):
    obsDate = day+'/04/'+year
elif (month == 'MAI '):
    obsDate = day+'/05/'+year
elif (month == 'JUIN'):
    obsDate = day+'/06/'+year
elif (month == 'JUIL'):
    obsDate = day+'/07/'+year
elif (month == 'AOUT'):
    obsDate = day+'/08/'+year
elif (month == 'SEPT'):
    obsDate = day+'/09/'+year
elif (month == 'OCTO'):
    obsDate = day+'/10/'+year
elif (month == 'NOVE'):
    obsDate = day+'/11/'+year
elif (month == 'DECE'):
    obsDate = day+'/12/'+year
else: 
    print 'couldnt read month'

hourIndex = txtToParse[37:].index(':')
obsHour = txtToParse[37+hourIndex-2:37+hourIndex+3]

print(obsDate)
print(obsHour)


#Temperature / OneHourVarTemp / RainFromMidnight
iter = iter.next_sibling.next_sibling.find_next('tr').next_sibling.next_sibling
findTemp = iter.contents[1].contents[0]
obsTemperature = findTemp.get_text()
print(obsTemperature)

findOneHourVarTemp = iter.contents[3].contents[1]
oneHourVarTemp = findOneHourVarTemp.get_text()
tempIndex = oneHourVarTemp.index('C')
oneHourVarTemp = oneHourVarTemp[:tempIndex-2]
print(oneHourVarTemp)

findRainFromMidnight = iter.contents[5].contents[1]
rainFromMidnight = findRainFromMidnight.get_text()

print(rainFromMidnight)


#Delta Temperature 24h / min Temperature / Rain intensity
iter = iter.next_sibling.next_sibling
findDeltaTemp = iter.contents[1].contents[1]
deltaTemp = findDeltaTemp.get_text()
tempIndex = deltaTemp.index('C')
deltaTemp = deltaTemp[:tempIndex-2]

print(deltaTemp)

iter = iter.next_sibling.next_sibling

findMinTemp = iter.contents[1].contents[1]
minTemp = findMinTemp.get_text()
tempIndex = minTemp.index('C')
minTemp = minTemp[:tempIndex-2]
print(minTemp)

findRainIntensity = iter.contents[3].contents[1]
rainIntensity = findRainIntensity.get_text()
tempIndex = rainIntensity.index('m')
rainIntensity = rainIntensity[:tempIndex-1]
print(rainIntensity)

#Max Temperature from 0h / Max Rain Intensity from 0h
iter = iter.next_sibling.next_sibling

findMaxTemp = iter.contents[1].contents[1]
maxTemp = findMaxTemp.get_text()
tempIndex = maxTemp.index('C')
maxTemp = maxTemp[:tempIndex-2]
print(maxTemp)

findMaxRainIntensity = iter.contents[3].contents[1]
maxRainIntensity = findMaxRainIntensity.get_text()
tempIndex = maxRainIntensity.index('m')
maxRainIntensity = maxRainIntensity[:tempIndex-1]
print(maxRainIntensity)

#Humidity / Pression
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling

findHumidity = iter.contents[1].contents[0]
humidity = findHumidity.get_text()
print(humidity)

findPression = iter.contents[5].contents[0]
pression = findPression.get_text()
print(pression)

#Rosee Point 
iter = iter.next_sibling.next_sibling
findRosePoint = iter.contents[1].contents[1]
roseePoint = findRosePoint.get_text()
tempIndex = roseePoint.index('C')
roseePoint = roseePoint[:tempIndex-2]
print(roseePoint)

#Pression Var (3h) 
iter = iter.next_sibling.next_sibling
findPressionVarLastThreeHour = iter.contents[3].contents[1]
pressionVarLastThreeHour = findPressionVarLastThreeHour.get_text()
pressionVarLastThreeHour = pressionVarLastThreeHour[:-4]
pressionVarLastThreeHour=pressionVarLastThreeHour[1 if pressionVarLastThreeHour[0]=='+' else 0:]

print(pressionVarLastThreeHour)

#Min Humidity / Pression since midnight 
#And hour of event
iter = iter.next_sibling.next_sibling
findMinHumidity = iter.contents[1].contents[1]
minHumidity = findMinHumidity.get_text()
minHumidity = minHumidity[:-2]
print(minHumidity)

hourMinHumidity = iter.contents[1].contents[2]
hourMinHumidity = hourMinHumidity[4 if hourMinHumidity[3]==' ' else 3:]
print(hourMinHumidity)

findMinPression = iter.contents[3].contents[1]
minPression = findMinPression.get_text()
minPression = minPression[:-4]
print(minPression)

hourMinPression = iter.contents[3].contents[2]
hourMinPression = hourMinPression[4 if hourMinPression[3]==' ' else 3:]
print(hourMinPression)

#Max Humidity / Pression since midnight
#And hour of event
iter = iter.next_sibling.next_sibling
findMaxHumidity = iter.contents[1].contents[1]
maxHumidity = findMaxHumidity.get_text()
maxHumidity = maxHumidity[:-2]
print(maxHumidity)

hourMaxHumidity = iter.contents[1].contents[2]
hourMaxHumidity = hourMaxHumidity[4 if hourMaxHumidity[3]==' ' else 3:]
print(hourMaxHumidity)

findMaxPression = iter.contents[3].contents[1]
maxPression = findMaxPression.get_text()
maxPression = maxPression[:-4]
print(maxPression)

hourMaxPression = iter.contents[3].contents[2]
hourMaxPression = hourMaxPression[4 if hourMaxPression[3]==' ' else 3:]
print(hourMaxPression)

#Sun
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
findSun = iter.contents[1].contents[1]
sun = findSun.get_text()
print(sun)

#max Sun / wind chill Temperature
iter = iter.next_sibling.next_sibling
findMaxSun = iter.contents[1].contents[1]
maxSun = findMaxSun.get_text()
tempIndex = maxSun.index('w')
maxSun = maxSun[:tempIndex-1]
print(maxSun)

findWindChillTemp = iter.contents[3].contents[1]
windChillTemp = findWindChillTemp.get_text()
print(windChillTemp)

#Average Wind
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
findAvgWind = iter.contents[1].contents[1]
avgWind = findAvgWind.get_text()
print(avgWind)

#TODO rose des vents ?

#Direction
iter = iter.next_sibling.next_sibling.next_sibling.next_sibling
findDirection = iter.contents[1].contents[1]
windDirection = findDirection.get_text()
print(windDirection)


#Max Wind last 10 min
iter = iter.next_sibling.next_sibling
findMaxWindLastTen = iter.contents[1].contents[1]
maxWindLastTen = findMaxWindLastTen.get_text()
tempIndex = maxWindLastTen.index('k')
maxWindLastTen=maxWindLastTen[:tempIndex-1]
print(maxWindLastTen)

#Max Wind since midnight / Hour
iter = iter.next_sibling.next_sibling
findMaxWindMidnight = iter.contents[1].contents[1]
maxWindMidnight = findMaxWindMidnight.get_text()
tempIndex = maxWindMidnight.index('k')
maxWindMidnight=maxWindMidnight[:tempIndex-1]
print(maxWindMidnight)

findHour = iter.contents[1].contents[2]
maxWindHour = findHour[4 if findHour[3]==' ' else 3:]
print(maxWindHour)


#####################
#                   #
#   SAVE TO FILES   #
#                   #
#####################