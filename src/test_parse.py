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

#print(soup.prettify())

#affichage simple
#print(soup.find(id="affichage_simple"))
#print(soup.find_all(text="Delta en 24h : "))
h3=soup.find(id="affichage_simple").find_next("h3")

txtToParse = h3.get_text()

#collect raw datas
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
    obsDate = day+'/02/'+year
else: 
    print 'couldnt read month'

hourIndex = txtToParse[37:].index(':')
obsHour = txtToParse[37+hourIndex-2:37+hourIndex+3]

print(obsDate)
print(obsHour)







#save to file