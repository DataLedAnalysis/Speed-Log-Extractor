from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

Fourline_html = urlopen(r'http://10.2.30.240/4Line/4LineSPD2.asp?S_Day=22&S_Month=March&S_Year=2023&S_Hour=07&S_Min=00&E_Day=23&E_Month=March&E_Year=2023&E_Hour=11&E_Min=21&B1=Search')

soup = bs(Fourline_html)

tableCells = soup.find_all('tr',attrs={'class':['TableCell1','TableCell2']})

dirtyData = []

for tr in tableCells:
    tds = tr.find_all('td')
    for td in tds:
        dirtyData.append(td.text)

cleanData = [dirtyData[x:x+13] for x in range(0,len(dirtyData),13)]
print(cleanData)













