from datetime import datetime, timedelta
from typing import Dict
import pandas as pd
import pyotp
import requests
import logging
import math
import time
import certifi
import json
import http
from SmartApi.smartConnect import SmartConnect
import holdings
import os

# # from headers import headers

# # # Set up logging configuration at the beginning of your file
# # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# # # Set up logging
# # logging = logging.getLogger(__name__)

# # def myhistory(headers, exchange, symbol_token, interval, start_date, end_date):
# #     """
# #     Fetch historical candle data from Angel Broking API.

# #     Parameters:
# #     - exchange (str): Exchange name (e.g., "NSE").
# #     - symbol_token (str or int): Symbol token for the company.
# #     - interval (str): Interval of the candle data (e.g., "ONE_DAY").
# #     - start_date (str): Start date and time in format '%Y-%m-%d %H:%M'.
# #     - end_date (str): End date and time in format '%Y-%m-%d %H:%M'.

# #     Returns:
# #     - pd.DataFrame: DataFrame containing historical candle data.
# #     """
# #     # Angel Broking API endpoint
# #     url = "https://apiconnect.angelone.in/rest/secure/angelbroking/historical/v1/getCandleData"

# #     # Payload for the request
# #     payload = {
# #         "exchange": exchange,
# #         "symboltoken": symbol_token,
# #         "interval": interval,
# #         "fromdate": start_date,
# #         "todate": end_date
# #     }

# #     try:
# #         response = requests.post(url, json=payload, headers=headers)
# #         response.raise_for_status()  # Raise HTTPError for bad responses

# #         data = response.json().get('data', [])
# #         # print(data)

# #         if data:
# #             # Convert API response data to formatted DataFrame
# #             formatted_data = pd.DataFrame(data, columns=[
# #                 "Timestamp", "Open", "High", "Low", "Close", "Volume"
# #             ])
# #             formatted_data["Timestamp"] = pd.to_datetime(formatted_data["Timestamp"])
# #             formatted_data["Open"] = formatted_data["Open"].astype(float)
# #             formatted_data["High"] = formatted_data["High"].astype(float)
# #             formatted_data["Low"] = formatted_data["Low"].astype(float)
# #             formatted_data["Close"] = formatted_data["Close"].astype(float)
# #             formatted_data["Volume"] = formatted_data["Volume"].astype(float)

# #             return formatted_data
# #         else:
# #             logging.error("No data returned from API")
# #             return pd.DataFrame()  # Return an empty DataFrame if no data

# #     except requests.exceptions.RequestException as e:
# #         logging.error(f"Error fetching Angel Broking data: {e}")
# #         return pd.DataFrame()  # Return an empty DataFrame on error

# # def calculate_dema(data: pd.DataFrame, period: int) -> pd.Series:
# #     """
# #     Calculate the Double Exponential Moving Average (DEMA) of the 'Close' prices.

# #     Parameters:
# #     - data (pd.DataFrame): DataFrame containing 'Close' prices.
# #     - period (int): The period for calculating the DEMA.

# #     Returns:
# #     - pd.Series: Series containing the DEMA values.
# #     """
# #     if not isinstance(data, pd.DataFrame):
# #         raise ValueError("data must be a pandas DataFrame")
    
# #     if 'Close' not in data.columns:
# #         raise ValueError("DataFrame must contain a 'Close' column")
    
# #     ema = data['Close'].ewm(span=period, adjust=False).mean()
# #     dema = 2 * ema - ema.ewm(span=period, adjust=False).mean()
    
# #     return dema

# # def to_invest(historical_data):
# #     """
# #     Determine if an investment should be made based on historical data.

# #     Parameters:
# #     - historical_data (pd.DataFrame): DataFrame containing historical market data with columns
# #       ['Volume', 'Close', 'High', 'Open'].

# #     Returns:
# #     - bool: True if investment criteria are met, False otherwise.
# #     """
# #     today = historical_data.iloc[-1]
# #     previous = historical_data.iloc[-2]

# #     # Calculate DEMA for periods 5, 8, and 13
# #     dema_5 = calculate_dema(historical_data, 5)
# #     dema_8 = calculate_dema(historical_data, 8)
# #     dema_13 = calculate_dema(historical_data, 13)

# #     # Check if the conditions are met
# #     if (today['Volume'] / previous['Volume'] >= 4 and
# #         (today['Close'] - previous['Close']) / previous['Close'] * 100 >= 4 and
# #         today['High'] > previous['High'] and
# #         dema_5.iloc[-1] > dema_8.iloc[-1] > dema_13.iloc[-1] and
# #         today['Close'] > today['Open']):
# #         return True
# #     return False

# def my_login(api_key,pwd,username,tokenenv):
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

#     try:
#         totp = pyotp.TOTP(tokenenv).now()
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
#         return None, None
#     else:
#         # login api call
#         # logging.info(f"Your Credentials: {data}")
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

# # def calculate_brokerage(headers: Dict[str, str], transaction_type: str, quantity: int, price: float, 
# #                         symbol_name: str, token: str) -> float:
# #     """
# #     Calculate brokerage charges based on the provided parameters.

# #     Parameters:
# #     - headers (Dict[str, str]): HTTP headers including authentication tokens.
# #     - transaction_type (str): Type of transaction (e.g., "BUY" or "SELL").
# #     - quantity (int): Quantity of the stock to be traded.
# #     - price (float): Price per unit of the stock.
# #     - symbol_name (str): Name of the stock symbol.
# #     - token (str): Token for the stock symbol.

# #     Returns:
# #     - float: Estimated total brokerage charges. Returns float('inf') in case of errors.
# #     """
# #     url = "https://apiconnect.angelone.in/rest/secure/angelbroking/brokerage/v1/estimateCharges"
# #     data = {
# #         "orders": [
# #             {
# #                 "product_type": "DELIVERY",
# #                 "transaction_type": transaction_type,
# #                 "quantity": quantity,
# #                 "price": price,
# #                 "exchange": "NSE",
# #                 "symbol_name": symbol_name,
# #                 "token": token
# #             }
# #         ]
# #     }
# #     try:
# #         response = requests.post(url, headers=headers, data=json.dumps(data))
# #         response.raise_for_status()  # Raise HTTPError for bad responses

# #         result = response.json()
# #         if result.get("status"):
# #             total_charges = result.get("data", {}).get("summary", {}).get("total_charges", 0)
# #             return float(total_charges)  # Ensure this is a float for comparison
# #         else:
# #             message = result.get('message', 'Unknown error')
# #             logging.error(f"API response error: {message}")
# #             return float('inf')  # Return a large number to indicate failure
# #     except requests.RequestException as e:
# #         logging.error(f"Request failed: {e}")
# #         return float('inf')  # Return a large number to indicate failure
    
# # def myfunds(headers):
# #     try:
# #         # Specify the path to the CA certificates file
# #         ca_file = certifi.where()

# #         # Create an HTTPSConnection with the specified CA certificates file
# #         conn = http.client.HTTPSConnection(
# #             'apiconnect.angelone.in',
# #             context=http.client.ssl.create_default_context(cafile=ca_file)
# #         )

# #         url = '/rest/secure/angelbroking/user/v1/getRMS'

# #         conn.request("GET", url, headers=headers)

# #         res = conn.getresponse()
# #         data = res.read()
# #         funds_str = data.decode('utf-8')  # Decode bytes to string
# #         funds_dict = json.loads(funds_str)  # Parse JSON string to dictionary
# #         return 15000#funds_dict
# #     except Exception as e:
# #         logging.error(f"An error occured: {e}")
# #         return None

# # def checkforinvestmentopportunities(headers, companiesdict: Dict[str, str], available_cash: float, start_date: str, end_date: str):
# #     """
# #     Check for investment opportunities based on historical data and available cash.

# #     Parameters:
# #     - headers (dict): HTTP headers for API requests.
# #     - companiesdict (Dict[str, str]): Dictionary with company symbols and their tokens.
# #     - available_cash (float): Amount of cash available for investment.
# #     - start_date (str): Start date for historical data in format '%Y-%m-%d'.
# #     - end_date (str): End date for historical data in format '%Y-%m-%d'.
# #     """

# #     # investments = []

# #     for i, (symbol, token) in enumerate(companiesdict.items(), start=1):

# #         # checks if there is enough cash to invest
# #         if available_cash < 9000:
# #             logging.info("Available cash is below the threshold. Exiting.")
# #             break

# #         try:
# #             # Fetch historical data for the company
# #             historical_data = myhistory(headers, "NSE", token, "ONE_DAY", start_date, end_date)
# #             if historical_data.empty:
# #                 logging.warning(f"No data available for {symbol}")
# #                 continue

# #             # Check if it's a good investment opportunity
# #             if to_invest(historical_data):
# #                 today = historical_data.iloc[-1]
# #                 max_shares = math.floor(available_cash / today['Close'])
# #                 logging.info(f"Max shares for {symbol}: {max_shares}")

# #                 available_cash -= today["Close"] * max_shares
# #                 transaction_type = "BUY"
                
# #                 # Check brokerage and adjust shares if necessary
# #                 calc_brokerage = calculate_brokerage(headers, transaction_type, max_shares, today['Close'], symbol, token)
# #                 if calc_brokerage > available_cash:
# #                     max_shares -= 1
# #                     logging.info(f"Adjusted max shares for {symbol}: {max_shares}")
                
# #                 if max_shares > 0:
# #                     sl = today['Low'] - (today['Low'] * 0.03)
# #                     investment_details = ["BUY", max_shares, symbol, token, today['Timestamp'].strftime('%Y-%m-%d'), today["Close"], sl]
# #                     logging.info(f"Investment details for {symbol}: {investment_details}")
# #                     # investments.append(investment_details)

# #                     # Update available cash after each investment
# #                     available_cash = myfunds(headers)

# #         except Exception as e:
# #             logging.error(f"Error processing {symbol}: {e}")

# #         # Add delay every 3 requests to avoid rate-limiting
# #         if i % 3 == 0:
# #             time.sleep(1)

# #     # # If there are new investments, send email and save to CSV
# #     # if investments:
# #     #     send_email(investments)
# #     #     save_in_csv(investments)


# # companiesdict = {
# #             "ADANIENT": 25,
# #             "ADANIPORTS": 15083,
# #             "APOLLOHOSP": 157,
# #             "ASIANPAINT": 236,
# #             "AXISBANK": 5900,
# #             "BAJAJ-AUTO": 16669,
# #             "BAJFINANCE": 317,
# #             "BAJAJFINSV": 16675,
# #             "BPCL": 526,
# #             "BHARTIARTL": 10604,
# #             "BRITANNIA": 547,
# #             "CIPLA": 694,
# #             "COALINDIA": 20374,
# #             "DIVISLAB": 10940,
# #             "DRREDDY": 881,
# #             "EICHERMOT": 910,
# #             "GRASIM": 1232,
# #             "HCLTECH": 7229,
# #             "HDFCBANK": 1333,
# #             "HDFCLIFE": 467,
# #             "HEROMOTOCO": 1348,
# #             "HINDALCO": 1363,
# #             "HINDUNILVR": 1394,
# #             "ICICIBANK": 4963,
# #             "ITC": 1660,
# #             "INDUSINDBK": 5258,
# #             "INFY": 1594,
# #             "JSWSTEEL": 11723,
# #             "KOTAKBANK": 1922,
# #             "LTIM": 17818,
# #             "LT": 11483,
# #             "M&M": 2031,
# #             "MARUTI": 10999,
# #             "NTPC": 11630,
# #             "NESTLEIND": 17963,
# #             "ONGC": 2475,
# #             "POWERGRID": 14977,
# #             "RELIANCE": 2885,
# #             "SBILIFE": 21808,
# #             "SHRIRAMFIN": 4306,
# #             "SBIN": 3045,
# #             "SUNPHARMA": 3351,
# #             "TCS": 11536,
# #             "TATACONSUM": 3432,
# #             "TATAMOTORS": 3456,
# #             "TATASTEEL": 3499,
# #             "TECHM": 13538,
# #             "TITAN": 3506,
# #             "ULTRACEMCO": 11532,
# #             "WIPRO": 3787,
            
# #             "ABB": 13,
# #             "ADANIENSOL": 10217,
# #             "ADANIGREEN": 3563,
# #             "ADANIPOWER": 17388,
# #             "ATGL": 6066,
# #             "AMBUJACEM": 1270,
# #             "DMART": 19913,
# #             "BAJAJHLDNG": 305,
# #             "BANKBARODA": 4668,
# #             "BERGEPAINT": 404,
# #             "BEL": 383,
# #             "BOSCHLTD": 2181,
# #             "CANBK": 10794,
# #             "CHOLAFIN": 685,
# #             "COLPAL": 15141,
# #             "DLF": 14732,
# #             "DABUR": 772,
# #             "GAIL": 4717,
# #             "GODREJCP": 10099,
# #             "HAVELLS": 9819,
# #             "HAL": 2303,
# #             "ICICIGI": 21770,
# #             "ICICIPRULI": 18652,
# #             "IOC": 1624,
# #             "IRCTC": 13611,
# #             "IRFC": 2029,
# #             "NAUKRI": 13751,
# #             "INDIGO": 11195,
# #             "JINDALSTEL": 6733,
# #             "JIOFIN": 18143,
# #             "LICI": 9480,
# #             "MARICO": 4067,
# #             "PIDILITIND": 2664,
# #             "PFC": 14299,
# #             "PNB": 10666,
# #             "RECLTD": 15355,
# #             "SBICARD": 17971,
# #             "SRF": 3273,
# #             "MOTHERSON": 4204,
# #             "SHREECEM": 3103,
# #             "SIEMENS": 3150,
# #             "TVSMOTOR": 8479,
# #             "TATAMTRDVR": 16965,
# #             "TATAPOWER": 3426,
# #             "TORNTPHARM": 3518,
# #             "TRENT": 1964,
# #             "VBL": 18921,
# #             "VEDL": 3063,
# #             "ZOMATO": 5097,
# #             "ZYDUSLIFE": 7929,

# #             "ACC": 22,
# #             "AUBANK": 21238,
# #             "ABCAPITAL": 21614,
# #             "ALKEM": 11703,
# #             "ASHOKLEY": 212,
# #             "ASTRAL": 14418,
# #             "AUROPHARMA": 275,
# #             "BALKRISIND": 335,
# #             "BANDHANBNK": 2263,
# #             "BHARATFORG": 422,
# #             "BHEL": 438,
# #             "COFORGE": 11543,
# #             "CONCOR": 4749,
# #             "CUMMINSIND": 1901,
# #             "DALBHARAT": 8075,
# #             "DIXON": 21690,
# #             "ESCORTS": 958,
# #             "FEDERALBNK": 1023,
# #             "GMRINFRA": 13528,
# #             "GODREJPROP": 17875,
# #             "GUJGASLTD": 10599,
# #             "HDFCAMC": 4244,
# #             "HINDPETRO": 1406,
# #             "IDFCFIRSTB": 11184,
# #             "INDHOTEL": 1512,
# #             "INDUSTOWER": 29135,
# #             "JUBLFOOD": 18096,
# #             "LTF": 24948,
# #             "LTTS": 18564,
# #             "LUPIN": 10440,
# #             "MRF": 2277,
# #             "M&MFIN": 13285,
# #             "MFSL": 2142,
# #             "MAXHEALTH": 22377,
# #             "MPHASIS": 4503,
# #             "NMDC": 15332,
# #             "OBEROIRLTY": 20242,
# #             "OFSS": 10738,
# #             "PIIND": 24184,
# #             "PAGEIND": 14413,
# #             "PERSISTENT": 18365,
# #             "PETRONET": 11351,
# #             "POLYCAB": 9590,
# #             "SAIL": 2963,
# #             "SUZLON": 12018,
# #             "TATACOMM": 3721,
# #             "TIINDIA": 312,
# #             "UPL": 11287,
# #             "IDEA": 14366,
# #             "YESBANK": 11915,
# #         }

# # holding = holdings.myholdings()
# # print(holding)

# # Add this to print environment variables for debugging
# api_key = os.getenv('API_KEY')
# username = os.getenv('USERNAME')
# pwd = os.getenv('MPIN')
# tokenenv = os.getenv('TOKEN')
# email_pass = os.getenv('EMAIL_PASS')

# headers,msg = my_login(api_key,pwd,username,tokenenv)
# # print(headers)
# # print(calculate_brokerage(headers, "BUY", 10, 500,"SBIN", "3045"))


# # def create_normal_order(headers, variety: str, trading_symbol: str, symbol_token: str, transaction_type: str, exchange: str, order_type: str, product_type: str, duration: str, price: str, square_off: str, stop_loss: str, qty: str):
# #     """
# #     Create Normal Order
# #         Parameters:
# #         - headers (Dict[str, str]): HTTP headers including authentication tokens.
# #         - variety (str): Type of Order (e.g., "NORMAL","STOPLOSS","AMO","ROBO").
# #         - trading_symbol (str): Symbol of the stock. (e.g., "ABB-EQ", "SBIN-EQ").
# #         - symbol_token (str): Token for the stock symbol.
# #         - transaction_type (str): Type of transaction (e.g., "BUY" or "SELL").
# #         - exchange (str): Exchange name (e.g., "NSE").
# #         - order_type (str): Another type of order (e.g., "MARKET","LIMIT","STOPLOSS_LIMIT","STOPLOSS_MARKET").
# #         - product_type (str): Another type of order (e.g., "DELIVERY","CARRYFORWARD","MARGIN","INTRADAY",BO).
# #         - price (str): Price per unit of the stock. (Kept 0 here or it will become Limit order).
# #         - square_off (str): Only For ROBO (Bracket Order).
# #         - stop_loss (str): Only For ROBO (Bracket Order).
# #         - qty (str): Quantity of the stock to be traded.

# #         Returns:
# #         - str: unique_order_id if successful.
# #         - None: if there is an error.
# #     """
# #     import http.client
# #     import json
# #     import certifi

# #     try:
# #         # Specify the path to the CA certificates file
# #         ca_file = certifi.where()
# #         print(f"CA Certificates Path: {ca_file}")

# #         # Create an HTTPSConnection with the specified CA certificates file
# #         conn = http.client.HTTPSConnection(
# #             'apiconnect.angelbroking.com',
# #             context=http.client.ssl._create_default_https_context(cafile=ca_file)
# #         )

# #         # Construct the payload
# #         payload = {
# #             "variety": variety,
# #             "tradingsymbol": trading_symbol,
# #             "symboltoken": symbol_token,
# #             "transactiontype": transaction_type,
# #             "exchange": exchange,
# #             "ordertype": order_type,
# #             "producttype": product_type,
# #             "duration": duration,
# #             "price": price,
# #             "squareoff": square_off,
# #             "stoploss": stop_loss,
# #             "quantity": qty
# #         }
# #         payload_str = json.dumps(payload)

# #         # Send the POST request
# #         conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)

# #         # Get and decode the response
# #         res = conn.getresponse()
# #         data = res.read()
# #         response_text = data.decode("utf-8")
# #         print(f"Response: {response_text}")

# #         # Parse the response
# #         response_json = json.loads(data)
# #         if 'data' in response_json and 'uniqueorderid' in response_json['data']:
# #             unique_order_id = response_json['data']['uniqueorderid']
# #             return unique_order_id
# #         else:
# #             print("Error: Unexpected response format.")
# #             print(f"Response JSON: {response_json}")
# #             return None

# #     except http.client.HTTPException as http_error:
# #         print(f"HTTP Exception occurred: {http_error}")
# #         return None

# #     except json.JSONDecodeError as json_error:
# #         print(f"JSON Decode Error: {json_error}")
# #         return None

# #     except KeyError as key_error:
# #         print(f"KeyError: {key_error}. Check if 'data' and 'uniqueorderid' exist in the response.")
# #         return None

# #     except Exception as general_error:
# #         print(f"An unexpected error occurred: {general_error}")
# #         return None

# # trading_symbol = "ABB-EQ"
# # symbol_token = "13"

# # price = square_off = stop_loss = "0" 

# # unique_order_id = create_normal_order(headers,"NORMAL",trading_symbol,symbol_token,"BUY","NSE","MARKET","DELIVERY","DAY",price,square_off,stop_loss,"1")

# # print(unique_order_id)
# # print(type(unique_order_id))

# def myholdings(headers):
#     """
#     Fetch and return holdings from the Angel Broking API.

#     Parameters:
#     - headers (dict): HTTP headers for the API request.

#     Returns:
#     - list: A list of holdings if the request is successful.
#     - None: If an error occurs during the request or data processing.
#     """
#     # API endpoint for holdings
#     url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/portfolio/v1/getHolding"

#     try:
#         # Make the GET request with SSL verification using certifi
#         response = requests.get(url, headers=headers, verify=certifi.where())

#         # Check if the response status is OK (HTTP 200)
#         if response.status_code == 200:
#             data = response.json()

#             # Verify if the API returned a success status
#             if data.get('status'):
#                 holdings = data.get('data', [])

#                 # Log and return holdings data
#                 logging.info(f"Successfully fetched {len(holdings)} holdings.")
#                 return holdings
#             else:
#                 logging.error(f"API error: {data.get('message', 'Unknown error')}")
#                 return None
#         else:
#             logging.error(f"HTTP error: Status code {response.status_code}")
#             return None

#     except requests.RequestException as e:
#         logging.error(f"Request failed: {e}")
#         return None

# hold_res = myholdings(headers)
# print(hold_res)
# # for holds in hold_res:
# #     for i in holds:
# #         print(i+" ",holds[i])

# print("*****************************************************************************************")
# print("*****************************************************************************************")

# def get_gtt_allrule_details(headers):
#     """
#         Fetch details of all GTT rules based on specified statuses.

#         Parameters:
#         - headers (dict): HTTP headers for the API request.

#         Returns:
#         - dict: Parsed JSON response containing GTT rule details if the request is successful.
#         - None: If an error occurs during the request or response parsing.
#     """
#     try:
#         # Specify the path to the CA certificates file
#         ca_file = certifi.where()

#         # Create an HTTPSConnection with the specified CA certificates file
#         conn = http.client.HTTPSConnection(
#             'apiconnect.angelbroking.com',
#             context=http.client.ssl._create_default_https_context(cafile=ca_file)
#         )

#         # Define the payload
#         payload = json.dumps({
#             "status": ["NEW", "ACTIVE", "SENTTOEXCHANGE"], # "CANCELLED" could also be added to view cancelled gtt orders , "FORALL"
#             "page": 1,
#             "count": 10
#         })

#         # Make the POST request
#         conn.request("POST", "/rest/secure/angelbroking/gtt/v1/ruleList", payload, headers)

#         # Get the response
#         res = conn.getresponse()
#         data = res.read().decode("utf-8")

#         # Parse the JSON response
#         response_data = json.loads(data)

#         # Log the response and return the parsed data
#         logging.info(f"Fetched GTT rule details: {json.dumps(response_data, indent=4)}")
#         return response_data["data"]

#     except http.client.HTTPException as http_error:
#         logging.error(f"HTTP Exception occurred: {http_error}")
#         return None
#     except json.JSONDecodeError as json_error:
#         logging.error(f"JSON Decode Error: {json_error}")
#         return None
#     except Exception as general_error:
#         logging.error(f"An unexpected error occurred: {general_error}")
#         return None

# gtt_res = get_gtt_allrule_details(headers)
# print(gtt_res)
# # for holds in gtt_res:
#     # for i in holds:
#     #     print(i+" ",holds[i])
#     # print(holds)

def is_business_day(now):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.nseindia.com/holiday-master',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }
    endpoint = "https://www.nseindia.com/api/holiday-master?type=trading"
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        holidays_json = response.json().get('FO', [])
        holidays_df = pd.DataFrame(holidays_json)
        holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'])
        return not(pd.Timestamp(now) in holidays_df['tradingDate'].values)
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching holiday data: {e}")
        return True
    
now = datetime.now()

print(is_business_day(now))

