#!/bin/python

from bs4 import BeautifulSoup
import urllib
from dataParse import DataParse 

#gather every station from url
urlStations = 'http://www.romma.fr/index.php'

urllist = DataParse.getStations()

#Le versoud
#url = 'http://www.romma.fr/station_24.php?id=%206'
#url = 'http://www.romma.fr/station_24.php?id=%2066'
url = 'http://www.romma.fr/station_24.php?id=%2072'




#########################
#                       #
#   COLLECT RAW DATAS   #
#                       #
#########################

dico = DataParse.getDatas(url)

for stationName in urllist:
    DataParse.getDatas(urllist[stationName])

#####################
#                   #
#   SAVE TO FILES   #
#                   #
#####################