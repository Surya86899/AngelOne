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
    """
        Check if the given date is a business (trading) day.

        Parameters:
        - now (datetime): The date to check.

        Returns:
        - bool: True if the date is a trading day, False if it is a holiday. (Returns true even if it is a weekend as github takes care of weekdays and weekends)
    """
    headers = {'user-agent': 'PostmanRuntime/7.26.5'}
    endpoint = "https://www.nseindia.com/api/holiday-master?type=trading"
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        holidays_json = response.json().get('FO', [])
        holidays_df = pd.DataFrame(holidays_json)
        holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'])
        logging.info(now)
        logging.info(holidays_df)
        return not(pd.Timestamp(now) in holidays_df['tradingDate'].values)
    except (requests.RequestException, KeyError, ValueError) as e:
        logging.error(f"Error fetching holiday data: {e}")
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
    """
        Fetch available funds in the account.

        Parameters:
        - headers (): Validation token

        Returns:
        - float: Available cash in the account in float format.
    """
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
        # logging.info(data)

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

# *************************************Trading functions*************************************

# 1] Normal Orders

# Creates normal buy order 
def create_normal_order(headers, variety: str, trading_symbol: str, symbol_token: str, transaction_type: str, exchange: str, order_type: str, product_type: str, duration: str, price: str, square_off: str, stop_loss: str, qty: str):
    """
    Create Normal Order
        Parameters:
        - headers (Dict[str, str]): HTTP headers including authentication tokens.
        - variety (str): Type of Order (e.g., "NORMAL","STOPLOSS","AMO","ROBO").
        - trading_symbol (str): Symbol of the stock. (e.g., "ABB-EQ", "SBIN-EQ").
        - symbol_token (str): Token for the stock symbol.
        - transaction_type (str): Type of transaction (e.g., "BUY" or "SELL").
        - exchange (str): Exchange name (e.g., "NSE").
        - order_type (str): Another type of order (e.g., "MARKET","LIMIT","STOPLOSS_LIMIT","STOPLOSS_MARKET").
        - product_type (str): Another type of order (e.g., "DELIVERY","CARRYFORWARD","MARGIN","INTRADAY",BO).
        - price (str): Price per unit of the stock. (Kept 0 here or it will become Limit order).
        - square_off (str): Only For ROBO (Bracket Order).
        - stop_loss (str): Only For ROBO (Bracket Order).
        - qty (str): Quantity of the stock to be traded.

        Returns:
        - str: unique_order_id if successful.
        - None: if there is an error.
    """
    import http.client
    import json
    import certifi

    try:
        # Specify the path to the CA certificates file
        ca_file = certifi.where()
        logging.info(f"CA Certificates Path: {ca_file}")

        # Create an HTTPSConnection with the specified CA certificates file
        conn = http.client.HTTPSConnection(
            'apiconnect.angelbroking.com',
            context=http.client.ssl._create_default_https_context(cafile=ca_file)
        )

        # Construct the payload
        payload = {
            "variety": variety,
            "tradingsymbol": trading_symbol,
            "symboltoken": symbol_token,
            "transactiontype": transaction_type,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": product_type,
            "duration": duration,
            "price": price,
            "squareoff": square_off,
            "stoploss": stop_loss,
            "quantity": qty
        }
        payload_str = json.dumps(payload)

        # Send the POST request
        conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)

        # Get and decode the response
        res = conn.getresponse()
        data = res.read()
        response_text = data.decode("utf-8")
        logging.info(f"Response: {response_text}")

        # Parse the response
        response_json = json.loads(data)
        if 'data' in response_json and 'uniqueorderid' in response_json['data']:
            unique_order_id = response_json['data']['uniqueorderid']
            return unique_order_id
        else:
            logging.error("Error: Unexpected response format.")
            logging.info(f"Response JSON: {response_json}")
            return None

    except http.client.HTTPException as http_error:
        logging.error(f"HTTP Exception occurred: {http_error}")
        return None

    except json.JSONDecodeError as json_error:
        logging.error(f"JSON Decode Error: {json_error}")
        return None

    except KeyError as key_error:
        logging.error(f"KeyError: {key_error}. Check if 'data' and 'uniqueorderid' exist in the response.")
        return None

    except Exception as general_error:
        logging.error(f"An unexpected error occurred: {general_error}")
        return None

#  The order book typically contains information about all open orders placed by a user, including details such as order ID, order type, product type, quantity, price, and status.
def get_normal_orderbook(headers):
    """
    Fetch the Normal Order Book.
    
    Parameters:
    - headers (Dict[str, str]): HTTP headers including authentication tokens.
    
    Returns:
    - dict: Parsed JSON response if successful.
    - dict: Error message if there is an issue.
    """
    try:
        # Configure HTTPS connection with CA certificates
        ca_file = certifi.where()
        conn = http.client.HTTPSConnection(
            "apiconnect.angelbroking.com",
            context=http.client.ssl._create_default_https_context(cafile=ca_file),
            timeout=10  # Timeout in seconds
        )
        
        # Send the GET request
        conn.request("GET", "/rest/secure/angelbroking/order/v1/getOrderBook", "", headers)
        res = conn.getresponse()

        # Process response
        if res.status == 200:
            data = res.read().decode("utf-8")
            logging.info("Order book fetched successfully.")
            return json.loads(data)
        else:
            error_message = f"Error fetching order book: {res.status} {res.reason}"
            logging.error(error_message)
            return {"error": error_message}
    
    except http.client.HTTPException as http_error:
        logging.error(f"HTTP Exception occurred: {http_error}")
        return {"error": str(http_error)}
    
    except json.JSONDecodeError as json_error:
        logging.error(f"JSON Decode Error: {json_error}")
        return {"error": "Invalid JSON response"}
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return {"error": str(e)}
    
    finally:
        conn.close()

# 2] GTT Orders

def create_gtt_rule(headers, trading_symbol, symbol_token, exchange, transaction_type, product_type, price, qty, trigger_price, disclosed_qty):
    """
    Create a GTT (Good Till Trigger) Rule and log it to a CSV file.
    
    Parameters:
    - headers (dict): HTTP headers with authentication tokens.
    - trading_symbol (str): Symbol of the stock (e.g., "ABB-EQ").
    - symbol_token (str): Token for the stock symbol.
    - exchange (str): Exchange name (e.g., "NSE").
    - transaction_type (str): Type of transaction ("BUY" or "SELL").
    - product_type (str): Product type ("DELIVERY", "MARGIN", etc.).
    - price (str): Price per unit for the GTT rule.
    - qty (str): Quantity for the GTT rule.
    - trigger_price (str): Trigger price for the rule.
    - disclosed_qty (str): Disclosed quantity for the rule.
    
    Returns:
    - dict: API response data.
    """
    try:
        # Specify the path to the CA certificates file
        ca_file = certifi.where()
        conn = http.client.HTTPSConnection(
            'apiconnect.angelbroking.com',
            context=http.client.ssl._create_default_https_context(cafile=ca_file),
            timeout=10  # Set timeout for the connection
        )

        # Prepare the payload
        payload = {
            "tradingsymbol": trading_symbol,
            "symboltoken": symbol_token,
            "exchange": exchange,
            "transactiontype": transaction_type,
            "producttype": product_type,
            "price": price,
            "qty": qty,
            "triggerprice": trigger_price,
            "disclosedqty": disclosed_qty
        }

        # Log the request payload
        logging.info(f"Creating GTT Rule with payload: {payload}")

        # Send the POST request
        conn.request("POST", "/rest/secure/angelbroking/gtt/v1/createRule", json.dumps(payload), headers)
        res = conn.getresponse()

        # Check response status
        if res.status != 200:
            error_message = f"Failed to create GTT rule: {res.status} {res.reason}"
            logging.error(error_message)
            return {"error": error_message}

        # Parse the response
        data = res.read().decode("utf-8")
        response_data = json.loads(data)

        # Extract rule ID
        rule_id = response_data.get("data", {}).get("id")
        if not rule_id:
            logging.error(f"Unexpected response format: {response_data}")
            return {"error": "Rule creation failed, no rule ID in response"}

        logging.info(f"GTT Rule created successfully with ID: {rule_id}")

        # Log rule details to CSV
        try:
            with open("gtt_rules.csv", "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([rule_id, trading_symbol, symbol_token, transaction_type, product_type, price, qty, trigger_price, disclosed_qty])
            logging.info("Rule details appended to gtt_rules.csv.")
        except IOError as csv_error:
            logging.error(f"Failed to write rule to CSV: {csv_error}")

        return response_data

    except http.client.HTTPException as http_error:
        logging.error(f"HTTP Exception occurred: {http_error}")
        return {"error": str(http_error)}

    except json.JSONDecodeError as json_error:
        logging.error(f"JSON Decode Error: {json_error}")
        return {"error": "Invalid JSON response"}

    except Exception as general_error:
        logging.error(f"An unexpected error occurred: {general_error}")
        return {"error": str(general_error)}

    finally:
        conn.close()

def get_gtt_rule_details(headers, rule_id):
    """
    Retrieve details of a GTT (Good Till Trigger) Rule by its ID.
    
    Parameters:
    - headers (dict): HTTP headers with authentication tokens.
    - rule_id (str): ID of the GTT rule to retrieve details for.
    
    Returns:
    - dict: Rule details if successful.
    - dict: Error details in case of failure.
    """
    try:
        # Specify the path to the CA certificates file
        ca_file = certifi.where()

        # Create an HTTPSConnection with the specified CA certificates file
        conn = http.client.HTTPSConnection(
            'apiconnect.angelbroking.com',
            context=http.client.ssl._create_default_https_context(cafile=ca_file),
            timeout=10  # Set timeout for the connection
        )

        # Construct the payload with the rule ID
        payload = {
            "id": rule_id
        }
        
        # Log the request payload
        logging.info(f"Fetching details for GTT Rule ID: {rule_id}")

        # Make the POST request to retrieve details of the GTT rule
        conn.request("POST", "/rest/secure/angelbroking/gtt/v1/ruleDetails", json.dumps(payload), headers)

        # Get the response
        res = conn.getresponse()
        
        # Check response status
        if res.status != 200:
            error_message = f"Failed to fetch GTT rule details: {res.status} {res.reason}"
            logging.error(error_message)
            return {"error": error_message}

        # Parse the response data
        data = res.read().decode("utf-8")
        response_data = json.loads(data)

        # Log the successful response
        logging.info(f"GTT Rule Details: {response_data}")

        return response_data

    except http.client.HTTPException as http_error:
        logging.error(f"HTTP Exception occurred: {http_error}")
        return {"error": str(http_error)}

    except json.JSONDecodeError as json_error:
        logging.error(f"JSON Decode Error: {json_error}")
        return {"error": "Invalid JSON response"}

    except Exception as general_error:
        logging.error(f"An unexpected error occurred: {general_error}")
        return {"error": str(general_error)}

    finally:
        conn.close()

# *****************Buy Share and sell gtt function *****************
def buy_shares(headers, symbol: str, token: str, qty: str, sl: float):
    """
    Function to automate buying shares and setting a GTT sell rule.
    
    Parameters:
    - headers (dict): HTTP headers for authentication.
    - symbol (str): Trading symbol of the stock.
    - token (str): Token representing the stock.
    - qty (str): Quantity of shares to buy.
    - sl (float): Stop-loss price for the sell order.
    
    Returns:
    - dict: Final status of the buy and GTT setup process.
    """
    
    # Common parameters for the buy order
    price = square_off = stop_loss = "0"
    variety = "NORMAL"
    exchange = "NSE"
    order_type = "MARKET"
    product_type = "DELIVERY"
    duration = "DAY"
    max_attempts = 2

    # Step 1: Place a normal buy order
    logging.info("Attempting to place a buy order.")
    for attempt in range(max_attempts):
        order_id = create_normal_order(
            headers, variety, symbol, token, "BUY", exchange, 
            order_type, product_type, duration, price, square_off, 
            stop_loss, qty
        )

        # Fetch the latest order book to verify order status
        orderbook = get_normal_orderbook(headers)
        if not orderbook:
            logging.error("Failed to fetch order book. Retrying...")
            continue

        # Check the latest order status
        last_order = orderbook.get("data", [])[-1] if orderbook.get("data") else None
        if last_order and last_order.get("orderstatus") != "rejected":
            logging.info(f"Buy order placed successfully: {last_order}")
            break
        else:
            logging.warning(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)  # Small delay before retry
    else:
        logging.error("Buy order failed after maximum attempts.")
        return {"status": "failure", "reason": "Buy order rejected"}

    # Step 2: Set a GTT Sell rule
    logging.info("Attempting to set a GTT Sell rule.")
    for attempt in range(max_attempts):
        risk_trigger_price = sl
        risk_price = sl - 5

        rule_id = create_gtt_rule(
            headers, symbol, token, exchange, "SELL", product_type, 
            risk_price, qty, risk_trigger_price, qty
        )

        if not rule_id:
            logging.error("Failed to create GTT rule. Retrying...")
            time.sleep(2)
            continue

        # Verify the status of the GTT rule
        gtt_details = get_gtt_rule_details(headers, rule_id)
        if gtt_details and gtt_details.get("data", {}).get("status") == "NEW":
            logging.info(f"GTT Sell rule created successfully: {gtt_details}")
            return {"status": "success", "buy_order_id": order_id, "gtt_rule_id": rule_id}
        else:
            logging.warning(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)
    else:
        logging.error("GTT Sell rule creation failed after maximum attempts.")
        return {"status": "failure", "reason": "GTT rule creation failed"}

# *************************************Trading functions*************************************

# min_cash_to_buy is the minimum amount of cash that should be available to buy shares (10000,30000) (e.g. 10000)
# risk is to keep the sl below close (less risk less profit) / low (more risk more profit)           (e.g. "low")
def checkforinvestmentopportunities(headers, companiesdict: Dict[str, str], available_cash: float, min_cash_to_buy: float, start_date: str, end_date: str, risk: str):
    """
    Check for investment opportunities based on historical data and available cash.

    Parameters:
    - headers (dict): HTTP headers for API requests.
    - companiesdict (Dict[str, str]): Dictionary with company symbols and their tokens.
    - available_cash (float): Amount of cash available for investment.
    - min_cash_to_buy (float): Minimum amount of cash to initiate an investment.
    - start_date (str): Start date for historical data in format '%Y-%m-%d'.
    - end_date (str): End date for historical data in format '%Y-%m-%d'.
    - risk (str): Column name to determine stop-loss (e.g., 'Close', 'Low').
    
    Returns:
    - List[Dict]: List of successful investment details.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    investments = []

    for i, (symbol, token) in enumerate(companiesdict.items(), start=1):
        # Check if there is enough cash to proceed
        if available_cash < min_cash_to_buy:
            logging.info("Available cash is below the minimum threshold. Exiting.")
            break

        try:
            # Fetch historical data for the company
            logging.info(f"Fetching historical data for {symbol}...")
            historical_data = myhistory(headers, "NSE", token, "ONE_DAY", start_date, end_date)
            if historical_data.empty:
                logging.warning(f"No historical data available for {symbol}. Skipping.")
                continue

            # Check investment criteria
            if to_invest(historical_data):
                today = historical_data.iloc[-1]  # Get the latest day's data
                max_shares = math.floor(available_cash / today["Close"])
                logging.info(f"Calculated max shares for {symbol}: {max_shares}")

                if max_shares > 0:
                    # Calculate stop-loss price
                    sl = today[risk] - (today[risk] * 0.03)
                    full_symbol = f"{symbol}-EQ"

                    # Execute the buy order
                    buy_response = buy_shares(headers, full_symbol, token, str(max_shares), sl)
                    if buy_response and buy_response["status"] == "success":
                        # Record the investment details
                        investment_details = {
                            "transaction_type": "BUY",
                            "shares": max_shares,
                            "symbol": full_symbol,
                            "token": token,
                            "date": today["Timestamp"].strftime('%Y-%m-%d'),
                            "price": today["Close"],
                            "stop_loss": sl
                        }
                        investments.append(investment_details)
                        logging.info(f"Investment successful for {symbol}: {investment_details}")

                        # Update available cash
                        available_cash -= max_shares * today["Close"]

                        break # As investment is done and there is no cash left for further investment
                    else:
                        logging.error(buy_response["reason"])
                else:
                    logging.warning(f"Insufficient cash to buy even one share of {symbol}. Skipping.")

        except Exception as e:
            logging.error(f"Error processing {symbol}: {e}")

        # Add delay every 3 requests to avoid rate-limiting
        if i % 3 == 0:
            logging.info("Adding a delay to avoid rate-limiting...")
            time.sleep(1)

    # # If there are new investments, send email and save to CSV
    if investment_details:
        send_email(investments)
        # save_in_csv(investments)




