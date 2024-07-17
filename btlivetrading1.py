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
import pywhatkit as kit

# Function to check if today is a business day
def is_business_day():
    today = dt.datetime.now().date()
    print(today)
    holidays_df = nselib.trading_holiday_calendar()  # Assuming this returns a DataFrame
    holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'], format='%d-%b-%Y').dt.date
    
    holidays = holidays_df['tradingDate'].values  # Convert to array of datetime.date objects
    
    if today.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        return False
    if today in holidays:
        return False
    return True

# Function to login
def login_to_platform():
    jwt_token = login.my_login(logincred.api_key, logincred.username, logincred.pwd)
    return jwt_token

# Function to collect today's data
def collect_today_data(company_file, file_path):
    with open(company_file, mode='r') as file:
        csv_reader = csv.reader(file)
        i = 0
        start_date = (dt.datetime.now().replace(hour=9, minute=15) - dt.timedelta(days=30)).strftime('%Y-%m-%d %H:%M')
        end_date = dt.datetime.now().replace(hour=15, minute=30).strftime('%Y-%m-%d %H:%M')
        for row in csv_reader:
            for company in row:
                i += 1
                name_to_search = company
                symbol_token, trading_symbol = history.search_symbol_by_name(name_to_search, file_path)
                if symbol_token and trading_symbol:
                    history.myhistory("NSE", symbol_token, "ONE_DAY", start_date, end_date,trading_symbol)
                if i % 3 == 0:
                    time.sleep(1)

# Function to check funds availability
def check_funds():
    funds = myfunds()
    available_funds = float(funds['data']['availablecash'])
    return available_funds

# Calculate DEMA
def calculate_dema(data, period):
    ema = data['Close'].ewm(span=period, adjust=False).mean()
    dema = 2 * ema - ema.ewm(span=period, adjust=False).mean()
    return dema


# # Function to place a GTT order
# def place_gtt_order(jwt_token, symbol, symbol_token, buy_price, buy_quantity, sell_price, sl_price):
#     gtt_result = gttrules.create_gtt_rule(
#         symbol,
#         symbol_token,
#         "NSE",
#         "BUY",
#         "DELIVERY",
#         buy_price,
#         buy_quantity,
#         sell_price,
#         buy_quantity,
#         sl_price
#     )
#     return gtt_result

# # Function to place a normal order
# def place_normal_order(jwt_token, symbol, symbol_token, buy_price, buy_quantity):
#     order_result = normalorder.create_normal_order(
#         "NORMAL",
#         symbol,
#         symbol_token,
#         "BUY",
#         "NSE",
#         "LIMIT",
#         "DELIVERY",
#         "DAY",
#         buy_price,
#         "0",
#         "0",
#         buy_quantity
#     )
#     return order_result

# Function to perform trading strategy
def trading_strategy(jwt_token, data, available_funds,max_holding_period):
    invested = False
    buy_price = 0
    buy_quantity = 0
    invested_company = None
    sl = 0
    targetnotach = False
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
            targetnotach = False
            positions.append(('Buy', today.name, buy_price, buy_quantity, available_funds))

            # Place GTT order
            sell_price = buy_price * 1.04
            tosenddetails = [data.name,data['symbol_token'],buy_price,buy_quantity,sell_price,sl]
            # gtt_result = place_gtt_order(jwt_token, data.name, data['symbol_token'], buy_price, buy_quantity, sell_price, sl)
            kit.sendwhatmsg("+918689905648", tosenddetails, 22, 19) 

            # print("GTT order placed:", gtt_result)
    
    # Sell conditions
    if invested:
        for i in range(1, max_holding_period + 1):
            future_date = today.name + pd.DateOffset(days=i)
            if future_date in data.index:
                future_data = data.loc[future_date]

                # Check for 4% target
                if not targetnotach and future_data['High'] >= buy_price * 1.04:
                    sl = buy_price * 1.02
                    targetnotach = True
                elif future_data['Low'] <= sl:
                    sell_price = sl
                    positions.append(('Sell (SL)', future_date, sell_price, buy_quantity, available_funds))
                    invested = False
                    break
                elif calculate_dema(data[:future_date], 5).iloc[-1] < calculate_dema(data[:future_date], 8).iloc[-1]:
                    sell_price = future_data['Close']
                    positions.append(('Sell (DEMA)', future_date, sell_price, buy_quantity, available_funds))
                    invested = False
                    break
                elif i == max_holding_period:
                    sell_price = future_data['Close']
                    positions.append(('Sell (Max Holding Period)', future_date, sell_price, buy_quantity, available_funds))
                    invested = False
                    break

    return positions, available_funds

def main():
    # initial_capital = 10000
    max_holding_period = 23
    if dt.datetime.now().strftime('%H:%M') == '15:15' and is_business_day():
        jwt_token = login_to_platform()
        if jwt_token:
            # List of company CSV files to process
            companies = ['nifty50.csv', 'niftynext50.csv', 'niftymidcap50.csv']

            # Process each company file
            for company_file in companies:
                collect_today_data(company_file, 'OpenAPIScript.csv')
                
                # Execute the trading strategy
                available_cash = check_funds()
                print(available_cash)
                positions, final_funds = trading_strategy(jwt_token, data, available_funds, max_holding_period)
                
                # Log the positions to a CSV file
                df_positions = pd.DataFrame(positions, columns=['Action', 'Date', 'Price', 'Quantity', 'Capital'])
                df_positions.to_csv(f'trading_positions_{company_file}.csv', index=False, mode='a')

if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)  # Check every minute
