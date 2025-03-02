from asyncio import sleep
from Discorder import Discorder
from IdealoParser import IdealoParser
from AzureDatabase  import AzureDataBase
from Offer import CrawlingPage
import os
import random
import asyncio

from Plotter import Plotter

urls=[]



result=[]

webhook = os.getenv('WEBHOOK','')
premiumWebhook = os.getenv('PREMIUM_WEBHOOK','')
connection_string = os.getenv('AZURE_SQL_CONNECTION_STRING','DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sbadbprod.database.windows.net,1433;DATABASE=sba-dealz-db;UID=sbaadmin;PWD==S?p86`YCYjo*7TNc~[S') 
category = os.getenv('CATEGORY','Modellbau')
database = AzureDataBase(connection_string)
database.createTableIfNotExists()

data= database.createPriceHistoryBypriceId(64)
p= Plotter(data)
p.plot()

shopstoCrawl= database.getActivesCrawlingPagesbyCategory(category)
print(f"Found {len(shopstoCrawl)} shops to crawl for category {category}")

discord=Discorder(webhook,premiumWebhook)
idealo= IdealoParser(database, discord, category)
## Fetch item urls first
async def main():
    for urlItem in shopstoCrawl:
        print(f"Processing {urlItem.title}")
        data=idealo.getOfferDetails(urlItem.shopUrl)
        result.extend([(urlItem, offer) for offer in data])
    ## Shuffle the results to generate random posts
    random.shuffle(result)    


    # Now iterate
    for urlItem in result:
        await idealo.processElement(urlItem[1])

    for urlItem in shopstoCrawl:
        urlItem.crawledAmount = sum(1 for item in result if item[0].category == urlItem.category)
        database.updateCrawlingPageWithAmountOfCrawledItems(urlItem)

if __name__ == "__main__":
    asyncio.run(main())

