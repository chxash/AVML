from bs4 import BeautifulSoup
import urllib
import re

class DataParse:

    nullValue = '--'
    braMainUrl = 'http://france.meteofrance.com/france/MONTAGNE?MONTAGNE_PORTLET.path=montagnebulletinneige%2FDEPT'
    
    ######################################
    #methods used to load data from romma#
    ######################################
    
    #Parse txt and cut the end according to a certain caracter (refCaracter) and a number of caracter to cut
    #Very often refCaracter is something like a physical unit (C for temperature ...)
    @staticmethod
    def ParseCut(contentToParse,refCaracter,numCaracToCut):
        result = contentToParse.get_text()
        index = result.index(refCaracter)
        result = result[:index-numCaracToCut]
        return result
        
    #Parse txt and simply trunk the end according to a number of caracter to cut
    @staticmethod    
    def ParseTrunk(contentToParse,numToTrunk):
        result = contentToParse.get_text()
        result = result[:-numToTrunk]
        return result
        
    #Return string on 3 or 4 caracters depending on input
    @staticmethod    
    def ParseHour(contentToParse):
        return contentToParse[4 if contentToParse[3]==' ' else 3:]
     
    #Convert date
    @staticmethod    
    def convertDate(txtToParse):
        day = txtToParse[30:32]
        month = txtToParse[33:37].upper()
        yearIndex = txtToParse[37:].index('2')
        year = txtToParse[37+yearIndex:41+yearIndex]
        if (month=='JANV'):
            return day+'/01/'+year
        elif (month == 'FEVR'):
            return day+'/01/'+year
        elif (month == 'MARS'):
            return day+'/03/'+year
        elif (month == 'AVRI'):
            return day+'/04/'+year
        elif (month == 'MAI '):
            return day+'/05/'+year
        elif (month == 'JUIN'):
            return day+'/06/'+year
        elif (month == 'JUIL'):
            return day+'/07/'+year
        elif (month == 'AOUT'):
            return day+'/08/'+year
        elif (month == 'SEPT'):
            return day+'/09/'+year
        elif (month == 'OCTO'):
            return day+'/10/'+year
        elif (month == 'NOVE'):
            return day+'/11/'+year
        elif (month == 'DECE'):
            return day+'/12/'+year
        else: 
            print 'couldnt read month'
            return
     
    @staticmethod
    def removeSpecialCharacters(string):
        return re.sub('/|[\\\]|:|[\*]|[\?]|[\"]|<>|[\|]','',string)
    
    @staticmethod
    def formatData(dico):    
        for key in dico:
            #Set null values
            if (dico[key].replace(' ','').replace(u'\xa0', u'')=='') or ('--' in dico[key]) or ('-.' in dico[key]):
                dico[key] = DataParse.nullValue
            if dico[key][0] in ('+'):#,' '):
                dico[key] = dico[key][1:]
            #Deleting white spaces
            dico[key] = dico[key].replace(' ','')
     
    #get a list of station's urls from romma
    @staticmethod
    def getStations():
        urllist = {}
        urlStations = 'http://www.romma.fr/index.php'
        filehandleStations = urllib.urlopen(urlStations, proxies={})

        soupStations = BeautifulSoup(filehandleStations)
        iterStations = soupStations.find(id="menu")
        iterStations = iterStations.contents[1].next_sibling.next_sibling.contents[2].contents[1].contents[2].contents[1]

        while (iterStations<>None):
            i=1
            while (i<len(iterStations.contents[2].contents)):
                stationUrl = iterStations.contents[2].contents[i].contents[0]['href']
                stationName = iterStations.contents[2].contents[i].contents[0].contents[0].get_text()
                stationName = DataParse.removeSpecialCharacters(stationName)
                #stationName = stationName.replace(u'\xa0', u'')
                stationName = stationName.encode("ascii","ignore")
                i=i+2
                urllist[stationName] = stationUrl
            iterStations = iterStations.next_sibling.next_sibling
        return urllist
        
    #get the whole data from a particular station
    @staticmethod
    def getDatas(urlStation,debug):
        dico={}
        filehandle = urllib.urlopen(urlStation, proxies={})
        soup = BeautifulSoup(filehandle)
        
        #Tag h3
        iter=soup.find(id="affichage_simple").find_next('h3')
        #looking if recent data for the station
        if (iter.contents[1].contents[0].get_text()<>''):
            print('Most recent data are > 15 min, skipping')
            return dico
     
        #Day and Hour
        txtToParse = iter.get_text()
        obsDate = DataParse.convertDate(txtToParse)

        hourIndex = txtToParse[37:].index(':')
        obsHour = txtToParse[37+hourIndex-2:37+hourIndex+3]

        dico['obsDate'] = obsDate
        dico['obsHour'] = obsHour

        #Temperature / OneHourVarTemp / RainFromMidnight
        iter = iter.next_sibling.next_sibling.find_next('tr').next_sibling.next_sibling
        obsTemperature = iter.contents[1].contents[0].get_text()
        dico['obsTemperature'] = obsTemperature

        oneHourVarTemp = DataParse.ParseCut(iter.contents[3].contents[1],'C',2)
        dico['oneHourVarTemp'] = oneHourVarTemp
        
        rainDataAvailable = (len(iter.contents[5])>1)
        if (rainDataAvailable):
            rainFromMidnight = iter.contents[5].contents[1].get_text()
        else:
            rainFromMidnight = DataParse.nullValue
        dico['rainFromMidnight'] = rainFromMidnight

        #Delta Temperature 24h / min Temperature / Rain intensity
        iter = iter.next_sibling.next_sibling
        deltaTemp = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
        dico['deltaTemp'] = deltaTemp

        iter = iter.next_sibling.next_sibling
        minTemp = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
        dico['minTemp'] = minTemp

        if (rainDataAvailable):
            rainIntensity = DataParse.ParseCut(iter.contents[3].contents[1],'m',1)
        else:
            rainIntensity = DataParse.nullValue
        dico['rainIntensity'] = rainIntensity

        #Max Temperature from 0h / Max Rain Intensity from 0h
        iter = iter.next_sibling.next_sibling

        maxTemp = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
        dico['maxTemp'] = maxTemp
        
        if (rainDataAvailable):
            maxRainIntensity = DataParse.ParseCut(iter.contents[3].contents[1],'m',1)
        else:
            maxRainIntensity=DataParse.nullValue
        dico['maxRainIntensity'] = maxRainIntensity

        #Hour of max intensity?
        
        #Humidity / Pression
        iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling

        humidity = iter.contents[1].contents[0].get_text()
        dico['humidity'] = humidity

        pression = iter.contents[5].contents[0].get_text()
        dico['pression'] = pression

        #Rosee Point 
        iter = iter.next_sibling.next_sibling
        roseePoint = DataParse.ParseCut(iter.contents[1].contents[1],'C',2)
        dico['roseePoint'] = roseePoint

        #Pression Var (3h) 
        iter = iter.next_sibling.next_sibling
        if (len(iter.contents[3].contents)>1):
            pressionVarLastThreeHour=DataParse.ParseTrunk(iter.contents[3].contents[1],4)
            pressionVarLastThreeHour=pressionVarLastThreeHour[1 if pressionVarLastThreeHour[0]=='+' else 0:]
        else:
            pressionVarLastThreeHour=DataParse.nullValue
        dico['pressionVarLastThreeHour'] = pressionVarLastThreeHour

        #Min Humidity / Pression since midnight 
        #And hour of event
        iter = iter.next_sibling.next_sibling
        minHumidity=DataParse.ParseTrunk(iter.contents[1].contents[1],2)
        dico['minHumidity'] = minHumidity

        hourMinHumidity=DataParse.ParseHour(iter.contents[1].contents[2])
        dico['hourMinHumidity'] = hourMinHumidity

        if (len(iter.contents[3].contents)>1):
            minPression=DataParse.ParseTrunk(iter.contents[3].contents[1],4)
            hourMinPression=DataParse.ParseHour(iter.contents[3].contents[2])
        else:
            minPression=DataParse.nullValue
            hourMinPression=DataParse.nullValue
            
        dico['minPression'] = minPression
        dico['hourMinPression'] = hourMinPression

        #Max Humidity / Pression since midnight
        #And hour of event
        iter = iter.next_sibling.next_sibling
        maxHumidity = DataParse.ParseTrunk(iter.contents[1].contents[1],2)
        dico['maxHumidity'] = maxHumidity

        hourMaxHumidity=DataParse.ParseHour(iter.contents[1].contents[2])
        dico['hourMaxHumidity'] = hourMaxHumidity

        if (len(iter.contents[3].contents)>1):
            maxPression=DataParse.ParseTrunk(iter.contents[3].contents[1],4)
            hourMaxPression=DataParse.ParseHour(iter.contents[3].contents[2])
        else:
            maxPression=DataParse.nullValue
            hourMaxPression=DataParse.nullValue
        dico['maxPression'] = maxPression

        dico['hourMaxPression'] = hourMaxPression

        #Sun
        iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        findSun = iter.contents[1].contents[1]
        sun = findSun.get_text()
        dico['sun'] = sun

        #max Sun / wind chill Temperature
        iter = iter.next_sibling.next_sibling
        if (iter.contents[1].contents[1].get_text()[0]=='S'):
            maxSun = DataParse.nullValue
        else:
            maxSun=DataParse.ParseCut(iter.contents[1].contents[1],'w',1)
        dico['maxSun'] = maxSun

        windChillTemp = iter.contents[3].contents[1].get_text()
        dico['windChillTemp'] = windChillTemp

        #Average Wind
        iter = iter.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        avgWind = iter.contents[1].contents[1].get_text()
        dico['avgWind'] = avgWind

        #TODO rose des vents ?

        #Direction
        iter = iter.next_sibling.next_sibling.next_sibling.next_sibling
        windDirection = iter.contents[1].contents[1].get_text()
        dico['windDirection'] = windDirection

        #Max Wind last 10 min
        iter = iter.next_sibling.next_sibling
        maxWindLastTen = DataParse.ParseCut(iter.contents[1].contents[1],'k',1)
        dico['maxWindLastTen'] = maxWindLastTen

        #Max Wind since midnight / Hour
        iter = iter.next_sibling.next_sibling
        maxWindMidnight = DataParse.ParseCut(iter.contents[1].contents[1],'k',1)
        dico['maxWindMidnight'] = maxWindMidnight

        maxWindHour=DataParse.ParseHour(iter.contents[1].contents[2])
        dico['maxWindHour'] = maxWindHour
        
        DataParse.formatData(dico)
        
        if debug:
            print('obsDate : '+obsDate)
            print('obsHour : '+obsHour)
            print('obsTemperature : '+obsTemperature)
            print('oneHourVarTemp : '+oneHourVarTemp)

            print('rainFromMidnight : '+rainFromMidnight)
            print('deltaTemp : '+deltaTemp)
            print('minTemp : '+minTemp)
            print('rainIntensity : '+rainIntensity)
            print('maxTemp : '+maxTemp)
            print('maxRainIntensity : '+maxRainIntensity)
            print('humidity : '+humidity)
            print('pression : '+pression)
            print('roseePoint : '+roseePoint)
            print('pressionVarLastThreeHour : '+pressionVarLastThreeHour)
            print('minHumidity : '+minHumidity)
            print('hourMinHumidity : '+hourMinHumidity)
            print('minPression : '+minPression)
            print('hourMinPression : '+hourMinPression)
            print('maxHumidity : '+maxHumidity)
            print('hourMaxHumidity : '+hourMaxHumidity)
            print('maxPression : '+maxPression)
            print('hourMaxPression : '+hourMaxPression)
            print('sun : '+sun)
            print('maxSun : '+maxSun)
            print('windChillTemp : '+windChillTemp)
            print('avgWind : '+avgWind)
            print('windDirection : '+windDirection)
            print('maxWindLastTen : '+maxWindLastTen)
            print('maxWindMidnight : '+maxWindMidnight)
            print('maxWindHour : '+maxWindHour)
            
        return dico

    ###################################
    #methods used to load data from MF#
    ###################################
    
    #get BRA for a particular department, essentially gathering risk value
    @staticmethod
    def getBRADept(deptNumber,debug):
        urlDept = DataParse.braMainUrl+str(deptNumber)
        filehandleBra = urllib.urlopen(urlDept, proxies={})
        soupBra = BeautifulSoup(filehandleBra)
        return
