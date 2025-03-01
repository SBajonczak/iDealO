import pyodbc
import os
from Offer import Offer
import pyodbc, struct
from azure import identity

connection_string = os.getenv('AZURE_SQL_CONNECTION_STRING','DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sbadbprod.database.windows.net,1433;DATABASE=sba-dealz-db;UID=sbaadmin;PWD==S?p86`YCYjo*7TNc~[S') 


def get_connection():

    # credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    # token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    # token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    # SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    # conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    # return conn

    return pyodbc.connect(connection_string)

def getElementByTitle(title) -> Offer:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ASIN, title, price, 
                   amazon_price, amazon_difference, ebay_price, 
                   ebay_difference, link, shop_name,
                   amazon_shop_Url, ebay_shop_Url, shopUrl
            FROM prices 
            WHERE title = ?
        ''', (title,))
        row = cursor.fetchone()
        if row:
            return Offer(
                ASIN=row.ASIN,
                ProductName=row.title,
                price=row.price,
                amazonPrice=row.amazon_price,
                ebayPrice=row.ebay_price,
                idealoUrl=row.link,
                storeName=row.shop_name,
                amazonShopUrl=row.amazon_shop_Url,
                ebayShopUrl=row.ebay_shop_Url,
                shopUrl=row.shopUrl
            )
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def getElementByASIN(asin) -> Offer:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ASIN, title, price, 
                   amazon_price, amazon_difference, ebay_price, 
                   ebay_difference, link, shop_name,
                   amazon_shop_Url, ebay_shop_Url, shopUrl
            FROM prices 
            WHERE ASIN = ?
        ''', (asin,))
        row = cursor.fetchone()
        if row:
            return Offer(
                ASIN=row.ASIN,
                ProductName=row.title,
                price=row.price,
                amazonPrice=row.amazon_price,
                ebayPrice=row.ebay_price,
                idealoUrl=row.link,
                storeName=row.shop_name,
                amazonShopUrl=row.amazon_shop_Url,
                ebayShopUrl=row.ebay_shop_Url,
                shopUrl=row.shopUrl
            )
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def createTableIfNotExists():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[prices]') AND type in (N'U'))
    BEGIN
        CREATE TABLE [dbo].[prices] (
            [Id] INT IDENTITY(1,1) PRIMARY KEY,
            [ASIN] NVARCHAR(50),
            [title] NVARCHAR(500),
            [price] DECIMAL(10,2),
            [amazon_price] DECIMAL(10,2),
            [amazon_difference] DECIMAL(10,2),
            [ebay_price] DECIMAL(10,2),
            [ebay_difference] DECIMAL(10,2),
            [link] NVARCHAR(1000),
            [shop_name] NVARCHAR(255),
            [shopUrl] NVARCHAR(1000),
            [amazon_shop_Url] NVARCHAR(1000),
            [ebay_shop_Url] NVARCHAR(1000),
            [Category] NVARCHAR(100),
            [created] DATETIME2 DEFAULT GETDATE(),
            [updated] DATETIME2 DEFAULT GETDATE()
        )

        CREATE INDEX IX_prices_ASIN ON [dbo].[prices] ([ASIN])
        CREATE INDEX IX_prices_title ON [dbo].[prices] ([title])
    END
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

    
def UpsertDb(offer:Offer):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            MERGE INTO prices AS target
            USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) 
                AS source (ASIN, title, price, amazon_price, amazon_difference, 
                          ebay_price, ebay_difference, link, shop_name, 
                          shopUrl, amazon_shop_Url, ebay_shop_Url)
            ON target.ASIN = source.ASIN
            WHEN MATCHED THEN
                UPDATE SET 
                    title = source.title,
                    price = source.price,
                    amazon_price = source.amazon_price,
                    amazon_difference = source.amazon_difference,
                    ebay_price = source.ebay_price,
                    ebay_difference = source.ebay_difference,
                    link = source.link,
                    shop_name = source.shop_name,
                    shopUrl = source.shopUrl,
                    amazon_shop_Url = source.amazon_shop_Url,
                    ebay_shop_Url = source.ebay_shop_Url,
                    updated = GETDATE()
            WHEN NOT MATCHED THEN
                INSERT (ASIN, title, price, amazon_price, amazon_difference,
                        ebay_price, ebay_difference, link, shop_name,
                        shopUrl, amazon_shop_Url, ebay_shop_Url)
                VALUES (source.ASIN, source.title, source.price, 
                        source.amazon_price, source.amazon_difference,
                        source.ebay_price, source.ebay_difference, 
                        source.link, source.shop_name, source.shopUrl,
                        source.amazon_shop_Url, source.ebay_shop_Url);
        ''', (
            offer.getAsinFromAmazon(), offer.ProductName, offer.price,
            offer.amazonPrice, offer.amazonDifference,
            offer.ebayPrice, offer.ebayDifference,
            offer.IdealoUrl, offer.StoreName,
            offer.shopUrl, offer.amazonShopUrl, offer.ebayShopUrl
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error upserting data: {str(e)}")
        return False