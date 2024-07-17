import nselib
import pandas as pd
from SmartApi import SmartConnect
import pyotp
from logzero import logger
import logincred
import http.client
import certifi
import json
import datetime as dt
import requests

# Function to check if today is a business day
def is_business_day(now):
    today = now.date()
    holidays_df = nselib.trading_holiday_calendar()  # Assuming this returns a DataFrame
    holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'], format='%d-%b-%Y').dt.date
    holidays = holidays_df['tradingDate'].values  # Convert to array of datetime.date objects

    if today.weekday() >= 5 or today in holidays:
        return False
    return True

# Function to login
def my_login(api_key, username, pwd):
    smartApi = SmartConnect(api_key)
    token = "TCLINC5Z7VAZCVKJ4Y2FYRIVPE"  # Ensure this is correct and valid

    try:
        totp = pyotp.TOTP(token).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    data = smartApi.generateSession(username, pwd, totp)

    if not data['status']:
        logger.error(data)
        return data, None, None
    else:
        # login api call
        # logger.info(f"Your Credentials: {data}")
        authToken = data['data']['jwtToken']
        msg = data['message']

        # Update the Authorization header with the received JWT token
        headers = {
            'Authorization': f'{authToken}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': '192.168.0.105',
            'X-ClientPublicIP': '192.168.0.105',
            'X-MACAddress': '50-C2-E8-8F-5A-85',
            'X-PrivateKey': '2D95hkAA'
        }
    return headers, msg

# Function to fetch funds
def myfunds(headers):
    # Specify the path to the CA certificates file
    ca_file = certifi.where()

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    url = '/rest/secure/angelbroking/user/v1/getRMS'

    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()
    funds_str = data.decode('utf-8')  # Decode bytes to string
    funds_dict = json.loads(funds_str)  # Parse JSON string to dictionary
    return funds_dict

# Function to access historical data  
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
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"

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
        print(data)

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
            print("No data returned from API")
            return pd.DataFrame()  # Return an empty DataFrame if no data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Angel Broking data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


def main():
    # Check if yesterday was a business day and then fetch funds
    now = dt.datetime.now() - dt.timedelta(days=1)
    
    if is_business_day(now):
        # Execute the login function and retrieve headers
        headers, msg = my_login(logincred.api_key, logincred.username, logincred.pwd)

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
        
        # One month time frame for any stock
        start_date = (dt.datetime.now().replace(hour=9, minute=15) - dt.timedelta(days=30)).strftime('%Y-%m-%d %H:%M')
        end_date = dt.datetime.now().replace(hour=15, minute=30).strftime('%Y-%m-%d %H:%M')

        for symbol, token in companiesdict.items():
            historical_data = myhistory(headers, "NSE", token, "ONE_DAY", start_date, end_date)
            # Process historical_data as needed

        funds = myfunds(headers)
        available_cash = funds.get('availablecash', 0)

        if msg == 'SUCCESS':
            if available_cash > 1000:
                print("Find Investment")
            elif available_cash < 1000:
                print("Sell Investment")

if __name__ == '__main__':
    main()





