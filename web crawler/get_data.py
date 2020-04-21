# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 19:24:02 2020

@author: Milad
"""


"""
install the following libraries
$ pip install beautifulsoup4
$ pip install lxml

"""


import pandas as pd
from bs4 import BeautifulSoup
import requests
page = requests.get("https://www.worldometers.info/coronavirus/")
soup = BeautifulSoup(page.content, 'html.parser')
table =soup.find_all('table')[0]
rows = table.find_all('tr')
columns = rows[0].find_all('th')
data = {}
header = []
for column in columns:
    header.append(column.get_text())
    data[column.get_text()]=[]
for row in rows[1:]:
    col = row.find_all('td')
    for i in range(len(header)):
        t = col[i].get_text()
        data[header[i]].append(t)
csv_d = pd.DataFrame.from_dict(data)
csv_d.to_csv('test.csv')
