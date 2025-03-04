from asyncio import sleep
from Discorder import Discorder
from IdealoParser import IdealoParser
from AzureDatabase  import AzureDataBase
from Offer import CrawlingPage
import os




import random
import asyncio
from  Amazon import Amazon
from Plotter import Plotter

urls=[]




result=[]

webhook = os.getenv('WEBHOOK')
premiumWebhook = os.getenv('PREMIUM_WEBHOOK')
connection_string = os.getenv('AZURE_SQL_CONNECTION_STRING') 
category = os.getenv('CATEGORY','Wildtiere')

amazon_access = os.getenv('AMAZON_SECRET')
amazon_secret= os.getenv('AMAZON_ACCESS')
database = AzureDataBase(connection_string)
database.createTableIfNotExists()

amazon = Amazon(amazon_access,amazon_secret)

shopstoCrawl= database.getActivesCrawlingPagesbyCategory(category)
print(f"Found {len(shopstoCrawl)} shops to crawl for category {category}")

discord=Discorder(database, webhook,premiumWebhook)
idealo= IdealoParser(amazon,database, discord, category)
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

