# This is the file that will deal with real money

# All the required imports
import math
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
import smtplib
from email.message import EmailMessage
import time
import csv
import logging
from typing import Dict, Any, List, Union


from headers import headers


# from dotenv import load_dotenv
import os

# Set up logging configuration at the beginning of your file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Set up logging
logger = logging.getLogger(__name__)

# Function to check if it's a business day
# now should be equal to = dt.datetime.now().date() for it to function properly
def is_business_day(now):
    headers = {'user-agent': 'PostmanRuntime/7.26.5'}
    endpoint = "https://www.nseindia.com/api/holiday-master?type=trading"
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        holidays_json = response.json().get('FO', [])
        holidays_df = pd.DataFrame(holidays_json)
        holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'])
        print(now)
        print(holidays_df)
        return not(pd.Timestamp(now) in holidays_df['tradingDate'].values)
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching holiday data: {e}")
        return True

# Function to login that returns headers and message
def my_login(api_key,pwd,username,tokenenv):
    """
    Login to the API and return headers and message.

    Parameters:
    - api_key (str): API key for authentication.
    - username (str): Username for login.
    - pwd (str): Password for login.

    Returns:
    - tuple: Headers and message.
    """
    smartApi = SmartConnect(api_key)

    try:
        totp = pyotp.TOTP(tokenenv).now()
    except Exception as e:
        logging.error("Invalid Token: The provided token is not valid.")
        raise e

    try:
        data = smartApi.generateSession(username, pwd, totp)
    except Exception as e:
        logging.error(f"Error generating session: {e}")
        return None, None

    if not data['status']:
        logging.error(data)
        return None, None
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
            'X-PrivateKey': api_key  # Include api_key dynamically in the header
        }
    return headers, msg

# Function to fetch funds it returns available cash of type float
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
        # return 15000#funds_dict
        return float(funds_dict['data']['availablecash'])
    except Exception as e:
        logger.error(f"An error occured: {e}")
        return None

# returns historical data from start date to end date
# Example 
# Timestamp                  Open    High    Low     Close   Volume
# 2024-10-21 00:00:00+05:30  551.60  561.90  547.00  548.10  11983482.0
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


# Function to check if to invest or not
# Have to remove this code in real implementation
def invest(available_cash):
    """
    Check if the available cash is sufficient for investing.

    Parameters:
    - available_cash (float or int): The amount of available cash.

    Returns:
    - bool: True if available_cash is greater than or equal to 10,000, otherwise False.
    """
    if not isinstance(available_cash, (int, float)):
        raise ValueError("available_cash must be an integer or float")
    
    return available_cash >= 10000


# Calculates DEMA
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

# Calculates brokerage in real time using angel one api
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
    
# Function to send Mail to recipients/Traders
# This mailing is for me so that i can know when stocks are bought and sold of my clients
def send_email(message):
    """
    Send an email with a table containing the data.

    Parameters:
    - message (List[Union[str, List[str]]]): The data to be included in the table. 
      The first item in the list determines the action ('BUY' or 'SELL'), and the rest are table rows.
    """
    # Create email message object
    # Log the received message
    # logging.info(f"Received message to send: {message}")
    email_pass = os.getenv('EMAIL_PASS')
    msg = EmailMessage()
    
    # Determine table headers based on the action
    action = message[0][0] 
    if action == 'BUY':
        t_headers = ["Action", "Quantity", "Stock", "Stock Token", "Date", "Buy Price", "Stop Loss"]
    else:
        t_headers = ["Action", "Quantity", "Stock", "Stock Token", "Date", "Sell Price", "Stop Loss"]

    # Construct the HTML content for the table
    table_headers = ''.join([f"<th style='padding: 7px;'>{header}</th>" for header in t_headers])
    table_rows = ''.join([
        '<tr>' + ''.join([f"<td style='padding: 7px;'>{cell}</td>" for cell in row]) + '</tr>'
        for row in message  # Skip the first item if it's the action
    ])
    
    html_content = f"""
    <html>
        <body>
            <div style="text-align: left;">
                <table border="1" style="margin-left: 0; margin-right: auto; text-align: center;">
                    <thead>
                        <tr>{table_headers}</tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                <p></p>
                <p style="color:blue">Note: <bold>Create a Good-Till-Triggered (GTT) order</bold> for your stop loss so that you save your money</p>
                <p></p>
                <p style="color:red">Note: This is a system-generated email. Do your analysis before investing.</p>
            </div>
        </body>
    </html>
    """
    
    # Set the email content to HTML
    msg.add_alternative(html_content, subtype='html')

    sender_email = 'dora42240@gmail.com'
    recipients = ['vu4f2122034@pvppcoe.ac.in','mitulcha13@gmail.com','shaneesharma33@gmail.com','nikhilmali810@gmail.com','Ayushghag99@gmail.com','ramdaschaugale33@gmail.com','shaamakm@gmail.com'] #, 'babudora00@gmail.com']
    
    msg['Subject'] = "Trading details from Surya"
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, email_pass)  # email_pass is an environment secret variable
            smtp.send_message(msg)
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send email. Error: {str(e)}")

# Function to check buy condition 
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



