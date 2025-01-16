import requests
from bs4 import BeautifulSoup
import json

# Function to scrape stock data from Yahoo Finance
def scrape_stock_data():
    # List of stock tickers you want to track
    stocks = ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'MSFT', 'NFLX', 'META', 'NVDA', 'SPY', 'BTC']
    stock_data = []

    for stock in stocks:
        # URL of the Yahoo Finance page for the stock
        url = f'https://finance.yahoo.com/quote/{stock}'
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve data for {stock}")
            continue

        # Parse the HTML page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt to extract the stock price from the page
        try:
            # Find the element containing the stock price
            price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
        except AttributeError:
            price = "N/A"  # If the price is not found, set as N/A

        # Append the stock ticker and price to the list
        stock_data.append({
            'ticker': stock,
            'price': price
        })

    return stock_data

# Function to save the stock data to a JSON file
def save_stock_data():
    # Scrape stock data
    stock_data = scrape_stock_data()

    # Write the stock data to a JSON file
    with open('stock_data.json', 'w') as json_file:
        # Use json.dump to write the list to a file with proper formatting
        json.dump(stock_data, json_file, indent=4)

# Run the script to scrape and save data
if __name__ == "__main__":
    save_stock_data()
    print("Stock data saved to stock_data.json")
