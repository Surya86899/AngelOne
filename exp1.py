from datetime import datetime, timedelta
from typing import Dict
import pandas as pd
import requests
import logging
import math
import time
import certifi
import json
import http
import holdings
import csv

# Set up logging configuration at the beginning of your file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Set up logging
logger = logging.getLogger(__name__)

def myhistory(headers, exchange, symbol_token, interval, start_date, end_date):
    """
    Fetch historical candle data from Angel Broking API.

    Parameters:
    - exchange (str): Exchange name (e.g., "NSE").
    - symbol_token (str or int): Symbol token for the company.
    - interval (str): Interval of the candle data (e.g., "ONE_DAY").
    - start_date (str): Start date and time in format '%Y-%m-%d %H:%M'.
    - end_date (str): End date and time in format '%Y-%m-%d %H:%M'.

    Returns:
    - pd.DataFrame: DataFrame containing historical candle data.
    """
    # Angel Broking API endpoint
    url = "https://apiconnect.angelone.in/rest/secure/angelbroking/historical/v1/getCandleData"

    # Payload for the request
    payload = {
        "exchange": exchange,
        "symboltoken": symbol_token,
        "interval": interval,
        "fromdate": start_date,
        "todate": end_date
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json().get('data', [])
        # print(data)

        if data:
            # Convert API response data to formatted DataFrame
            formatted_data = pd.DataFrame(data, columns=[
                "Timestamp", "Open", "High", "Low", "Close", "Volume"
            ])
            formatted_data["Timestamp"] = pd.to_datetime(formatted_data["Timestamp"])
            formatted_data["Open"] = formatted_data["Open"].astype(float)
            formatted_data["High"] = formatted_data["High"].astype(float)
            formatted_data["Low"] = formatted_data["Low"].astype(float)
            formatted_data["Close"] = formatted_data["Close"].astype(float)
            formatted_data["Volume"] = formatted_data["Volume"].astype(float)

            return formatted_data
        else:
            logger.error("No data returned from API")
            return pd.DataFrame()  # Return an empty DataFrame if no data

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Angel Broking data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def calculate_dema(data: pd.DataFrame, period: int) -> pd.Series:
    """
    Calculate the Double Exponential Moving Average (DEMA) of the 'Close' prices.

    Parameters:
    - data (pd.DataFrame): DataFrame containing 'Close' prices.
    - period (int): The period for calculating the DEMA.

    Returns:
    - pd.Series: Series containing the DEMA values.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("data must be a pandas DataFrame")
    
    if 'Close' not in data.columns:
        raise ValueError("DataFrame must contain a 'Close' column")
    
    ema = data['Close'].ewm(span=period, adjust=False).mean()
    dema = 2 * ema - ema.ewm(span=period, adjust=False).mean()
    
    return dema

def to_invest(historical_data):
    """
    Determine if an investment should be made based on historical data.

    Parameters:
    - historical_data (pd.DataFrame): DataFrame containing historical market data with columns
      ['Volume', 'Close', 'High', 'Open'].

    Returns:
    - bool: True if investment criteria are met, False otherwise.
    """
    today = historical_data.iloc[-1]
    previous = historical_data.iloc[-2]

    # Calculate DEMA for periods 5, 8, and 13
    dema_5 = calculate_dema(historical_data, 5)
    dema_8 = calculate_dema(historical_data, 8)
    dema_13 = calculate_dema(historical_data, 13)

    # Check if the conditions are met
    if (today['Volume'] / previous['Volume'] >= 4 and
        (today['Close'] - previous['Close']) / previous['Close'] * 100 >= 4 and
        today['High'] > previous['High'] and
        dema_5.iloc[-1] > dema_8.iloc[-1] > dema_13.iloc[-1] and
        today['Close'] > today['Open']):
        return True
    return False

def calculate_brokerage(headers: Dict[str, str], transaction_type: str, quantity: int, price: float, 
                        symbol_name: str, token: str) -> float:
    """
    Calculate brokerage charges based on the provided parameters.

    Parameters:
    - headers (Dict[str, str]): HTTP headers including authentication tokens.
    - transaction_type (str): Type of transaction (e.g., "BUY" or "SELL").
    - quantity (int): Quantity of the stock to be traded.
    - price (float): Price per unit of the stock.
    - symbol_name (str): Name of the stock symbol.
    - token (str): Token for the stock symbol.

    Returns:
    - float: Estimated total brokerage charges. Returns float('inf') in case of errors.
    """
    url = "https://apiconnect.angelone.in/rest/secure/angelbroking/brokerage/v1/estimateCharges"
    data = {
        "orders": [
            {
                "product_type": "DELIVERY",
                "transaction_type": transaction_type,
                "quantity": quantity,
                "price": price,
                "exchange": "NSE",
                "symbol_name": symbol_name,
                "token": token
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses

        result = response.json()
        if result.get("status"):
            total_charges = result.get("data", {}).get("summary", {}).get("total_charges", 0)
            return float(total_charges) + 10 # Ensure this is a float for comparison +10 for safer side
        else:
            message = result.get('message', 'Unknown error')
            logger.error(f"API response error: {message}")
            return float('inf')  # Return a large number to indicate failure
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return float('inf')  # Return a large number to indicate failure

def myfunds(headers):
    try:
        # Specify the path to the CA certificates file
        ca_file = certifi.where()

        # Create an HTTPSConnection with the specified CA certificates file
        conn = http.client.HTTPSConnection(
            'apiconnect.angelone.in',
            context=http.client.ssl.create_default_context(cafile=ca_file)
        )

        url = '/rest/secure/angelbroking/user/v1/getRMS'

        conn.request("GET", url, headers=headers)

        res = conn.getresponse()
        data = res.read()
        funds_str = data.decode('utf-8')  # Decode bytes to string
        funds_dict = json.loads(funds_str)  # Parse JSON string to dictionary
        return 15000#funds_dict
    except Exception as e:
        logger.error(f"An error occured: {e}")
        return None

# Function to check if there are selling opportunities in the invested stocks and if there then sell it
def checkforsellingopportunities( headers, companiesdict, available_cash, start_date, end_date):
    """
    Check for selling opportunities based on historical data and existing investments.

    Parameters:
    - headers (dict): HTTP headers for API requests.
    - companiesdict (Dict[str, str]): Dictionary with company symbols and their tokens.
    - available_cash (float): Amount of cash available for investment.
    - start_date (str): Start date for historical data in format '%Y-%m-%d'.
    - end_date (str): End date for historical data in format '%Y-%m-%d'.
    """
    # Read the CSV file into a DataFrame
    csv_file_path = "investment.csv"
    try:
        df = pd.read_csv(csv_file_path, header=None)
    except FileNotFoundError:
        logging.error(f"File not found: {csv_file_path}")
        return
    except Exception as e:
        logging.error(f"Error reading {csv_file_path}: {e}")
        return

    # Ensure correct column names
    column_names = ['action','quantity','stock','stock_token','date','buy_price','sl']
    df.columns = column_names

    # Convert relevant columns to appropriate types
    df['buy_price'] = df['buy_price'].astype(float)
    df['sl'] = df['sl'].astype(float)
    df['quantity'] = df['quantity'].astype(int)

    # # Convert end_date_str to datetime
    # end_date = '2024-07-05 05:30'
    
    try:
        end_date = dt.datetime.strptime(end_date, '%Y-%m-%d %H:%M')
    except ValueError as e:
        logging.error(f"Error parsing end_date: {e}")
        return
    
    # Calculate start_date as 30 days before the end_date
    start_date = end_date - dt.timedelta(days=30)
    # Format dates as strings if needed for API or database queries
    end_date = end_date.strftime('%Y-%m-%d %H:%M')
    start_date = start_date.strftime('%Y-%m-%d %H:%M')
    logging.info(f"Start Date: {start_date}, End Date: {end_date}")


    # Define variables to store updated data
    updated_rows = []
    rows_to_delete = []
    email_msg = []

    # Check if DataFrame is empty
    if df.empty:
        logging.info("No data to process.")
        return

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        try:
            buy_date = row["date"]
        except ValueError:
            logging.warning(f"Invalid date format for row index {index}")
            continue
        if end_date[:10] == buy_date:
            logging.info(f"Skipping row {index} with buy date {buy_date} matching end_date")
            continue
        stock = row['stock']
        stock_token = row['stock_token']
        historical_data = myhistory(headers, "NSE", stock_token, "ONE_DAY", start_date, end_date)

        # Ensure there's data to check
        if historical_data.empty:
            continue
        
        today = historical_data.iloc[-1].copy()
        today['DEMA_5'] = calculate_dema(historical_data, 5).iloc[-1]
        today['DEMA_8'] = calculate_dema(historical_data, 8).iloc[-1]
        today['DEMA_13'] = calculate_dema(historical_data, 13).iloc[-1]
        
        sl = row['sl']
        targetnotach = row['action'] == "BUY"  # Example condition

        # Convert row["date"] to a datetime object
        purchase_date = dt.datetime.strptime(row["date"], '%Y-%m-%d')
        # Generate business date range
        bdate_range = pd.bdate_range(start=purchase_date, periods=24)  # Get the next 24 business days
        # print(bdate_range)
        if len(bdate_range) >= 24:
            max_holding_date = bdate_range[-1]

        # print(today)
        # print(sl)
        # print(targetnotach)
        
        logging.info(f"Max holding date for {stock}: {max_holding_date.date()}")

        if today["Timestamp"].date() >= max_holding_date.date(): #time.time >= 15:15 and
            # Sell on the max holding period
            sell_price = today['Close']
            updated_rows.append((index, 'Max Holding Period', sell_price))
            email_msg.append(['Max Holding Period',row['quantity'],row['stock'],row['stock_token'],end_date,sell_price,'-'])
            rows_to_delete.append(index)  # Mark for deletion

        elif today['Low'] <= sl:
            # Update with new stop-loss price
            sell_price = sl
            updated_rows.append((index, 'Stop Loss Hit', sell_price))
            email_msg.append(['Stop Loss Hit',row['quantity'],row['stock'],row['stock_token'],end_date,sell_price,sl])
            rows_to_delete.append(index)  # Optional, depending on your logic

        # Check if 4% target is achieved
        elif targetnotach and today['High'] >= (row['buy_price'] * 1.04):
            if today['DEMA_5'] > today['DEMA_8'] > today['DEMA_13']:
                # Update stop-loss to 2% down from the 4% target
                new_sl = row['buy_price'] * 1.02
                updated_rows.append((index, 'Updated SL', new_sl))
                email_msg.append(['Updated SL',row['quantity'],row['stock'],row['stock_token'],end_date,'-',new_sl])
            else:
                sell_price = row['buy_price'] * 1.04
                email_msg.append(['Sell 4% Hit',row['quantity'],row['stock'],row['stock_token'],end_date,sell_price])
                rows_to_delete.append(index)  # Mark for deletion

        elif not targetnotach and today['DEMA_5'] < today['DEMA_8']:
            # Perform the sell operation
            sell_price = today['Close']
            updated_rows.append((index, 'DEMA SELL', sell_price))
            email_msg.append(['DEMA Condition (Sell)',row['quantity'],row['stock'],row['stock_token'],end_date,sell_price,'-'])
            rows_to_delete.append(index)  # Mark for deletion

    # Update rows in DataFrame if updated_rows is properly structured
    if updated_rows:
        if isinstance(updated_rows, list) and all(isinstance(item, tuple) and len(item) == 3 for item in updated_rows):
            for index, new_action, new_sl in updated_rows:
                df.loc[index, 'action'] = new_action
                df.loc[index, 'sl'] = new_sl
        else:
            logging.info("updated_rows is either empty or not structured as expected.")

    # Send email if email_msg is correctly structured
    if email_msg:
        if isinstance(email_msg, list) and email_msg and isinstance(email_msg[0], list) and email_msg[0]:
            send_email(email_msg)
        else:
            logging.info("Email message is either empty or not structured as expected.")

    # Delete rows from DataFrame if rows_to_delete is properly structured
    if rows_to_delete:
        if isinstance(rows_to_delete, list) and all(isinstance(item, int) for item in rows_to_delete):
            df = df.drop(rows_to_delete)
        else:
            logging.info("rows_to_delete is either empty or not a list of indices.")

    # Save updated DataFrame to CSV
    if len(updated_rows) > 0 or len(rows_to_delete) > 0:
        df.to_csv(csv_file_path, index=False,header=False)  
        logging.info(f"Updated DataFrame saved to {csv_file_path}.")


companiesdict = {
            "ADANIENT": 25,
            "ADANIPORTS": 15083,
            "APOLLOHOSP": 157,
            "ASIANPAINT": 236,
            "AXISBANK": 5900,
            "BAJAJ-AUTO": 16669,
            "BAJFINANCE": 317,
            "BAJAJFINSV": 16675,
            "BPCL": 526,
            "BHARTIARTL": 10604,
            "BRITANNIA": 547,
            "CIPLA": 694,
            "COALINDIA": 20374,
            "DIVISLAB": 10940,
            "DRREDDY": 881,
            "EICHERMOT": 910,
            "GRASIM": 1232,
            "HCLTECH": 7229,
            "HDFCBANK": 1333,
            "HDFCLIFE": 467,
            "HEROMOTOCO": 1348,
            "HINDALCO": 1363,
            "HINDUNILVR": 1394,
            "ICICIBANK": 4963,
            "ITC": 1660,
            "INDUSINDBK": 5258,
            "INFY": 1594,
            "JSWSTEEL": 11723,
            "KOTAKBANK": 1922,
            "LTIM": 17818,
            "LT": 11483,
            "M&M": 2031,
            "MARUTI": 10999,
            "NTPC": 11630,
            "NESTLEIND": 17963,
            "ONGC": 2475,
            "POWERGRID": 14977,
            "RELIANCE": 2885,
            "SBILIFE": 21808,
            "SHRIRAMFIN": 4306,
            "SBIN": 3045,
            "SUNPHARMA": 3351,
            "TCS": 11536,
            "TATACONSUM": 3432,
            "TATAMOTORS": 3456,
            "TATASTEEL": 3499,
            "TECHM": 13538,
            "TITAN": 3506,
            "ULTRACEMCO": 11532,
            "WIPRO": 3787,
            
            "ABB": 13,
            "ADANIENSOL": 10217,
            "ADANIGREEN": 3563,
            "ADANIPOWER": 17388,
            "ATGL": 6066,
            "AMBUJACEM": 1270,
            "DMART": 19913,
            "BAJAJHLDNG": 305,
            "BANKBARODA": 4668,
            "BERGEPAINT": 404,
            "BEL": 383,
            "BOSCHLTD": 2181,
            "CANBK": 10794,
            "CHOLAFIN": 685,
            "COLPAL": 15141,
            "DLF": 14732,
            "DABUR": 772,
            "GAIL": 4717,
            "GODREJCP": 10099,
            "HAVELLS": 9819,
            "HAL": 2303,
            "ICICIGI": 21770,
            "ICICIPRULI": 18652,
            "IOC": 1624,
            "IRCTC": 13611,
            "IRFC": 2029,
            "NAUKRI": 13751,
            "INDIGO": 11195,
            "JINDALSTEL": 6733,
            "JIOFIN": 18143,
            "LICI": 9480,
            "MARICO": 4067,
            "PIDILITIND": 2664,
            "PFC": 14299,
            "PNB": 10666,
            "RECLTD": 15355,
            "SBICARD": 17971,
            "SRF": 3273,
            "MOTHERSON": 4204,
            "SHREECEM": 3103,
            "SIEMENS": 3150,
            "TVSMOTOR": 8479,
            "TATAMTRDVR": 16965,
            "TATAPOWER": 3426,
            "TORNTPHARM": 3518,
            "TRENT": 1964,
            "VBL": 18921,
            "VEDL": 3063,
            "ZOMATO": 5097,
            "ZYDUSLIFE": 7929,

            "ACC": 22,
            "AUBANK": 21238,
            "ABCAPITAL": 21614,
            "ALKEM": 11703,
            "ASHOKLEY": 212,
            "ASTRAL": 14418,
            "AUROPHARMA": 275,
            "BALKRISIND": 335,
            "BANDHANBNK": 2263,
            "BHARATFORG": 422,
            "BHEL": 438,
            "COFORGE": 11543,
            "CONCOR": 4749,
            "CUMMINSIND": 1901,
            "DALBHARAT": 8075,
            "DIXON": 21690,
            "ESCORTS": 958,
            "FEDERALBNK": 1023,
            "GMRINFRA": 13528,
            "GODREJPROP": 17875,
            "GUJGASLTD": 10599,
            "HDFCAMC": 4244,
            "HINDPETRO": 1406,
            "IDFCFIRSTB": 11184,
            "INDHOTEL": 1512,
            "INDUSTOWER": 29135,
            "JUBLFOOD": 18096,
            "LTF": 24948,
            "LTTS": 18564,
            "LUPIN": 10440,
            "MRF": 2277,
            "M&MFIN": 13285,
            "MFSL": 2142,
            "MAXHEALTH": 22377,
            "MPHASIS": 4503,
            "NMDC": 15332,
            "OBEROIRLTY": 20242,
            "OFSS": 10738,
            "PIIND": 24184,
            "PAGEIND": 14413,
            "PERSISTENT": 18365,
            "PETRONET": 11351,
            "POLYCAB": 9590,
            "SAIL": 2963,
            "SUZLON": 12018,
            "TATACOMM": 3721,
            "TIINDIA": 312,
            "UPL": 11287,
            "IDEA": 14366,
            "YESBANK": 11915,
        }

# holding = holdings.myholdings()
# print(holding)

