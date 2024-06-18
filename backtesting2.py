# Buy Condition

# Buy Signal:
# Buy a stock if:
# Not currently invested.
# VolumeRatio is at least 3.
# CloseChange is at least 4%.
# Current day's high is greater than the previous day's high.
# DEMA_5 > DEMA_8 > DEMA_13.
# Current day's close is greater than the open.
# Calculate the maximum number of shares that can be bought with the available capital.
# Update the positions list with the buy transaction.
# Deduct the invested amount from capital.
# Set invested to True and record the invested company and buy date.


# Sell Condition

# Sell Signal:
# If currently invested, check the holding period and sell conditions.
# Iterate through future dates up to the maximum holding period.
# Sell if:
# Next day's open price is at least 3% higher than the buy price (intraday sell).
# Closing price is at least 4% higher than the buy price (normal sell).
# End of the maximum holding period is reached.
# Calculate profit from the sell transaction.
# Update the positions list with the sell transaction.
# Add the sale proceeds back to capital.
# Set invested to False and reset invested_company.


import pandas as pd
import math

def backtest_trading_strategy(data_list, initial_capital, max_holding_period=40):
    # Initialize variables to track trades and performance
    positions = []
    capital = initial_capital  # Use the full initial capital for trading
    profit = 0
    invested = False  # Flag to track if the capital is currently invested
    invested_company = None  # Track which company is currently invested
    start = '2024-01-01T00:00:00+05:30'
    end = '2024-12-31T00:00:00+05:30'

    # Iterate through each day's data for each company
    current_start_date = pd.Timestamp(start)
    while current_start_date <= pd.Timestamp(end):
        sell_occurred = False
        for company_index, data in enumerate(data_list):
            if current_start_date not in data.index:
                continue

            today = data.loc[current_start_date]
            previous_date = current_start_date - pd.Timedelta(days=1)
            previous = data.loc[previous_date] if previous_date in data.index else None

            if previous is None:
                continue

            # Calculate indicators for today
            data.loc[current_start_date, 'VolumeRatio'] = today['Volume'] / previous['Volume'] if previous['Volume'] != 0 else 0
            data.loc[current_start_date, 'CloseChange'] = (today['Close'] - previous['Close']) / previous['Close'] * 100
            data.loc[current_start_date, 'DEMA_5'] = data['Close'].ewm(span=5).mean().loc[current_start_date]
            data.loc[current_start_date, 'DEMA_8'] = data['Close'].ewm(span=8).mean().loc[current_start_date]
            data.loc[current_start_date, 'DEMA_13'] = data['Close'].ewm(span=13).mean().loc[current_start_date]

            # Buy condition
            if not invested and \
               data.loc[current_start_date, 'VolumeRatio'] >= 3 and \
               data.loc[current_start_date, 'CloseChange'] >= 4 and \
               today['High'] > previous['High'] and \
               data.loc[current_start_date, 'DEMA_5'] > data.loc[current_start_date, 'DEMA_8'] > data.loc[current_start_date, 'DEMA_13'] and \
               today['Close'] > today['Open']:
                
                max_shares = math.floor(capital / today['Close'])
                
                if max_shares > 0:
                    buy_amount = max_shares * today['Close']
                    positions.append(('Buy', today.name.strftime('%Y-%m-%d'), today['Close'], max_shares, capital, company_index))
                    capital -= buy_amount
                    invested = True
                    invested_company = company_index
                    buy_date = current_start_date

            # Sell condition
            if invested and invested_company == company_index:
                for future_date in pd.date_range(start=current_start_date + pd.Timedelta(days=1), end=current_start_date + pd.Timedelta(days=max_holding_period), freq='B'):
                    if future_date in data.index:
                        sell_candidate = data.loc[future_date]
                        next_day_open = sell_candidate['Open']

                        if next_day_open >= (positions[-1][2] * 1.03):
                            # Intraday sell for at least 3% profit
                            intraday_sell_price = next_day_open
                            sell_amount = intraday_sell_price * positions[-1][3]
                            profit += (sell_amount - positions[-1][2] * positions[-1][3])
                            capital += sell_amount
                            positions.append(('Sell (Intraday)', sell_candidate.name.strftime('%Y-%m-%d'), intraday_sell_price, positions[-1][3]))
                            invested = False
                            invested_company = None
                            sell_occurred = True
                            break
                        elif sell_candidate['Close'] >= (positions[-1][2] * 1.04):
                            # Normal sell at least 4% higher
                            sell_price = sell_candidate['Close']
                            sell_amount = sell_price * positions[-1][3]
                            profit += (sell_amount - positions[-1][2] * positions[-1][3])
                            capital += sell_amount
                            positions.append(('Sell', sell_candidate.name.strftime('%Y-%m-%d'), sell_price, positions[-1][3]))
                            invested = False
                            invested_company = None
                            sell_occurred = True
                            break
                        elif future_date == buy_date + pd.Timedelta(days=max_holding_period):
                            # Sell at the end of the maximum holding period
                            sell_price = sell_candidate['Close']
                            sell_amount = sell_price * positions[-1][3]
                            profit += (sell_amount - positions[-1][2] * positions[-1][3])
                            capital += sell_amount
                            positions.append(('Sell (Max Holding Period)', sell_candidate.name.strftime('%Y-%m-%d'), sell_price, positions[-1][3]))
                            invested = False
                            invested_company = None
                            sell_occurred = True
                            break

            if sell_occurred:
                current_start_date = sell_candidate.name
                break
        current_start_date += pd.Timedelta(days=1)

    # Calculate final profit percentage
    final_profit_percentage = ((capital - initial_capital) / initial_capital) * 100

    return positions, capital, final_profit_percentage

# Load historical stock data for multiple companies from CSV files
file_paths = [
    # r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\ADANIENT-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\ADANIPORTS-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\APOLLOHOSP-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\ASIANPAINT-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\AXISBANK-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\BAJAJ-AUTO-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\BAJFINANCE-EQ_ONE_DAY_candle_data.csv",
    # r"C:\Documents\GitHub\AngelOne\historical files\BAJAJFINSV-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\BHARTIARTL-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\BPCL-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\BRITANNIA-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\CIPLA-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\COALINDIA-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\DIVISLAB-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\DRREDDY-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\EICHERMOT-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\GRASIM-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\HCLTECH-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\HDFCBANK-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\HDFCLIFE-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\HEROMOTOCO-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\HINDALCO-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\HINDUNILVR-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\ICICIBANK-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\INDUSINDBK-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\INFY-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\ITC-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\JSWSTEEL-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\KOTAKBANK-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\LT-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\M&M-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\MARUTI-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\NESTLEIND-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\NTPC-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\ONGC-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\POWERGRID-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\RELIANCE-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\SBILIFE-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\SBIN-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\SUNPHARMA-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\TATACONSUM-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\TATAMOTORS-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\TATASTEEL-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\TCS-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\TECHM-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\TITAN-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\ULTRACEMCO-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\UPL-EQ_ONE_DAY_candle_data.csv",
    r"C:\Documents\GitHub\AngelOne\historical files\WIPRO-EQ_ONE_DAY_candle_data.csv"
]

# Load data into a list of DataFrames
data_list = [pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp') for file_path in file_paths]

# Run the backtest
positions, final_capital, final_profit_percentage = backtest_trading_strategy(data_list, initial_capital=500000)

# Output the results
print("Positions:")
for position in positions:
    print(position)
print("Final Capital:", final_capital)
print("Final Profit Percentage:", final_profit_percentage)
