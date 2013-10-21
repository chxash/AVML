#!/bin/python

from bs4 import BeautifulSoup
import urllib
from dataParse import DataParse 

#gather every station from url
urlStations = 'http://www.romma.fr/index.php'

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
    DataParse.getDatas(urllist[stationName])
    