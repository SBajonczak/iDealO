import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import sqlite3
import threading
from datetime import datetime
from Offer import Offer
from Database import UpsertDb,  createTableIfNotExists,getElementByASIN
from Discorder import send_to_discord

from IdealoParser import IdealoParser



urls=[]
## Heimwerken
#urls.append("https://www.idealo.de/preisvergleich/SubProductCategory/6812.html")
# ## festplattn
urls.append("https://www.idealo.de/preisvergleich/ProductCategory/14613.html")
# ## kopfhörer
urls.append("https://www.idealo.de/preisvergleich/ProductCategory/2520.html")
# ## Lego
urls.append("https://www.idealo.de/preisvergleich/ProductCategory/9552.html")
# ## Sammelkarten
urls.append("https://www.idealo.de/preisvergleich/ProductCategory/18448.html")

result=[]
createTableIfNotExists()

for url in urls:
    idealo= IdealoParser(url)
    data=idealo.getOffers()
    result.extend(data)
