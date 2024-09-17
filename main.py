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
# jwt_token = login.my_login(logincred.api_key, logincred.username, logincred.pwd)
# *********************************************************


# ************************Logout****************************
# logout.my_logout()
# **********************************************************


# ************************Profile****************************
# getprofile.profile()
# **********************************************************

# ************************Historical Candle data****************************
# # File path for the OpenAPIScripMaster.csv
# file_path = 'OpenAPIScripMaster.csv'
# # Name to search for
# name_to_search = 'WIPRO'

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



# ************************Historical Candle data through file****************************

# File path for the OpenAPIScripMaster.csv
file_path = 'OpenAPIScript.csv'
company_names = 'niftymidcap50.csv'

# Specify the starting line number
start_line_number = 0 # Change this to your desired starting line number

# Open the CSV file and read the contents
with open(company_names, mode='r') as file:
    csv_reader = csv.reader(file)
    line_counter = 0
    
    for row in csv_reader:
        line_counter += 1
        
        # Skip lines until the starting line number
        if line_counter < start_line_number:
            continue
        
        for company in row:
            # print(company)
            # Name to search for
            name_to_search = company

            # Searching for symbol and token based on the name
            symbol_token, trading_symbol = history.search_symbol_by_name(name_to_search, file_path)
            print(symbol_token, trading_symbol)

            if symbol_token and trading_symbol:
                print(f"Token: {symbol_token}, Symbol: {trading_symbol}")
                # Retrieving historical data for the symbol and token
                for i in range(2020, 2025):  # Adjust the range as per your requirement
                    history.myhistory("NSE", symbol_token, "ONE_DAY", f"{i}-12-31 09:00", f"{i+1}-12-31 03:30", trading_symbol)
                    time.sleep(1)
                    # historydelivery.myhistory("NSE", symbol_token, "ONE_DAY", f"{i}-01-01 09:00", f"{i}-12-31 03:30", trading_symbol)
                    # historyAngelandNSE.merge_and_save_data(trading_symbol, "NSE", symbol_token, "ONE_DAY", f"{i}-01-01 09:00", f"{i}-12-31 03:30", file_path)
            else:
                print(f"Name of {company} not found.")
        # time.sleep(1)


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
# print("id = ",gttrules.create_gtt_rule("SBIN-EQ", "3045", "NSE", "BUY", "DELIVERY", "754", "50", "753.95", "50", "20"))
# *************************************************************


# *****************modify gtt_rule function********************
# Example usage 
# gttrules.modify_gtt_rule(2819079, "SBIN-EQ", "3045", "NSE", "BUY", "DELIVERY", "755", "50", "753.95", "50", "20")
# *************************************************************


# *****************get rules gtt_rule function********************
# Example usage 
# gttrules.get_gtt_rule_details("2819079")
# *************************************************************


# *****************get all gtt_rule function********************
# Example usage
# gttrules.get_gtt_allrule_details()
# *************************************************************


# *****************cancel gtt_rule function********************
# Example usage
# gttrules.cancel_gtt_rule("2819079","3045","NSE")
# *************************************************************


# **********************get my holdings**********************
# Example usage (Dono ka data holdings.csv mai save hota hai)
# holdings.myholdings()   # sirf stocks ka details    
# holdings.all_myholdings()   #stocks ke detail ke saath total(holding,invested,pnl,pnl in %)
# holdings.get_position()   # stock position track karne ke liye
# holdings.convert_position()   # not yet ready
# *************************************************************


# *************************get my funds************************
# Example usage
# myfunds()
# *************************************************************

# unique_order_id = normalorder.create_normal_order("NORMAL",trading_symbol,symbol_token,"BUY","NSE","LIMIT","DELIVERY","DAY","470.50","0","0","1")
# print(unique_order_id)
# normalorder.modify_normal_order("NORMAL","201020000000080","LIMIT","INTRADAY","DAY","194.00","1")

# normalorder.cancel_normal_order("NORMAL","201020000000080")

# normalorder.get_normal_orderbook()

# normalorder.get_normal_tradebook()

# normalorder.get_ltp_data("NSE","SBIN-EQ","3045")

# normalorder.get_normal_individualorder(unique_order_id)


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

