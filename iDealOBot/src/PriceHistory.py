
import datetime

class PriceHistory:
    
    def __init__(self,id:int=0,fkpriceid:int=0,  ASIN:str="", ProductName:str= "", storeName: str="", price: float = 0,created:datetime.datetime = datetime.datetime.now()):
        self.ID=id
        self.fkpriceid=fkpriceid
        self.ASIN=ASIN
        self.ProductName = ProductName
        self.StoreName = storeName
        self.price = price
        self.created =created
    