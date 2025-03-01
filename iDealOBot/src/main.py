from asyncio import sleep
from Discorder import Discorder
from IdealoParser import IdealoParser
from AzureDatabase  import createTableIfNotExists
import os
import random
import asyncio

urls=[]



result=[]
idealourls = os.getenv('IDEALO_URLS', 'https://www.idealo.de/preisvergleich/ProductCategory/26151.html,https://www.idealo.de/preisvergleich/ProductCategory/18817.html,https://www.idealo.de/preisvergleich/ProductCategory/25515.html')
idealoUrlsSplitted= idealourls.split(",")
webhook = os.getenv('WEBHOOK','')
premiumWebhook = os.getenv('PREMIUM_WEBHOOK','')

category = os.getenv('category','')
print(f"connection: {os.getenv('AZURE_SQL_CONNECTION_STRING')}")
createTableIfNotExists()
if len(idealoUrlsSplitted) > 0:
    for idealourl in idealoUrlsSplitted:
        urls.append({"webhook": webhook, "category": category, "url": idealourl})

discord=Discorder(webhook,premiumWebhook)
## Fetch item urls first
async def main():
    for urlItem in urls:
        idealo= IdealoParser(discord, category)
        data=idealo.getOfferDetails(urlItem.get("url"))
        result.extend(data)

    ## Shuffle the results
    random.shuffle(result)    
    for urlItem in result:
        idealo= IdealoParser(discord, category)
        data=idealo.processElement(urlItem)
        waitTime = random.uniform(60, 300)
        print(f"Item was processed, waiting now {waitTime}")
        await sleep(waitTime)

if __name__ == "__main__":
    asyncio.run(main())

