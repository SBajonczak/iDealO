import datetime
from decimal import Decimal
import re
import Offer 

class CrawlingPage:

    def __init__(self, id:int,category: str = "", title: str = "", shopUrl: str = "", shopType: int = 0, crawledAt: datetime.datetime = None, isActive: bool = True, created: datetime.datetime = None, updated: datetime.datetime = None, crawledAmount:int=0):
        self.id = id
        self.category = category
        self.title = title
        self.shopUrl = shopUrl
        self.shopType = shopType
        self.crawledAt = crawledAt if crawledAt else datetime.datetime.now()
        self.isActive = isActive
        self.created = created if created else datetime.datetime.now()
        self.updated = updated if updated else datetime.datetime.now()
        self.crawledAmount=crawledAmount
        self.ShopUrls=[]

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def shopUrl(self):
        return self._shopUrl

    @shopUrl.setter
    def shopUrl(self, value):
        self._shopUrl = value

    @property
    def shopType(self):
        return self._shopType

    @shopType.setter
    def shopType(self, value):
        self._shopType = value

    @property
    def crawledAt(self):
        return self._crawledAt

    @crawledAt.setter
    def crawledAt(self, value):
        self._crawledAt = value

    @property
    def isActive(self):
        return self._isActive

    @isActive.setter
    def isActive(self, value):
        self._isActive = value

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, value):
        self._created = value

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, value):
        self._updated = value

        

class Offer:
    keepaAccessKey=""
    amazonDomainForGermany=3

    def __init__(self,bsr:str="", id :int=0,  category:str="",imageUrl:str="", ASIN:str="",idealoUrl:str="", ProductName:str= "", storeName: str="", price: float = 0, amazonPrice: float = 0, ebayPrice: float = 0, shopUrl:str="", amazonShopUrl:str="", ebayShopUrl:str=""):
        self.ID=id
        self.BSR=bsr
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
    
    def IsDifferentTo(self, offer:Offer)->bool:
        return self.price != float(offer.price)
    
    def HashMinimumMargin(self, margin):
         return self.getHighestMargin() >=margin
        
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
    
    def getEbayIdFromLink(self)->str:
        ident = re.search(r'(?:[ebay]*(?:[\/]|[itm=])|^)([0-9]{9,12})', self.ebayShopUrl, flags=re.IGNORECASE)
        if ident:
            return ident.group(1)
        return None

    def isAmazonAvailable(self)->bool:
        return self.getAsinFromAmazon()!=None

    def isEbayAvailable(self)->bool:
        return self.getEbayIdFromLink()!=None


    def getKeepaLink(self):
        asin= self.getAsinFromAmazon()
        if asin!=None:
            return f"https://api.keepa.com/graphimage?key={self.keepaAccessKey}&domain={self.amazonDomainForGermany}&asin={asin}"
        

    def __repr__(self):
        return (f"Offer(shop_name='{self.shop_name}', url='{self.url}', price='{self.price}', "
                f"relocation_url='{self.relocation_url}')")
