import math
import pandas as pd
import datetime as dt
import time
import csv
import logincred
import login
import gttrules
import normalorder
import holdings
from getfunds import myfunds
import historyAngelandNSE
import nselib
import history
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
def login_to_platform():
    try:
        data = login.my_login(logincred.api_key, logincred.username, logincred.pwd)
        if data is None:
            print("Login failed: No response from the server.")
            return None
        
        msg = data.get('message')
        if msg is None:
            print("Login failed: 'message' key not found in response.")
            return None
        
        return msg
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return None


# Function to collect today's data
def collect_today_data(company_file, file_path):
    with open(company_file, mode='r') as file:
        csv_reader = csv.reader(file)
        start_date = (dt.datetime.now().replace(hour=9, minute=15) - dt.timedelta(days=30)).strftime('%Y-%m-%d %H:%M')
        end_date = dt.datetime.now().replace(hour=15, minute=30).strftime('%Y-%m-%d %H:%M')
        for i, row in enumerate(csv_reader):
            for company in row:
                name_to_search = company
                symbol_token, trading_symbol = history.search_symbol_by_name(name_to_search, file_path)
                if symbol_token and trading_symbol:
                    history.myhistory("NSE", symbol_token, "ONE_DAY", start_date, end_date, trading_symbol)
                if i % 3 == 0:
                    time.sleep(1)

# Function to check funds availability
def check_funds():
    funds = myfunds()
    available_funds = float(funds['data']['availablecash'])
    # return available_funds
    return 10000

# Calculate DEMA
def calculate_dema(data, period):
    ema = data['Close'].ewm(span=period, adjust=False).mean()
    dema = 2 * ema - ema.ewm(span=period, adjust=False).mean()
    return dema

# Function to perform trading strategy
def trading_strategy(data, available_funds, max_holding_period):
    invested = False
    buy_price = 0
    buy_quantity = 0
    invested_company = None
    sl = 0
    target_not_achieved = False
    positions = []

    today = data.iloc[-1]
    previous = data.iloc[-2]

    if not invested and \
       today['Volume'] / previous['Volume'] >= 4 and \
       (today['Close'] - previous['Close']) / previous['Close'] * 100 >= 4 and \
       today['High'] > previous['High'] and \
       calculate_dema(data, 5).iloc[-1] > calculate_dema(data, 8).iloc[-1] > calculate_dema(data, 13).iloc[-1] and \
       today['Close'] > today['Open']:
        
        max_shares = math.floor(available_funds / today['Close'])
        
        if max_shares > 0:
            buy_price = today['Close']
            buy_quantity = max_shares
            invested = True
            invested_company = data
            available_funds -= buy_price * buy_quantity
            sl = today['Low'] - (today['Low'] * 0.03)
            target_not_achieved = False
            positions.append(('Buy', today.name, buy_price, buy_quantity, available_funds))

            # Send WhatsApp message
            send_whatsapp_message(f"Bought {buy_quantity} shares of {data.name} at {buy_price}")

            # Update investment.csv
            update_investment_csv('buy', data.name, buy_price, buy_quantity, sl, 0)

    # Sell conditions
    if invested:
        day_counter = invested_company['day_counter'].iloc[-1]
        if day_counter != max_holding_period:
            future_data = data.iloc[-i]

            # Check for 4% target
            if not target_not_achieved and future_data['High'] >= buy_price * 1.04:
                if calculate_dema(data[:future_data], 5).iloc[-1] > calculate_dema(data[:future_data], 8).iloc[-1]:
                    sl = buy_price * 1.02
                    target_not_achieved = True
                else:
                    sell_price = buy_price * 1.04 
                    positions.append(('Sell (4% Target Hit)', future_data.name, sell_price, buy_quantity, available_funds))
                    invested = False
            elif future_data['Low'] <= sl:
                sell_price = sl
                positions.append(('Sell (SL)', future_data, sell_price, buy_quantity, available_funds))
                invested = False
            elif calculate_dema(data[:future_data], 5).iloc[-1] < calculate_dema(data[:future_data], 8).iloc[-1]:
                sell_price = future_data['Close']
                positions.append(('Sell (DEMA)', future_data, sell_price, buy_quantity, available_funds))
                invested = False
        elif day_counter == max_holding_period:
            sell_price = future_data['Close']
            positions.append(('Sell (Max Holding Period)', future_data, sell_price, buy_quantity, available_funds))
            invested = False

    return positions, available_funds

def send_whatsapp_message(message):
    try:
        driver_path = r'C:\Users\Surya\Downloads\Exe files\chromedriver-win64\chromedriver.exe'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
        
        driver.get('https://web.whatsapp.com/')
        time.sleep(15)  # Allow time to scan QR code and load WhatsApp

        contact_names = ["+918689905648", "+912345678901", "+919876543210"]  # Add the contact numbers here
        for contact_name in contact_names:
            search_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(contact_name)
            time.sleep(2)

            contact_title = driver.find_element_by_xpath(f'//span[@title="{contact_name}"]')
            contact_title.click()
            time.sleep(2)

            message_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="1"]')
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            time.sleep(2)
            print(f"Message sent to {contact_name}: {message}")

        driver.quit()
    except Exception as e:
        print(f"Failed to send message. Error: {str(e)}")

def update_investment_csv(action, symbol, price=None, quantity=None, sl=None, day_counter=None):
    file_path = 'investment.csv'
    try:
        investments_df = pd.read_csv(file_path)
    except FileNotFoundError:
        investments_df = pd.DataFrame(columns=['symbol', 'action', 'buydate', 'price', 'quantity', 'sl', 'day_counter'])

    if action == 'buy':
        new_row = {
            'symbol': symbol,
            'action': 'buy',
            'buydate': dt.datetime.now().strftime('%Y-%m-%d'),
            'price': price,
            'quantity': quantity,
            'sl': sl,
            'day_counter': day_counter
        }
        investments_df = investments_df.append(new_row, ignore_index=True)
    elif action == 'update_sl':
        # Update stop-loss (sl) for the symbol if it exists
        if symbol in investments_df['symbol'].values:
            investments_df.loc[investments_df['symbol'] == symbol, 'sl'] = sl
            investments_df.loc[investments_df['symbol'] == symbol, 'action'] = 'update_sl'
        else:
            print(f"Symbol {symbol} not found in the investment dataframe. No updates were made.")
    elif action == 'sell':
        # Remove the row corresponding to the symbol
        investments_df = investments_df[investments_df['symbol'] != symbol]

    # Write back to CSV
    investments_df.to_csv(file_path, index=False)

def increment_day_counter():
    file_path = 'investment.csv'
    try:
        investments_df = pd.read_csv(file_path)
        investments_df['day_counter'] += 1
        investments_df.to_csv(file_path, index=False)
    except FileNotFoundError:
        pass  # If the file doesn't exist, do nothing

def main():
    max_holding_period = 23
    now = dt.datetime.now() - dt.timedelta(days=1)
    
    if is_business_day(now): # now.strftime('%H:%M') == '15:15' and  
        msg = login_to_platform()
        print(msg)
        if msg:
            increment_day_counter()

            try:
                investments_df = pd.read_csv('investment.csv')
                invested_symbols = investments_df['symbol'].tolist()
            except FileNotFoundError:
                investments_df = pd.DataFrame(columns=['symbol', 'action', 'buydate', 'price', 'quantity', 'sl', 'day_counter'])
                invested_symbols = []

            available_funds = check_funds()

            if available_funds < 1000:
                for symbol in invested_symbols:
                    start_date = (dt.datetime.now().replace(hour=9, minute=15) - dt.timedelta(days=30)).strftime('%Y-%m-%d %H:%M')
                    end_date = dt.datetime.now().replace(hour=15, minute=30).strftime('%Y-%m-%d %H:%M')
                    data = history.myhistory("NSE", symbol, "ONE_DAY", start_date, end_date, symbol)
                    sell_positions, available_funds = trading_strategy(data, available_funds, max_holding_period)
                    for position in sell_positions:
                        action, date, price, quantity, capital = position
                        if action == 'Sell':
                            update_investment_csv('sell', symbol, None, None, None, None)
                            send_whatsapp_message(f"Sold {quantity} shares of {symbol} at {price}")
                        elif action == 'update_sl':
                            sl = price
                            update_investment_csv('update_sl', symbol, None, None, sl, None)
                            send_whatsapp_message(f"Updated stop-loss for {symbol} to {sl}")

            if available_funds > 1000:
                companies = ['nifty50.csv', 'niftynext50.csv', 'niftymidcap50.csv']
                for company_file in companies:
                    collect_today_data(company_file, 'OpenAPIScript.csv')
                    print(symbol)
                    for symbol in pd.read_csv(company_file)['Symbol']:
                        if symbol not in invested_symbols:
                            data = history.myhistory("NSE", symbol, "ONE_DAY", start_date, end_date, symbol)
                            buy_positions, available_funds = trading_strategy(data, available_funds, max_holding_period)
                            for position in buy_positions:
                                action, date, price, quantity, capital = position
                                if action == 'Buy':
                                    sl = price * 0.97
                                    update_investment_csv('buy', symbol, price, quantity, sl, 0)
                                    send_whatsapp_message(f"Bought {quantity} shares of {symbol} at {price}")

if __name__ == '__main__':
    main()
