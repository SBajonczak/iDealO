from asyncio import sleep
import random
import requests
from bs4 import BeautifulSoup
import threading
import concurrent.futures
from datetime import datetime
from Offer import Offer
from Toolkits import priceStringtoFload, priceStringtoFload
from Discorder import Discorder
from WhatsApp import WhatsApp
from AzureDatabase import AzureDataBase

class IdealoParser:
    
    def __init__(self,database: AzureDataBase, discorder:Discorder, category:str=""):
        self.Category=category
        self.Database:AzureDataBase =database
        self.Discorder=discorder

    @property
    def getHeader(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Microsoft Edge\";v=\"134\"",
        }
    
    def getDestinationShopWithFollowLink(self,inputUrl):
        header= {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Microsoft Edge\";v=\"134\"",
        }
        url = f"https://www.idealo.de{inputUrl}"
        try:
            responseDetails =  requests.get(url, headers=header, allow_redirects=True)
            return responseDetails.url
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


    def getLinkAndPrice(self,offerDetails:Offer)->Offer:
        responseDetails = self.performRequest(offerDetails.IdealoUrl)
        # requests.get(offerDetails.IdealoUrl, headers=self.getHeader)
        if responseDetails.status_code == 200:
            soupDetails = BeautifulSoup(responseDetails.content, 'html.parser')
            offer_list = soupDetails.find(id="offer-list-with-pagination")

            ## Get Image
            if soupDetails.find(id="slide-0")!= None:
                img= soupDetails.find(id="slide-0").find("img")["src"]
                offerDetails.ImageUrl= f"https:{img}"
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
                offerDetails.shopRelocationUrl=relocateUrlhRef

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
            # Getting both urls 
            if (offerDetails.amazonRelocationUrl != ""):
                offerDetails.amazonShopUrl = self.getDestinationShopWithFollowLink(offerDetails.amazonRelocationUrl) + "&tag=saschabajoncz-21"
            if (offerDetails.ebayRelocationUrl != ""):
                offerDetails.ebayShopUrl = self.getDestinationShopWithFollowLink(offerDetails.ebayRelocationUrl)

            offerDetails.shopUrl = self.getDestinationShopWithFollowLink(relocateUrlhRef)
    
            return offerDetails
        




    async def processElement(self,element)->Offer:
        offer= Offer()
        
        title = element.find("div", {"data-testid": "productSummary__title"}).text.strip()
        print("Fetching product ", title)
        if element.find("a", {"data-testid": "link"}) != None:
            offer.IdealoUrl = element.find("a", {"data-testid": "link"})['href']
        offer.Category=self.Category
        offer.ProductName=title
        offerData= self.getLinkAndPrice(offer)
        offerData.ProductName = title
        waitTime = random.uniform(30, 300)

        if offerData.isAmazonAvailable():
            existingOffer = self.Database.getElementByIdealoUrl(offerData.IdealoUrl)
            if existingOffer is None:
                ## Wenn nicht exisitert und ein Amazon link verfügbar ist, 
                ## dann speicher den Eintrag
                self.Database.UpsertDb(offerData)
                ## Emittle den eintrag noch mal um die ID zu bekommen 
                existingOffer = self.Database.getElementByIdealoUrl(offerData.IdealoUrl)
                ## erstelle Historien eintrag
                self.Database.CreatePriceHistoryEntry(existingOffer, offerData)
                ## Sende an discord
                if offerData.HashMinimumMargin(12):
                    print(f"Send to Basic the price differ stored price {existingOffer.price} new price {float(offer.price.real)}")
                    self.Discorder.sendToPremium(offerData)
                else:
                    if offerData.HashMinimumMargin(1):
                        self.Discorder.sendToBasic(offerData)
                await sleep(waitTime)
            ## Wenn ein Eintrag existiert UND preise unterschiedlich sind
            elif existingOffer is not None and existingOffer.price is not None and offerData.price != float(existingOffer.price.real):
                ## Aktualisiere den Preis
                self.Database.UpsertDb(offerData)
                ## Erstelle ein Historien Eintrag
                self.Database.CreatePriceHistoryEntry(existingOffer, offerData)
                ## Send an discord
                print(f"Item was processed, waiting now {waitTime}")
                if offerData.HashMinimumMargin(12):
                    print(f"Send to Basic the price differ stored price {existingOffer.price} new price {float(offer.price.real)}")
                    self.Discorder.sendToPremium(offerData)
                else:
                    if offerData.HashMinimumMargin(1):
                        self.Discorder.sendToBasic(offerData)
                await sleep(waitTime)
        else:
            ## Benhandle alle anderen Fälle die nicht amazon spezifisch sind
            fetchedOfferFromDB = self.Database.getElementByIdealoUrl(offerData.IdealoUrl)
            ## Is noch kein Eintrag vorhanden?
            if (fetchedOfferFromDB is None):
                ## erstelle ein Eintrag
                self.Database.UpsertDb(offerData)
                ## Hole element noch mal aus DB
                fetchedOfferFromDB= self.Database.getElementByIdealoUrl(offerData.IdealoUrl)
                ## Speicher historien Eintrag
                self.Database.CreatePriceHistoryEntry(fetchedOfferFromDB, offerData)
            else:
                if offerData.price != float(fetchedOfferFromDB.price.real):
                    ## Speicher historien Eintrag
                    self.Database.CreatePriceHistoryEntry(fetchedOfferFromDB, offerData)
                    # if offerData.HashMinimumMargin(12):
                    #     print(f"Send to Basic the price differ stored price {existingOffer.price} new price {float(offer.price.real)}")
                    #     self.Discorder.sendToPremium(offerData)
                    # else:
                    #     if offerData.HashMinimumMargin(1):
                    #         self.Discorder.sendToBasic(offerData)
                    # await sleep(waitTime)

        
        return offerData
    
    def performRequest(self,url):
        response = requests.get(url, headers=self.getHeader)#, allow_redirects=True) 
        if response.status_code == 200:
            return response
    

    def getOfferDetails(self, url:str) -> list:
        data = []
        response = self.performRequest(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all(attrs={"data-testid": "resultItemLink"})
            for currentLink in links:
                data.append(currentLink)
        else:
            print(f"Fehler: {response.status_code}")
        return data