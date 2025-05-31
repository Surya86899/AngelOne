import http.client
import time
import certifi
import json
import csv

import logincred    # Contains my login credentials
import login        # Contains my login code

import gttrules     # Contains gttrules operations code
import holdings     # Contains holding getting code
from getfunds import myfunds    # Contains fund getting code

import datetime as dt

import logout       # Contains my login code
from headers import headers     # Contains headers
import getprofile       # Contains my profile code
import history
import historyAngelandNSE
import normalorder      # Contains my normal order manipulation code

# ************************Login****************************
jwt_token = login.my_login(logincred.api_key, logincred.username, logincred.pwd)
# *********************************************************


# ************************Logout****************************
# logout.my_logout()
# **********************************************************


# ************************Profile****************************
# getprofile.profile()
# **********************************************************

# ************************Historical Candle data****************************
# File path for the OpenAPIScripMaster.csv
# file_path = 'OpenAPIScripMaster.csv'
# # Name to search for
# name_to_search = 'ABB'

# # Searching for symbol and token based on the name
# symbol_token,trading_symbol = history.search_symbol_by_name(name_to_search, file_path)
# print (symbol_token,trading_symbol)

# if symbol_token and trading_symbol:
#     print(f"Token: {symbol_token}, Symbol: {trading_symbol}")
#     # Retrieving historical data for the symbol and token
#     for i in range(2020, 2025):  # Adjust the range as per your requirement
#         # history.myhistory("NSE", symbol_token, "ONE_DAY", f"{i}-12-31 09:00", f"{i+1}-12-31 03:30",trading_symbol)
#         # historydelivery.myhistory("NSE", symbol_token, "ONE_DAY", f"{i}-01-01 09:00", f"{i}-12-31 03:30","M&M")
#         historyAngelandNSE.merge_and_save_data(trading_symbol, "NSE", symbol_token, "ONE_DAY", f"{i}-01-01 09:00", f"{i}-12-31 03:30", file_path)
# else:
#     print("Name not found.")

# ************************Historical Candle data****************************



# ************************ Historical Candle data through file for 1 day data ****************************

# # File path for the OpenAPIScripMaster.csv
# file_path = 'OpenAPIScript.csv'
# company_list = ['nifty50.csv','niftynext50.csv','niftymidcap50.csv']

# # Specify the starting line number
# start_line_number = 0 # Change this to your desired starting line number

# # Open the CSV file and read the contents
# for company_names in company_list:
#     with open(company_names, mode='r') as file:
#         csv_reader = csv.reader(file)
#         line_counter = 0
        
#         for row in csv_reader:
#             line_counter += 1
            
#             # Skip lines until the starting line number
#             if line_counter < start_line_number:
#                 continue
            
#             for company in row:
#                 # print(company)
#                 # Name to search for
#                 name_to_search = company

#                 # Searching for symbol and token based on the name
#                 symbol_token, trading_symbol = history.search_symbol_by_name(name_to_search, file_path)
#                 print(symbol_token, trading_symbol)

#                 if symbol_token and trading_symbol:
#                     print(f"Token: {symbol_token}, Symbol: {trading_symbol}")
#                     # Retrieving historical data for the symbol and token
#                     for i in range(2024, 2025):  # Adjust the range as per your requirement
#                         history.myhistory("NSE", symbol_token, "ONE_DAY", f"{i}-12-31 09:00", f"{i+1}-12-31 03:30", trading_symbol)
#                         time.sleep(1)
#                         # historydelivery.myhistory("NSE", symbol_token, "ONE_DAY", f"{i}-01-01 09:00", f"{i}-12-31 03:30", trading_symbol)
#                         # historyAngelandNSE.merge_and_save_data(trading_symbol, "NSE", symbol_token, "ONE_DAY", f"{i}-01-01 09:00", f"{i}-12-31 03:30", file_path)
#                 else:
#                     print(f"Name of {company} not found.")
#             # time.sleep(1)

# ************************Historical Candle data through file****************************

# ************************ Historical Candle data through file for different time ****************************

# import csv
# import time
# from datetime import timedelta
# import pandas as pd

# # === CONFIGURATION ===
# INTERVAL = "ONE_HOUR"   # change this only
# START_DATE = "2023-01-01"
# END_DATE = "2025-05-31"
# FILE_PATH = 'OpenAPIScript.csv'
# COMPANY_LIST = ['nifty50.csv', 'niftynext50.csv', 'niftymidcap50.csv']
# START_LINE_NUMBER = 0

# # === DYNAMIC INTERVAL MAPPING ===
# INTERVAL_CONFIG = {
#     "ONE_MINUTE": {"minutes": 1, "max_days": 5},
#     "THREE_MINUTE": {"minutes": 3, "max_days": 10},
#     "FIVE_MINUTE": {"minutes": 5, "max_days": 20},
#     "TEN_MINUTE": {"minutes": 10, "max_days": 30},
#     "FIFTEEN_MINUTE": {"minutes": 15, "max_days": 40},
#     "THIRTY_MINUTE": {"minutes": 30, "max_days": 60},
#     "ONE_HOUR": {"minutes": 60, "max_days": 90},
#     "ONE_DAY": {"minutes": 1440, "max_days": 365}
# }

# def chunk_dates(start_date, end_date, interval):
#     config = INTERVAL_CONFIG.get(interval, {"minutes": 15, "max_days": 30})
#     max_days = config["max_days"]
#     chunks = []

#     start = pd.to_datetime(start_date + " 09:00")
#     end = pd.to_datetime(end_date + " 15:30")

#     while start < end:
#         chunk_end = min(start + timedelta(days=max_days - 1), end)
#         chunks.append((start.strftime('%Y-%m-%d %H:%M'), chunk_end.strftime('%Y-%m-%d %H:%M')))
#         start = chunk_end + timedelta(minutes=config["minutes"])

#     return chunks

# # === MAIN SCRIPT ===
# for company_csv in COMPANY_LIST:
#     with open(company_csv, mode='r') as file:
#         csv_reader = csv.reader(file)
#         line_counter = 0

#         for row in csv_reader:
#             line_counter += 1
#             if line_counter < START_LINE_NUMBER:
#                 continue

#             for company_name in row:
#                 symbol_token, trading_symbol = history.search_symbol_by_name(company_name, FILE_PATH)
#                 print(f"\n🔍 Searching: {company_name}")

#                 if not symbol_token or not trading_symbol:
#                     print(f"❌ Not found: {company_name}")
#                     continue

#                 print(f"✅ Token: {symbol_token}, Symbol: {trading_symbol}")
#                 date_chunks = chunk_dates(START_DATE, END_DATE, INTERVAL)

#                 for start, end in date_chunks:
#                     print(f"➡ Fetching {INTERVAL} data from {start} to {end} for {trading_symbol}")
#                     history.myhistory("NSE", symbol_token, INTERVAL, start, end, trading_symbol)
#                     time.sleep(1.2)

# ************************Historical Candle data through file****************************


# if symbol_token and trading_symbol:
#     history.myhistory("NSE",symbol_token,"ONE_DAY","2024-05-28 09:00","2024-06-04 03:30",trading_symbol)
# else:
#      print("Name not found.")


# payload = {
#         "exchange": "NSE",
#         "symboltoken": "3045",
#         "interval": "ONE_DAY",
#         "fromdate": "2024-02-27 09:00",
#         "todate": "2024-04-08 03:30"
#     }

# Year on Year Data  (2020-12-31,2021-12-31),(2021-12-31,2022-12-31),(2022-12-31,2023-12-31),(2023-12-31,2024-12-31)
# **********************************************************


# *****************create gtt_rule function********************
# Example usage
# print("id = ",gttrules.create_gtt_rule("SBIN-EQ", "3045", "NSE", "BUY", "DELIVERY", "754", "50", "753.95", "50"))
# *************************************************************


# *****************modify gtt_rule function********************
# Example usage 
# gttrules.modify_gtt_rule(2819079, "SBIN-EQ", "3045", "NSE", "BUY", "DELIVERY", "755", "50", "753.95", "50", "20")
# *************************************************************


# *****************get rules gtt_rule function********************
# Example usage 
# gttrules.get_gtt_rule_details("3042419")
# *************************************************************


# *****************get all gtt_rule function********************
# # Example usage
# gttrule = gttrules.get_gtt_allrule_details()
# # print(gttrule)
# print(gttrule["data"][0]['tradingsymbol'])

# *************************************************************


# *****************cancel gtt_rule function********************
# Example usage
# gttrules.cancel_gtt_rule("2819079","3045","NSE")
# *************************************************************


# **********************get my holdings**********************
# # Example usage (Dono ka data holdings.csv mai save hota hai)
# holdings.myholdings()   # sirf stocks ka details      
# print("***************************************************************************************************")
# holdings.all_myholdings()   #stocks ke detail ke saath total(holding,invested,pnl,pnl in %)
# print("***************************************************************************************************")
# holdings.get_position()   # stock position track karne ke liye
# # holdings.convert_position()   # not yet ready
# *************************************************************


# *************************get my funds************************
# Example usage
# myfunds()
# *************************************************************

# *************************Normal Orders************************
# unique_order_id = normalorder.create_normal_order("NORMAL",trading_symbol,symbol_token,"BUY","NSE","MARKET","DELIVERY","DAY","0","0","0","1")

# print(unique_order_id)

# normalorder.modify_normal_order("NORMAL","201020000000080","LIMIT","INTRADAY","DAY","194.00","1")

# normalorder.cancel_normal_order("NORMAL","201020000000080")

# data = normalorder.get_normal_orderbook()
# print(data["data"][-1])

# data = normalorder.get_normal_individualorder(unique_order_id)

# normalorder.get_normal_tradebook()

# normalorder.get_ltp_data("NSE","SBIN-EQ","3045")

# *************************************************************

# ************************Historical 15 Min Candle data through file****************************

# # File path for the OpenAPIScripMaster.csv
# file_path = 'OpenAPIScripMaster.csv'
# # Name to search for
# name_to_search = 'ABB'

# # Searching for symbol and token based on the name
# symbol_token, trading_symbol = history.search_symbol_by_name(name_to_search, file_path)
# print(symbol_token, trading_symbol)

# if symbol_token and trading_symbol:
#     print(f"Token: {symbol_token}, Symbol: {trading_symbol}")
#     # Retrieving historical data for the symbol and token
#     start_date = "2024-01-01"
#     end_date = "2024-07-08"
#     interval = "FIFTEEN_MINUTE"
#     exchange = "NSE"
    
#     # Calculate number of days between start_date and end_date
#     from datetime import datetime, timedelta
#     date_format = "%Y-%m-%d %H:%M"
#     start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
#     end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    
#     # Initialize the start of the current month
#     current_month_start = start_datetime.replace(day=1, hour=9, minute=0)
    
#     while current_month_start <= end_datetime:
#         # Calculate end of current month
#         next_month_start = current_month_start + timedelta(days=31)
#         current_month_end = min(next_month_start - timedelta(seconds=1), end_datetime)
        
#         # Set the time to 15:30 for the end of the month
#         current_end_time = current_month_end.replace(hour=15, minute=45)
        
#         # Convert datetime objects to formatted strings
#         start_time_str = current_month_start.strftime(date_format)
#         end_time_str = current_end_time.strftime(date_format)
        
#         history.myhistory(exchange, symbol_token, interval, start_time_str, end_time_str, trading_symbol)
#         time.sleep(1)
        
#         # Move to the start of the next month
#         current_month_start = next_month_start
        
# else:
#     print("Name not found.")

# ************************Historical 15 Min Candle data through file****************************

