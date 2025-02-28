import requests
from bs4 import BeautifulSoup
import threading
import concurrent.futures
from datetime import datetime
from Offer import Offer
from Toolkits import priceStringtoFload
from Database import UpsertDb, getElementByASIN
from Discorder import send_to_discord


class IdealoParser:
    
   
   
    
    def __init__(self,entryUrl:str=""):
        self.EntryUrl=entryUrl
    @property
    def getHeader(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Microsoft Edge\";v=\"134\"",
        }
    
    def getDestinationShopWithFollowLink(self,inputUrl):
        headers= {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Microsoft Edge\";v=\"134\"",
        }
        responseDetails = requests.get(f"https://www.idealo.de{inputUrl}", headers=headers, allow_redirects=True)
        return responseDetails.url


    def getLinkAndPrice(self,offerDetails:Offer)->Offer:
        responseDetails = requests.get(offerDetails.IdealoUrl, headers=self.getHeader)
        if responseDetails.status_code == 200:
            soupDetails = BeautifulSoup(responseDetails.content, 'html.parser')
            offer_list = soupDetails.find(id="offer-list-with-pagination")
            if soupDetails.find("img", class_="oopStage-galleryCollageImage")!= None:
                img=soupDetails.find("img", class_="oopStage-galleryCollageImage")["src"]
                offerDetails.ImageUrl= f"https:{img}"

            if offer_list:
                offer_items = offer_list.find_all(class_="productOffers-listItem")
                # list was sorted descending
                offerDetails.StoreName =  offer_items[0].find("a", class_="productOffers-listItemOfferShopV2LogoLink")['data-shop-name']
                price= offer_items[0].find("div", class_="productOffers-listItemOfferShippingDetails").text.strip()
                
                
                offerDetails.price= priceStringtoFload(price)
                
                relocateUrlhRef = offer_items[0].find("a", class_="productOffers-listItemOfferCtaLeadout")['href']
                offerDetails.shopUrl = self.getDestinationShopWithFollowLink(relocateUrlhRef)

                ## find out if amazon is available
                for offer_item in offer_items:
                    amazon = "Amazon" in offer_item.find("a", class_="productOffers-listItemOfferShopV2LogoLink")['data-shop-name']
                    ebay = "eBay" in offer_item.find("a", class_="productOffers-listItemOfferShopV2LogoLink")['data-shop-name']
                    if amazon and offerDetails.amazonRelocationUrl=="":
                        ## Todo dupplicate code remove
                        offerDetails.amazonRelocationUrl = offer_item.find("a", class_="productOffers-listItemOfferCtaLeadout")['href']
                        # amazon_price = offer_item.find("a", class_="productOffers-listItemOfferPrice").text.strip()
                        amazon_price = offer_item.find("div", class_="productOffers-listItemOfferShippingDetails").text.strip()
                        offerDetails.amazonPrice= priceStringtoFload(amazon_price)
                    if ebay and offerDetails.ebayRelocationUrl=="":
                        offerDetails.ebayRelocationUrl = offer_item.find("a", class_="productOffers-listItemOfferCtaLeadout")['href']
                        ebay_price = offer_item.find("div", class_="productOffers-listItemOfferShippingDetails").text.strip()
                        offerDetails.ebayPrice= priceStringtoFload(ebay_price)
            
                    if offerDetails.hasMarketPrices():
                        break
            if offerDetails.getShopNameWithTheHighestMargin()=="amazon":
                offerDetails.amazonShopUrl = self.getDestinationShopWithFollowLink(offerDetails.amazonRelocationUrl) + "&tag=saschabajoncz-21"
            else:
                offerDetails.ebayShopUrl = self.getDestinationShopWithFollowLink(offerDetails.ebayRelocationUrl)
                
            return offerDetails
        




    def process_element(self,element)->Offer:
        title = element.find("div", {"data-testid": "productSummary__title"}).text.strip()
        print("Fetching product ", title)
        link = element.find("a", {"data-testid": "link"})['href']
        
    
        offer= Offer()
        offer.IdealoUrl=link
        offer.ProductName=title

        offerData= self.getLinkAndPrice(offer)
        offerData.ProductName = title


        if offerData.isAmazonAvailable():
            existingOffer = getElementByASIN(offerData.getAsinFromAmazon())
            if existingOffer is None or offerData.price != existingOffer.price:
                UpsertDb(offerData)
                if offerData.HashMinimumMargin(5):
                    send_to_discord(offerData)
        return offerData

    def getOffers(self) -> list[Offer]:
        data = []
        response = requests.get(self.EntryUrl, headers=self.getHeader)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.find_all(attrs={"data-testid": "resultItemLink"})
            for currentElement in elements:
                data.append(self.process_element(currentElement))
        else:
            print(f"Fehler: {response.status_code}")
        return data