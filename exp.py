import requests
import pandas as pd
from datetime import datetime

# Headers used for NSE URL fetching
headerfornselib = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1",
    "Accept": "*/*",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
}

# Function to fetch URL with NSE headers
def nse_urlfetch(url):
    try:
        r_session = requests.session()
        # Fetching NSE homepage to initialize session (sometimes needed for NSE requests)
        r_session.get("http://nseindia.com", headers=headerfornselib)
        response = r_session.get(url, headers=headerfornselib)
        
        # Check if response is okay
        if response.status_code == 200:
            return response
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

# Function to get the trading holiday calendar from NSE
def trading_holiday_calendar():
    data_df = pd.DataFrame(columns=['Product', 'tradingDate', 'weekDay', 'description', 'Sr_no'])
    url = "https://www.nseindia.com/api/holiday-master?type=trading"
    
    try:
        # Fetching data from NSE
        response = nse_urlfetch(url)
        
        # Check if the response is valid
        if response is None or response.status_code != 200:
            raise Exception("Failed to retrieve data from NSE.")

        # Try to parse the response as JSON
        try:
            data_dict = response.json()
        except ValueError:
            raise Exception("Failed to parse JSON; response was not valid.")
        
        # Loop through the products in the data dictionary
        for prod in data_dict:
            h_df = pd.DataFrame(data_dict[prod])
            h_df['Product'] = prod
            data_df = pd.concat([data_df, h_df], ignore_index=True)
        
        # Define the mapping for product codes
        product_mapping = {
            'CBM': 'Corporate Bonds',
            'CD': 'Currency Derivatives',
            'CM': 'Equities',
            'CMOT': 'CMOT',
            'COM': 'Commodity Derivatives',
            'FO': 'Equity Derivatives',
            'IRD': 'Interest Rate Derivatives',
            'MF': 'Mutual Funds',
            'NDM': 'New Debt Segment',
            'NTRP': 'Negotiated Trade Reporting Platform',
            'SLBS': 'Securities Lending & Borrowing Schemes'
        }
        
        # Ensure 'Product' column is of type string and map the product descriptions
        data_df['Product'] = data_df['Product'].astype(str).map(product_mapping).fillna('Unknown')
        
        return data_df

    except Exception as e:
        print(e)
        raise Exception("Calendar data not found; try again later.")

# Function to check if today is a business day
def is_business_day(now):
    today = now.date()
    holidays_df = trading_holiday_calendar()  # Get the DataFrame from nselib

    # Convert 'tradingDate' to datetime.date format
    holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'], format='%d-%b-%Y').dt.date

    # Convert 'tradingDate' column to a list for easy comparison
    holidays = holidays_df['tradingDate'].tolist()

    # Check if today is a weekend or a holiday
    if today.weekday() >= 5 or today in holidays:
        return False
    return True

# Example usage:
now = datetime.now()
if is_business_day(now):
    print("Today is a business day.")
else:
    print("Today is not a business day.")
