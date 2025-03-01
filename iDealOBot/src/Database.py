import sqlite3
from Offer import Offer

#DatabasePath="D:\sourcen\Angebots\prices_data.db"
DatabasePath="prices_data.db"

def getElementByTitle(title)->Offer:
    conn = sqlite3.connect(DatabasePath)
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT ASIN, title, price, 
                   amazon_price,amazon_difference,ebay_price, 
                   ebay_difference, link,shop_name,
                   amazon_shop_Url,ebay_shop_Url,shopUrl
                   FROM prices WHERE title = ? ''', (title,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Offer(
            ASIN=row[0], ProductName=row[1], price=row[2],
            amazonPrice=row[3], ebayPrice=row[5],idealoUrl=row[7],storeName=row[8],
            amazonShopUrl=row[9], ebayShopUrl=row[10], shopUrl=row[11]
        )
    return None


def getElementByASIN(asin)->Offer:
    conn = sqlite3.connect(DatabasePath)
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT 
                   ASIN, title, price, 
                   amazon_price,amazon_difference,ebay_price, 
                   ebay_difference, link,shop_name,
                   amazon_shop_Url,ebay_shop_Url,shopUrl
                   FROM prices WHERE ASIN = ? ''', (asin,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Offer(
            ASIN=row[0], ProductName=row[1], price=row[2],
            amazonPrice=row[3], ebayPrice=row[5],
            idealoUrl=row[7],storeName=row[8],
            amazonShopUrl=row[9], ebayShopUrl=row[10], shopUrl=row[11]
        )
    return None


def UpsertDb(currentOfferData:Offer):
    databaseElement= getElementByTitle(currentOfferData.ProductName)
    conn = sqlite3.connect(DatabasePath)
    cursor = conn.cursor()
    
    if databaseElement is None:
        cursor.execute('''
        INSERT INTO prices (
            ASIN,
            title, 
            price, 
            amazon_price, 
            amazon_difference, 
            ebay_price, 
            ebay_difference, 
            link,
            shop_name,
            shopUrl,
            amazon_shop_Url,
            ebay_shop_Url,Category)
        VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?)
        ''', (currentOfferData.getAsinFromAmazon(), 
              currentOfferData.ProductName, 
              currentOfferData.price, 
              currentOfferData.amazonPrice, 
              currentOfferData.amazonDifference, 
              currentOfferData.ebayPrice,
              currentOfferData.ebayDifference, 
              currentOfferData.IdealoUrl,
              currentOfferData.StoreName,
              currentOfferData.shopUrl, 
              currentOfferData.amazonShopUrl,
              currentOfferData.ebayShopUrl,
              currentOfferData.Category))
    else:
        cursor.execute('''
        UPDATE prices
        SET price = ?, amazon_price = ?, amazon_difference = ?, ebay_price = ?, ebay_difference = ?, link = ?, updated = CURRENT_TIMESTAMP
        WHERE title = ?
        ''', (currentOfferData.price, currentOfferData.amazonPrice, currentOfferData.amazonDifference,  currentOfferData.ebayPrice,currentOfferData.ebayDifference, currentOfferData.shopUrl,currentOfferData.StoreName ))

    # Commit the tranfprintsaction
    conn.commit()
    conn.close()
    return databaseElement

def createTableIfNotExists():
    conn = sqlite3.connect(DatabasePath)
    cursor = conn.cursor()

    # Create a table to store the data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        ASIN TEXT,
        title TEXT,
        price REAL,
        amazon_price REAL,
        amazon_difference REAL,
        ebay_price REAL,
        ebay_difference REAL,
        link TEXT,
        shop_name TEXT,
        shopUrl TEXT,
        amazon_shop_Url TEXT,
        ebay_shop_Url TEXT,
        Category TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.close() 
