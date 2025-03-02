
from PriceHistory import PriceHistory
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, data: list[PriceHistory]):
        self.data = data

    def plot(self):
        # Plot the data
        # Extract dates and prices from the data
        dates = [entry.created for entry in self.data]
        prices = [entry.price for entry in self.data]

        # Create the plot
        # Format dates to German format
        dates = [entry.created.strftime('%d.%m.%Y') for entry in self.data] 
        plt.plot(dates, prices, marker='o')

        # Add labels and title
        plt.xlabel('Datum')
        plt.ylabel('Preis')
        plt.title(f'Preisentwicklung für {self.data[0].ProductName}')

        # Save the plot to a file
        plt.savefig(f"{self.data[0].fkpriceid}.png")
        plt.close()
        # Initialize the bot
