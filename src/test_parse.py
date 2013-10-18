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
month = txtToParse[33:36]
year = '0'
print(day+' '+month+' '+year)








#save to file