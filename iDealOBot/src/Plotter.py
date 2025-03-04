
from PriceHistory import PriceHistory
import matplotlib.pyplot as plt

from AzureDatabase import AzureDataBase
from collections import defaultdict
from statistics import mean


class Plotter:
    def __init__(self,Database:AzureDataBase):
        self.database=Database      

    def plot(self,priceId:int)->str:
        data: list[PriceHistory] = self.database.createPriceHistoryBypriceId(priceId)
        # Group prices by date
        grouped_data = defaultdict(list)
        for entry in data:
            date_str = entry.created.strftime('%d.%m')
            grouped_data[date_str].append(entry.price)

        # Calculate average price per day
        avg_prices_per_day = {date: mean(prices) for date, prices in grouped_data.items()}

        # Prepare data for plotting
        dates = list(avg_prices_per_day.keys())
        
        if len(dates)>1:
            return None
        
        prices = [f"{price:.2f} €" for price in avg_prices_per_day.values()]
        
        # Create the plot
        # Format dates to German format
        plt.plot(dates, prices, marker='o')
        plt.gcf().autofmt_xdate()  # Automatically format x-axis labels to fit
        plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin to make space for labels

        # Add labels and title
        plt.xlabel('Datum')
        plt.xticks(rotation=45)
        plt.ylabel('Preis')
        # plt.gca().invert_yaxis()
        plt.title(f'Preisentwicklung für {data[0].ProductName}')

        filename=f"{data[0].fkpriceid}.png"
        # Save the plot to a file
        plt.savefig(filename)
        plt.close()
        return filename
        # Initialize the bot
