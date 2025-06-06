# Volume backtesting code with brokerage Calculator for short timeframes like 5 or 15 minutes

import pandas as pd
import numpy as np
import math
import csv

import math
import pandas as pd

import pandas as pd

# def to_invest(historical_data):
#     if len(historical_data) < 30:
#         return False

#     today = historical_data.iloc[-1]
#     previous = historical_data.iloc[-2]

#     dema_3 = historical_data['DEMA_3']
#     dema_5 = historical_data['DEMA_5']
#     dema_7 = historical_data['DEMA_7']
#     rsi = historical_data['RSI']

#     score = 0

#     # 1. Strong Trend
#     if dema_3.iloc[-1] > dema_5.iloc[-1] > dema_7.iloc[-1]:
#         score += 1

#     # 2. Strong Volume
#     avg_volume = historical_data['Volume'].iloc[-21:-1].mean()
#     if today['Volume'] > 1.2 * avg_volume:
#         score += 1

#     # 3. Bullish Marubozu-like candle
#     body_size = abs(today['Close'] - today['Open'])
#     candle_size = today['High'] - today['Low']
#     if today['Close'] > today['Open'] and body_size > 0.6 * candle_size:
#         score += 1

#     # 4. Strong RSI
#     if rsi.iloc[-1] > 60:
#         score += 1

#     # 5. Breakout of consolidation
#     recent_high = historical_data['High'].iloc[-21:-1].max()
#     if today['High'] > recent_high:
#         score += 1

#     # 6. Small upper wick
#     upper_wick = today['High'] - today['Close']
#     if body_size > 0 and upper_wick <= 0.3 * body_size:
#         score += 1

#     # 7. Positive momentum: today's close > 5 bars ago close
#     if today['Close'] > historical_data['Close'].iloc[-6]:
#         score += 1

#     # Final decision
#     return score >= 5

def calculate_dema(data, period):
    ema = data['Close'].ewm(span=period, adjust=False).mean()
    dema = 2 * ema - ema.ewm(span=period, adjust=False).mean()
    return dema

def calculate_rsi(data, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given dataset.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing at least the 'Close' prices.
    period (int): The period over which to calculate the RSI, default is 14.
    
    Returns:
    pd.Series: A series containing the RSI values.
    """
    # Calculate the price changes
    delta = data['Close'].diff()

    # Calculate gains and losses
    gain = delta.where(delta > 0, 0)  # Gains are positive changes
    loss = -delta.where(delta < 0, 0)  # Losses are negative changes

    # Calculate the average gains and average losses over the period
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Calculate the relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate RSI using the RS
    rsi = 100 - (100 / (1 + rs))

    return rsi

def calculate_total_charges(buy_price, buy_quantity, sell_price, sell_quantity):
    # Charge rates and fees
    stt_rate_buy = 0.001  # 0.1% STT on buy
    stt_rate_sell = 0.001  # 0.1% STT on sell
    transaction_charge_rate = 0.0000335  # 0.00335%
    dp_charge_per_scrip = 20  # DP charges
    dp_gst_rate = 0.18  # GST on DP charges
    stamp_duty_rate = 0.000076  # 0.015%
    sebi_turnover_fee_rate = 0.000001  # 0.0001%
    gst_rate = 0.18  # GST on brokerage and transaction charges

    if buy_quantity != sell_quantity:
        raise ValueError("Buy and Sell quantities do not match.")
    
    buy_value = buy_price * buy_quantity
    sell_value = sell_price * sell_quantity
    
    # STT calculation
    stt = buy_value * stt_rate_buy + sell_value * stt_rate_sell
    
    # Transaction charges
    transaction_charges = (buy_value + sell_value) * transaction_charge_rate
    
    # DP charges on sell side only
    dp_charges = dp_charge_per_scrip
    dp_charges_gst = dp_charges * dp_gst_rate
    
    # Stamp duty
    stamp_duty = buy_value * stamp_duty_rate + sell_value * stamp_duty_rate
    
    # SEBI turnover fees
    sebi_turnover_fees = (buy_value + sell_value) * sebi_turnover_fee_rate
    
    # GST on transaction charges and DP charges
    gst = (transaction_charges + dp_charges + sebi_turnover_fees) * gst_rate
    
    # Total charges
    total_charges = stt + transaction_charges + dp_charges + dp_charges_gst + stamp_duty + sebi_turnover_fees + gst
    
    return total_charges

def backtest_trading_strategy(data_list, initial_capital, max_holding_period, start_date, end_date):
    positions = []
    capital = initial_capital
    profit = 0
    invested = False
    invested_company = None
    buy_time = None
    sl = None
    target = None
    direction = None  # 'Buy' or 'Sell'

    trades = 0
    wins = 0
    losses = 0
    max_profit = -float('inf')
    max_loss = float('inf')
    peak_capital = capital
    max_drawdown = 0

    print("=== Starting Backtest ===")
    print(f"Initial Capital: {capital}\n")

    for data in data_list:
        data['DEMA_3'] = calculate_dema(data, 3)
        data['DEMA_5'] = calculate_dema(data, 5)
        data['DEMA_7'] = calculate_dema(data, 7)
        data['RSI'] = calculate_rsi(data)

    all_times = sorted(set(time for data in data_list for time in data.index))
    all_times = [t for t in all_times if start_date <= t <= end_date]

    current_index = 0
    day_high_low = {}

    while current_index < len(all_times):
        current_time = all_times[current_index]
        print(f"\nCurrent Time: {current_time}")

        if not invested:
            for company_index, data in enumerate(data_list):
                if current_time not in data.index:
                    continue

                today = data.loc[current_time]
                today_date = current_time.date()

                if current_time.time() == pd.Timestamp('09:30').time():
                    morning_data = data.between_time('09:15', '09:30')
                    if not morning_data.empty:
                        high = morning_data['High'].max()
                        low = morning_data['Low'].min()
                        day_high_low[(today_date, company_index)] = (high, low)
                        print(f"Marked 9:15-9:30 High/Low for {company_index} | High: {high}, Low: {low}")

                if current_time.time() == pd.Timestamp('09:45').time() and (today_date, company_index) in day_high_low:
                    high, low = day_high_low[(today_date, company_index)]

                    prev_volume = data.loc[:current_time].iloc[-2]['Volume'] if len(data.loc[:current_time]) >= 2 else 1
                    volume_ratio = today['Volume'] / prev_volume if prev_volume != 0 else 0

                    print(f"Checking Breakout for {company_index} | Close: {today['Close']}, Volume Ratio: {volume_ratio:.2f}")

                    if today['Close'] > high and volume_ratio > 1.0:
                        print(f"** BUY Signal ** at {today['Close']} for {company_index}")
                        buy_price = today['Close']
                        leverage = 5
                        max_shares = math.floor((capital * leverage) / buy_price)

                        if max_shares > 0:
                            buy_amount = max_shares * buy_price
                            positions.append(('Buy', current_time.strftime('%Y-%m-%d %H:%M'), buy_price, max_shares, capital, company_index))
                            capital -= buy_amount
                            invested = True
                            invested_company = company_index
                            buy_time = current_time

                            sl = today['Low']
                            target = buy_price + 2 * (buy_price - sl)
                            direction = 'Buy'
                            print(f"BUY Entry | Price: {buy_price}, SL: {sl}, Target: {target}, Shares: {max_shares}")
                            break

                    elif today['Close'] < low and volume_ratio > 1.2:
                        print(f"** SELL Signal ** at {today['Close']} for {company_index}")
                        sell_price = today['Close']
                        leverage = 5
                        max_shares = math.floor((capital * leverage) / sell_price)

                        if max_shares > 0:
                            sell_amount = max_shares * sell_price
                            positions.append(('Sell', current_time.strftime('%Y-%m-%d %H:%M'), sell_price, max_shares, capital, company_index))
                            capital -= sell_amount
                            invested = True
                            invested_company = company_index
                            buy_time = current_time

                            sl = today['High']
                            target = sell_price - 2 * (sl - sell_price)
                            direction = 'Sell'
                            print(f"SELL Entry | Price: {sell_price}, SL: {sl}, Target: {target}, Shares: {max_shares}")
                            break

        else:
            data = data_list[invested_company]

            holding_period = 0
            while holding_period < max_holding_period and (current_index + holding_period) < len(all_times):
                check_time = all_times[current_index + holding_period]
                if check_time not in data.index:
                    holding_period += 1
                    continue

                candle = data.loc[check_time]

                if check_time.date() != buy_time.date():
                    sell_price = candle['Close']
                    sell_reason = "End of Day"
                    print(f"Exiting {direction} due to End of Day | Sell Price: {sell_price}")
                    break

                if direction == 'Buy':
                    if candle['High'] >= target:
                        sell_price = target
                        sell_reason = "Target Hit"
                        print(f"Target Hit for BUY | Sell Price: {sell_price}")
                        break
                    if candle['Low'] <= sl:
                        sell_price = sl
                        sell_reason = "Stoploss Hit"
                        print(f"Stoploss Hit for BUY | Sell Price: {sell_price}")
                        break

                elif direction == 'Sell':
                    if candle['Low'] <= target:
                        sell_price = target
                        sell_reason = "Target Hit"
                        print(f"Target Hit for SELL | Sell Price: {sell_price}")
                        break
                    if candle['High'] >= sl:
                        sell_price = sl
                        sell_reason = "Stoploss Hit"
                        print(f"Stoploss Hit for SELL | Sell Price: {sell_price}")
                        break

                holding_period += 1
            else:
                sell_price = data.loc[all_times[min(current_index + holding_period - 1, len(all_times)-1)]]['Close']
                sell_reason = "Max Holding Reached"
                print(f"Max Holding Period Exit | Sell Price: {sell_price}")

            # Execute Sell/Buy to Cover
            shares = positions[-1][3]
            sell_amount = sell_price * shares
            total_charges = calculate_total_charges(positions[-1][2], shares, sell_price, shares)
            net_sell = sell_amount - total_charges

            if direction == 'Buy':
                trade_profit = net_sell - (positions[-1][2] * shares)
                profit += trade_profit
            else:
                trade_profit = (positions[-1][2] * shares) - net_sell
                profit += trade_profit

            capital += net_sell

            sell_time = all_times[current_index + holding_period - 1] if (current_index + holding_period - 1) < len(all_times) else current_time
            positions.append(('Sell' if direction == 'Buy' else 'Buy to Cover', sell_time.strftime('%Y-%m-%d %H:%M'), sell_price, shares, capital, invested_company))

            print(f"Closed {direction} Trade | Reason: {sell_reason} | Profit: {trade_profit:.2f} | New Capital: {capital:.2f}")

            invested = False
            invested_company = None

            trades += 1
            if trade_profit > 0:
                wins += 1
            else:
                losses += 1
            max_profit = max(max_profit, trade_profit)
            max_loss = min(max_loss, trade_profit)

            peak_capital = max(peak_capital, capital)
            drawdown = (peak_capital - capital) / peak_capital * 100
            max_drawdown = max(max_drawdown, drawdown)

            current_index += holding_period
            continue

        current_index += 1

    final_profit_percentage = ((capital - initial_capital) / initial_capital) * 100
    accuracy = (wins / trades) * 100 if trades > 0 else 0

    print("\n=== Backtest Summary ===")
    print(f"Final Capital: {capital:.2f}")
    print(f"Profit %: {final_profit_percentage:.2f}%")
    print(f"Trades: {trades} | Wins: {wins} | Losses: {losses}")
    print(f"Max Profit per Trade: {max_profit:.2f}")
    print(f"Max Loss per Trade: {max_loss:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Max Drawdown: {max_drawdown:.2f}%")

    return positions, capital, final_profit_percentage, max_profit, max_loss, accuracy, max_drawdown

# Load historical stock data for multiple companies from CSV files
file_paths = [
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ADANIENT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #0
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ADANIPORTS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #1
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\APOLLOHOSP-EQ_FIFTEEN_MINUTE_candle_data.csv",  #2
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ASIANPAINT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #3
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\AXISBANK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #4
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BAJAJ-AUTO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #5
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BAJFINANCE-EQ_FIFTEEN_MINUTE_candle_data.csv",  #6
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BAJAJFINSV-EQ_FIFTEEN_MINUTE_candle_data.csv",  #7
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BPCL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #8
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BHARTIARTL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #9
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BRITANNIA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #10
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\CIPLA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #11
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\COALINDIA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #12
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\DIVISLAB-EQ_FIFTEEN_MINUTE_candle_data.csv",  #13
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\DRREDDY-EQ_FIFTEEN_MINUTE_candle_data.csv",  #14
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\EICHERMOT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #15
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\GRASIM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #16
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HCLTECH-EQ_FIFTEEN_MINUTE_candle_data.csv",  #17
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HDFCBANK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #18
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HDFCLIFE-EQ_FIFTEEN_MINUTE_candle_data.csv",  #19
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HEROMOTOCO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #20
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HINDALCO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #21
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HINDUNILVR-EQ_FIFTEEN_MINUTE_candle_data.csv",  #22
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ICICIBANK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #23
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ITC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #24
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\INDUSINDBK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #25
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\INFY-EQ_FIFTEEN_MINUTE_candle_data.csv",  #26
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\JSWSTEEL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #27
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\KOTAKBANK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #28
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\LTIM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #29
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\LT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #30
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\M&M-EQ_FIFTEEN_MINUTE_candle_data.csv",  #31
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\MARUTI-EQ_FIFTEEN_MINUTE_candle_data.csv",  #32
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\NTPC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #33
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\NESTLEIND-EQ_FIFTEEN_MINUTE_candle_data.csv",  #34
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ONGC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #35
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\POWERGRID-EQ_FIFTEEN_MINUTE_candle_data.csv",  #36
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\RELIANCE-EQ_FIFTEEN_MINUTE_candle_data.csv",  #37
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SBILIFE-EQ_FIFTEEN_MINUTE_candle_data.csv",  #38
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SHRIRAMFIN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #39
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SBIN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #40
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SUNPHARMA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #41
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TCS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #42
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TATACONSUM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #43
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TATAMOTORS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #44
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TATASTEEL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #45
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TECHM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #46
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TITAN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #47
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ULTRACEMCO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #48
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\WIPRO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #49

    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ABB-EQ_FIFTEEN_MINUTE_candle_data.csv",  #50
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ADANIENSOL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #51
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ADANIGREEN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #52
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ADANIPOWER-EQ_FIFTEEN_MINUTE_candle_data.csv",  #53
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ATGL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #54
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\AMBUJACEM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #55
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\DMART-EQ_FIFTEEN_MINUTE_candle_data.csv",  #56
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BAJAJHLDNG-EQ_FIFTEEN_MINUTE_candle_data.csv",  #57
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BANKBARODA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #58
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BERGEPAINT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #59
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BEL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #60
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BOSCHLTD-EQ_FIFTEEN_MINUTE_candle_data.csv",  #61
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\CANBK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #62
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\CHOLAFIN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #63
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\COLPAL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #64
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\DLF-EQ_FIFTEEN_MINUTE_candle_data.csv",  #65
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\DABUR-EQ_FIFTEEN_MINUTE_candle_data.csv",  #66
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\GAIL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #67
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\GODREJCP-EQ_FIFTEEN_MINUTE_candle_data.csv",  #68
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HAVELLS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #69
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HAL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #70
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ICICIGI-EQ_FIFTEEN_MINUTE_candle_data.csv",  #71
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ICICIPRULI-EQ_FIFTEEN_MINUTE_candle_data.csv",  #72
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\IOC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #73
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\IRCTC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #74
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\IRFC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #75
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\NAUKRI-EQ_FIFTEEN_MINUTE_candle_data.csv",  #76
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\INDIGO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #77
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\JINDALSTEL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #78
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\JIOFIN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #79
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\LICI-EQ_FIFTEEN_MINUTE_candle_data.csv",  #80
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\MARICO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #81
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\PIDILITIND-EQ_FIFTEEN_MINUTE_candle_data.csv",  #82
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\PFC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #83
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\PNB-EQ_FIFTEEN_MINUTE_candle_data.csv",  #84
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\RECLTD-EQ_FIFTEEN_MINUTE_candle_data.csv",  #85
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SBICARD-EQ_FIFTEEN_MINUTE_candle_data.csv",  #86
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SRF-EQ_FIFTEEN_MINUTE_candle_data.csv",  #87
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\MOTHERSON-EQ_FIFTEEN_MINUTE_candle_data.csv",  #88
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SHREECEM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #89
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SIEMENS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #90
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TVSMOTOR-EQ_FIFTEEN_MINUTE_candle_data.csv",  #91
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TATAMTRDVR-EQ_FIFTEEN_MINUTE_candle_data.csv",  #92
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TATAPOWER-EQ_FIFTEEN_MINUTE_candle_data.csv",  #93
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TORNTPHARM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #94
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TRENT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #95
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\VBL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #96
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\VEDL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #97
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ZOMATO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #98
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ZYDUSLIFE-EQ_FIFTEEN_MINUTE_candle_data.csv",  #99

    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ACC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #100
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\AUBANK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #101
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ABCAPITAL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #102
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ALKEM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #103
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ASHOKLEY-EQ_FIFTEEN_MINUTE_candle_data.csv",  #104
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ASTRAL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #105
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\AUROPHARMA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #106
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BALKRISIND-EQ_FIFTEEN_MINUTE_candle_data.csv",  #107
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BANDHANBNK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #108
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BHARATFORG-EQ_FIFTEEN_MINUTE_candle_data.csv",  #109
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\BHEL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #110
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\COFORGE-EQ_FIFTEEN_MINUTE_candle_data.csv",  #111
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\CONCOR-EQ_FIFTEEN_MINUTE_candle_data.csv",  #112
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\CUMMINSIND-EQ_FIFTEEN_MINUTE_candle_data.csv",  #113
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\DALBHARAT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #114
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\DIXON-EQ_FIFTEEN_MINUTE_candle_data.csv",  #115
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\ESCORTS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #116
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\FEDERALBNK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #117
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\GMRINFRA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #118
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\GODREJPROP-EQ_FIFTEEN_MINUTE_candle_data.csv",  #119
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\GUJGASLTD-EQ_FIFTEEN_MINUTE_candle_data.csv",  #120
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HDFCAMC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #121
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\HINDPETRO-EQ_FIFTEEN_MINUTE_candle_data.csv",  #122
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\IDFCFIRSTB-EQ_FIFTEEN_MINUTE_candle_data.csv",  #123
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\INDHOTEL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #124
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\INDUSTOWER-EQ_FIFTEEN_MINUTE_candle_data.csv",  #125
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\JUBLFOOD-EQ_FIFTEEN_MINUTE_candle_data.csv",  #126
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\LTF-EQ_FIFTEEN_MINUTE_candle_data.csv",  #127
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\LTTS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #128
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\LUPIN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #129
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\MRF-EQ_FIFTEEN_MINUTE_candle_data.csv",  #130
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\M&MFIN-EQ_FIFTEEN_MINUTE_candle_data.csv",  #131
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\MFSL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #132
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\MAXHEALTH-EQ_FIFTEEN_MINUTE_candle_data.csv",  #133
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\MPHASIS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #134
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\NMDC-EQ_FIFTEEN_MINUTE_candle_data.csv",  #135
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\OBEROIRLTY-EQ_FIFTEEN_MINUTE_candle_data.csv",  #136
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\OFSS-EQ_FIFTEEN_MINUTE_candle_data.csv",  #137
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\PIIND-EQ_FIFTEEN_MINUTE_candle_data.csv",  #138
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\PAGEIND-EQ_FIFTEEN_MINUTE_candle_data.csv",  #139
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\PERSISTENT-EQ_FIFTEEN_MINUTE_candle_data.csv",  #140
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\PETRONET-EQ_FIFTEEN_MINUTE_candle_data.csv",  #141
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\POLYCAB-EQ_FIFTEEN_MINUTE_candle_data.csv",  #142
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SAIL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #143
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\SUZLON-EQ_FIFTEEN_MINUTE_candle_data.csv",  #144
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TATACOMM-EQ_FIFTEEN_MINUTE_candle_data.csv",  #145
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\TIINDIA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #146
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\UPL-EQ_FIFTEEN_MINUTE_candle_data.csv",  #147
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\IDEA-EQ_FIFTEEN_MINUTE_candle_data.csv",  #148
    r"C:\Documents\GitHub\AngelOne\historical files\FIFTEEN_MINUTE\YESBANK-EQ_FIFTEEN_MINUTE_candle_data.csv",  #149
]

# Load data into a list of DataFrames
data_list = [pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp') for file_path in file_paths]

start_date = pd.Timestamp('2025-01-01 09:15:00', tz='Asia/Kolkata')
end_date = pd.Timestamp('2025-02-01 15:30:00', tz='Asia/Kolkata')

# Run the backtest
positions, final_capital, final_profit_percentage, max_profit, max_loss, accuracy, max_drawdown = backtest_trading_strategy(
    data_list=data_list,
    initial_capital=10000,
    max_holding_period=10,
    start_date=start_date,
    end_date=end_date
)

# Output the results
print("Positions:")
for position in positions:
    print(f"{position},")

print("\nFinal Capital:", final_capital)
print("Final Profit Percentage:", final_profit_percentage)
print("Max Profit from a Trade:", max_profit)
print("Max Loss from a Trade:", max_loss)
print("Accuracy of Trades:", accuracy)
print("Max Drawdown:", max_drawdown)

# Save positions and summary to a CSV file
df_positions = pd.DataFrame(positions, columns=['Action', 'Date', 'Price', 'Quantity', 'Capital', 'Company Index'])
df_positions.to_csv('backtest_results1.csv', index=False, mode='w')

# Append final metrics to the CSV file
with open('backtest_results6.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([])
    writer.writerow(['Final Capital:', final_capital])
    writer.writerow(['Final Profit Percentage:', final_profit_percentage])
    writer.writerow(['Maximum Profit:', max_profit])
    writer.writerow(['Maximum Loss:', max_loss])
    writer.writerow(['Accuracy:', accuracy])
    writer.writerow(['Maximum Drawdown:', max_drawdown])

print("Backtest results saved to backtest_results.csv")
