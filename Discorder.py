import requests
from Offer import Offer


def send_to_discord(dealData:Offer):
    webhook_url = 'https://discord.com/api/webhooks/1344760020092588093/1TQWHQU9h9lv13zsGwBTQa5ail_LVRQnFo2i1tXz6FNCC51kK2IIPYghZg9j5j20R4Yc'
    headers = {
        'Content-Type': 'application/json',
    }
   
    message = {
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
                        "value": f"[**€{dealData.price}**]({dealData.shopUrl})",
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

    if dealData.ebayPrice > 0:
        message["embeds"][0]["fields"].append({
            "name": f"🛒 sell on {dealData.getShopNameWithTheHighestMargin()}",
            "value": f"[**€{round(dealData.getPriceWithTheHighestRate(),2)}**]({dealData.getCheapestShopUrl()})",
            "inline": True
        })
        message["embeds"][0]["fields"].append({
            "name": "💰 Profit",
            "value": f"Marge: **{round(dealData.getHighestMargin(), 2)}%** - Profit: **€{round(dealData.getProfitInEur(),2)}**",
            "inline": True
        })
        message["embeds"][0]["fields"].append({
            "name": "🔍 Tools",
            "value": "[SAS](https://example.com/sas) | [BBP](https://example.com/bbp) | [A1](https://example.com/a1)",
            "inline": False
        })
    
    response = requests.post(webhook_url, headers=headers, json=message)
    if response.status_code != 204:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")
