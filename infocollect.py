import requests
from bs4 import BeautifulSoup

# Function to scrape stock data from Yahoo Finance
def scrape_stock_data():
    # List of stocks (add your own list of tickers here)
    stocks = ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'MSFT']
    stock_data = []

    for stock in stocks:
        url = f'https://finance.yahoo.com/quote/{stock}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get stock price
        try:
            price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
        except AttributeError:
            price = "N/A"

        stock_data.append({
            'ticker': stock,
            'price': price
        })

    return stock_data

# Save data to a file (or could save to JSON, or even upload to a database)
def save_stock_data():
    stock_data = scrape_stock_data()
    with open('stock_data.json', 'w') as f:
        f.write(str(stock_data))

if __name__ == "__main__":
    save_stock_data()