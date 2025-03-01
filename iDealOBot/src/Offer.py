import datetime
import re

class Offer:
    keepaAccessKey=""
    amazonDomainForGermany=3

    def __init__(self,category:str="",imageUrl:str="", ASIN:str="",idealoUrl:str="", ProductName:str= "", storeName: str="", price: float = 0, amazonPrice: float = 0, ebayPrice: float = 0, shopUrl:str="", amazonShopUrl:str="", ebayShopUrl:str=""):
        self.ASIN=ASIN
        self.Category=category
        self.ImageUrl=imageUrl
        self.IdealoUrl=idealoUrl
        self.ProductName = ProductName
        self.StoreName = storeName
        self.price = price
        self.amazonPrice = amazonPrice
        self.ebayPrice = ebayPrice
        self.shopUrl=shopUrl
        self.amazonShopUrl=amazonShopUrl
        self.ebayShopUrl=ebayShopUrl
        self.amazonRelocationUrl = ""
        self.ebayRelocationUrl = ""
        self.shopRelocationUrl = ""
    
    def hasMarketPrices(self)-> bool:
        if self.amazonPrice >0 and self.ebayPrice >0:
            return True
        return False

    @property
    def amazonDifference(self):
        if self.amazonPrice and self.price:
            return ((self.amazonPrice - self.price) / self.price) * 100
        return 0

    @property
    def ebayDifference(self):
        if self.ebayPrice and self.price:
            return ((self.ebayPrice - self.price) / self.price) * 100
        return 0
    
    def HashMinimumMargin(self, margin):
         return self.getShopNameWithTheHighestMargin() >=margin
        
    def getShopNameWithTheHighestMargin(self):
        if self.amazonDifference >self.ebayDifference:
            return "amazon"
        return "eBay"

    def getHighestMargin(self):
        if self.amazonDifference >self.ebayDifference:
            return self.amazonDifference
        return self.ebayDifference

    def getProfitInEur(self):
        return self.getPriceWithTheHighestRate()-self.price

    def getCheapestShopUrl(self):
        if self.amazonDifference >self.ebayDifference:
            return self.amazonShopUrl
        return self.ebayShopUrl
    
    def getPriceWithTheHighestRate(self):
        if self.amazonPrice >self.ebayPrice:
            return self.amazonPrice
        return self.ebayPrice

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%H:%M")

    def getAsinFromAmazon(self)->str:
        asin = re.search(r'\/[dg]p\/([\w.]+)', self.amazonShopUrl, flags=re.IGNORECASE)
        if asin:
            return asin.group(1)
        return None

    def isAmazonAvailable(self)->bool:
        return self.getAsinFromAmazon()!=None

    def getKeepaLink(self):
        asin= self.getAsinFromAmazon()
        if asin!=None:
            return f"https://api.keepa.com/graphimage?key={self.keepaAccessKey}&domain={self.amazonDomainForGermany}&asin={asin}"
        

    def __repr__(self):
        return (f"Offer(shop_name='{self.shop_name}', url='{self.url}', price='{self.price}', "
                f"relocation_url='{self.relocation_url}')")
