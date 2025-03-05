import requests
from Offer import Offer
from Plotter import Plotter
from AzureDatabase import AzureDataBase
import os

class Discorder:
    def __init__(self,database:AzureDataBase, webhookUrl:str="", webHookPremiumUrl:str="" ):
        self.db= database
        self.WebhookUrl=webhookUrl
        self.WebHookPremiumUrl=webHookPremiumUrl

    def generateMessage(self,dealData:Offer):
        message= {
            "username": "iDealOBot",
    #        "avatar_url": "https://blog.bajonczak.com/content/images/2022/10/20221014_171637.png",
            "embeds": [
                {
                    "title": dealData.StoreName,
                    "description": f"**{dealData.ProductName}**",
                    "color": 16750848,
                    "thumbnail": {
                        "url": f"{dealData.ImageUrl}"
                    },
                    "fields": [
                        {
                            "name": f"Stand {dealData.getCurrentTime()}",
                            "value": f"**€{dealData.price}** [zum Shop]({dealData.shopUrl})",
                            "inline": False
                        },
                        
                    ],
                    "footer": {
                    "text": "der Sascha",
                    "icon_url": "https://blog.bajonczak.com/content/images/2022/10/20221014_171637.png"
                }
                }
            ]
        }
        if dealData.ebayPrice > 0 or dealData.amazonPrice > 0:
            message["embeds"][0]["fields"].append({
                "name": f"🛒 sell on {dealData.getShopNameWithTheHighestMargin()}",
                "value": f"**€{round(dealData.getPriceWithTheHighestRate(),2)}** [zum Shop]({dealData.getCheapestShopUrl()})",
                "inline": True
            })
            if dealData.BSR != None:
                message["embeds"][0]["fields"].append({
                    "name": f"BSR",
                    "value": f"**{dealData.BSR}**",
                    "inline": True
                })
            message["embeds"][0]["fields"].append({
                "name": "💰 Profit",
                "value": f"Marge: **{round(dealData.getHighestMargin(), 2)}%** - Profit: **€{round(dealData.getProfitInEur(),2)}**",
                "inline": True
            })
        return message


    def sendToBasic(self, dealData:Offer):
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(self.WebhookUrl, headers=headers, json=self.generateMessage(dealData))
        if response.status_code != 204:
            print(f"Failed to send message to Discord: {response.status_code}, {response.text}")

    def sendToPremium(self, dealData:Offer):
        p= Plotter(self.db)
        filename=p.plot(dealData.ID)

        headers = {
                'Content-Type': 'application/json',
            }
        response = requests.post(self.WebHookPremiumUrl, headers=headers, json=self.generateMessage(dealData))
        if response.status_code != 204:
            print(f"Failed to send message to Discord: {response.status_code}, {response.text}")

        # plotting files
        p= Plotter(self.db)
        filename=p.plot(dealData.ID)

        if filename!="" and filename!=None:
            with open(filename, "rb") as file:
     
                files = {"file": file}
                response = requests.post(self.WebHookPremiumUrl, json=self.generateMessage(dealData), files=files)
                # response = requests.post(self.WebHookPremiumUrl, files=files, data={"payload_json": self.generateMessage(dealData)})
            if response.status_code != 204:
                print(f"Failed to send message to Discord: {response.status_code}, {response.text}")
        
            if os.path.exists(filename):
                os.remove(filename)
