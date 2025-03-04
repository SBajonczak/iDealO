from amazon_paapi import AmazonApi


class Amazon:
    def __init__(self, accesskey: str, secretkey: str):
        self.accesskey= accesskey
        self.secretkey= secretkey
        self.partnerTag="saschabajoncz-21"
        self.REGION = "us-east-1"  # Change for your region
        self.COUNTRY = "DE"  # Change for your country
        pass
    
    def fetchBSR(self, asin:str)->str:
        try:
            amazon = AmazonApi(self.accesskey, self.secretkey, self.partnerTag, self.COUNTRY, throttling=2)
            item = amazon.get_items(asin)
            if len(item[0].browse_node_info.browse_nodes) > 0:
                print(f"Found BSR for {asin} {item[0].browse_node_info.browse_nodes[0].display_name}")
                return item[0].browse_node_info.browse_nodes[0].sales_rank
        except Exception as e:
            print(f"An error occurred while fetching BSR for {asin}: {e}")
            return None
