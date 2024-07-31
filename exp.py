from datetime import datetime
import pandas as pd
import nselib

import numpy as np
import pandas as pd
import requests

# header = {
#     "Connection": "keep-alive",
#     "Cache-Control": "max-age=0",
#     "DNT": "1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/111.0.0.0 Safari/537.36",
#     "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
#     "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
#     }
# def nse_urlfetch(url):
#     r_session = requests.session()
#     nse_live = r_session.get("http://nseindia.com", headers=header)
#     return r_session.get(url, headers=header)
# def trading_holiday_calendar():
#     data_df = pd.DataFrame(columns=['Product', 'tradingDate', 'weekDay', 'description', 'Sr_no'])
#     url = "https://www.nseindia.com/api/holiday-master?type=trading"
#     try:
#         data_dict = nse_urlfetch(url).json()
#     except Exception as e:
#         raise ("Calendar data not found; try again later.")
    
#     for prod in data_dict:
#         h_df = pd.DataFrame(data_dict[prod])
#         h_df['Product'] = prod
#         data_df = pd.concat([data_df, h_df], ignore_index=True)
    
#     # Define the conditions and corresponding values
#     product_mapping = {
#         'CBM': 'Corporate Bonds',
#         'CD': 'Currency Derivatives',
#         'CM': 'Equities',
#         'CMOT': 'CMOT',
#         'COM': 'Commodity Derivatives',
#         'FO': 'Equity Derivatives',
#         'IRD': 'Interest Rate Derivatives',
#         'MF': 'Mutual Funds',
#         'NDM': 'New Debt Segment',
#         'NTRP': 'Negotiated Trade Reporting Platform',
#         'SLBS': 'Securities Lending & Borrowing Schemes'
#     }
    
#     # Ensure 'Product' column is of type string
#     data_df['Product'] = data_df['Product'].astype(str)
    
#     # Map the 'Product' column values to their descriptions
#     data_df['Product'] = data_df['Product'].map(product_mapping).fillna('Unknown')
    
#     return data_df
# def is_business_day(now):
#     today = now.date()
#     holidays_df = trading_holiday_calendar()  # Get the DataFrame from nselib

#     # Convert 'tradingDate' to datetime.date
#     holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'], format='%d-%b-%Y').dt.date
    
#     # Convert 'tradingDate' column to list for easy comparison
#     holidays = holidays_df['tradingDate'].tolist()

#     # Check if today is a weekend or a holiday
#     if today.weekday() >= 5 or today in holidays:
#         return False
#     return True

# # Test the function with a specific date
# now = datetime.now()
# print(f"Is today ({now}) a business day? {is_business_day(now)}")

import logging
import os
from dotenv import load_dotenv
import pyotp
from SmartAPI import SmartConnect
import datetime as dt

purchase_date = dt.datetime.strptime("2024-06-07", '%Y-%m-%d')
# Generate business date range
bdate_range = pd.bdate_range(start=purchase_date, periods=24)  # Get the next 24 business days
# print(bdate_range)
if len(bdate_range) >= 24:
    max_holding_date = bdate_range[-1]

today = dt.datetime.now().date
if today >= max_holding_date.date():
    print("sell")


# # Function to login
# def my_login():
#     """
#     Login to the API and return headers and message.

#     Parameters:
#     - api_key (str): API key for authentication.
#     - username (str): Username for login.
#     - pwd (str): Password for login.

#     Returns:
#     - tuple: Headers and message.
#     """
#     smartApi = SmartConnect(api_key)
#     token = tokenenv  # Ensure this is correct and valid

#     try:
#         totp = pyotp.TOTP(token).now()
#     except Exception as e:
#         logging.error("Invalid Token: The provided token is not valid.")
#         raise e

#     try:
#         data = smartApi.generateSession(username, pwd, totp)
#     except Exception as e:
#         logging.error(f"Error generating session: {e}")
#         return None, None

#     if not data['status']:
#         logging.error(data)
#         return data, None, None
#     else:
#         # login api call
#         # logger.info(f"Your Credentials: {data}")
#         authToken = data['data']['jwtToken']
#         msg = data['message']

#         # Update the Authorization header with the received JWT token
#         headers = {
#             'Authorization': f'{authToken}',
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#             'X-UserType': 'USER',
#             'X-SourceID': 'WEB',
#             'X-ClientLocalIP': '192.168.0.105',
#             'X-ClientPublicIP': '192.168.0.105',
#             'X-MACAddress': '50-C2-E8-8F-5A-85',
#             'X-PrivateKey': api_key  # Include api_key dynamically in the header
#         }
#     return headers, msg

# print(my_login())


