# Volume backtesting code with brokerage Calculator 

import pandas as pd
import numpy as np
import math
import csv

def calculate_dema(data, period):
    ema = data['Close'].ewm(span=period, adjust=False).mean()
    dema = 2 * ema - ema.ewm(span=period, adjust=False).mean()
    return dema

def calculate_total_charges(buy_price, buy_quantity, sell_price, sell_quantity):
    # Charge rates
    stt_rate_buy = 0.001  # 0.1% STT on buy
    stt_rate_sell = 0.001  # 0.1% STT on sell
    transaction_charge_rate = 0.0000335  # 0.00335%
    dp_charge_per_scrip = 20  # DP charges
    dp_gst_rate = 0.18  # GST on DP charges
    stamp_duty_rate = 0.000076  # 0.015%
    sebi_turnover_fee_rate = 0.000001  # 0.0001%
    gst_rate = 0.18  # GST on brokerage and transaction charges

    # Ensure the quantities match for buy and sell transactions
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

def backtest_trading_strategy(data_list, initial_capital, max_holding_period):
    positions = []
    capital = initial_capital
    profit = 0
    invested = False
    invested_company = None
    buy_date = None
    start = '2024-01-01T00:00:00+05:30'
    end = '2025-12-31T00:00:00+05:30'

    current_start_date = pd.Timestamp(start)
    end_date = pd.Timestamp(end)
    
    # Generate a range of business days within the start and end dates
    business_days = pd.bdate_range(start=current_start_date, end=end_date)
    
    trades = 0
    wins = 0
    losses = 0
    max_profit = -float('inf')
    max_loss = float('inf')
    peak_capital = capital
    drawdown = 0
    max_drawdown = 0

    while current_start_date <= end_date:
        if current_start_date not in business_days:
            current_start_date += pd.Timedelta(days=1)
            continue

        sell_occurred = False

        for company_index, data in enumerate(data_list):
            if current_start_date not in data.index:
                continue

            today = data.loc[current_start_date]
            previous_date = current_start_date - pd.Timedelta(days=1)
            previous = data.loc[previous_date] if previous_date in data.index else None

            if previous is None:
                continue

            data.loc[current_start_date, 'VolumeRatio'] = today['Volume'] / previous['Volume'] if previous['Volume'] != 0 else 0
            data.loc[current_start_date, 'CloseChange'] = (today['Close'] - previous['Close']) / previous['Close'] * 100
            data.loc[current_start_date, 'DEMA_5'] = calculate_dema(data, 5).loc[current_start_date]
            data.loc[current_start_date, 'DEMA_8'] = calculate_dema(data, 8).loc[current_start_date]
            data.loc[current_start_date, 'DEMA_13'] = calculate_dema(data, 13).loc[current_start_date]

            # Buy conditions
            if not invested and \
               data.loc[current_start_date, 'VolumeRatio'] >= 4 and \
               data.loc[current_start_date, 'CloseChange'] >= 4 and \
               today['High'] > previous['High'] and \
               data.loc[current_start_date, 'DEMA_5'] > data.loc[current_start_date, 'DEMA_8'] > data.loc[current_start_date, 'DEMA_13'] and \
               today['Close'] > today['Open']:
                
                max_shares = math.floor(capital / today['Close'])
                max_shares -= 1
                
                if max_shares > 0:
                    buy_amount = max_shares * today['Close']
                    positions.append(('Buy', today.name.strftime('%Y-%m-%d'), today['Close'], max_shares, capital, company_index))
                    capital -= buy_amount
                    invested = True
                    invested_company = company_index
                    buy_date = current_start_date
                    # initial_sl = today['Close'] - (today['Close'] * 0.03) # Less Risky but less profitable
                    initial_sl = (today['Low'] - (today['Low'] * 0.03)) # Risky but profitable
                    sl = initial_sl
                    targetnotach = False  # Indicates if the 4% target is achieved

            # Sell conditions
            if invested and invested_company == company_index:
                future_dates = pd.bdate_range(start=current_start_date + pd.Timedelta(days=1), periods=max_holding_period)
                
                for future_date in future_dates:
                    if future_date in data.index:
                        sell_candidate = data.loc[future_date]

                        data.at[future_date, 'DEMA_5'] = calculate_dema(data, 5).loc[future_date]
                        data.at[future_date, 'DEMA_8'] = calculate_dema(data, 8).loc[future_date]
                        data.at[future_date, 'DEMA_13'] = calculate_dema(data, 13).loc[future_date]
                        
                        # Check if 4% target is achieved
                        if not targetnotach and sell_candidate['High'] >= (positions[-1][2] * 1.04):
                            if data.at[future_date, 'DEMA_5'] > data.at[future_date, 'DEMA_8'] > data.at[future_date, 'DEMA_13']:
                                sl = positions[-1][2] * 1.02  # Update stop-loss to 2% down from the 4% target
                                targetnotach = True
                            else:
                                sell_price = positions[-1][2] * 1.04
                                sell_amount = sell_price * positions[-1][3]
                                total_charges = calculate_total_charges(positions[-1][2], positions[-1][3], sell_price, positions[-1][3])
                                net_sell_amount = sell_amount - total_charges
                                profit += net_sell_amount - (positions[-1][2] * positions[-1][3])
                                capital += net_sell_amount
                                positions.append(('Sell', sell_candidate.name.strftime('%Y-%m-%d'), sell_price, positions[-1][3], capital, company_index))
                                invested = False
                                invested_company = None
                                sell_occurred = True
                                break

                        # Check updated stop-loss after 4% target is achieved
                        elif sell_candidate['Low'] <= sl:
                            sell_price = sl
                            sell_amount = sell_price * positions[-1][3]
                            total_charges = calculate_total_charges(positions[-1][2], positions[-1][3], sell_price, positions[-1][3])
                            net_sell_amount = sell_amount - total_charges
                            profit += (net_sell_amount - positions[-1][2] * positions[-1][3])
                            capital += net_sell_amount
                            positions.append(('Sell (Updated Stop Loss)', sell_candidate.name.strftime('%Y-%m-%d'), sell_price, positions[-1][3], capital, company_index))
                            invested = False
                            invested_company = None
                            sell_occurred = True
                            break

                        # Continue running the trade until DEMA_5 < DEMA_8
                        elif targetnotach and data.at[future_date, 'DEMA_5'] < data.at[future_date, 'DEMA_8']:
                            sell_price = sell_candidate['Close']
                            sell_amount = sell_price * positions[-1][3]
                            total_charges = calculate_total_charges(positions[-1][2], positions[-1][3], sell_price, positions[-1][3])
                            net_sell_amount = sell_amount - total_charges
                            profit += (net_sell_amount - positions[-1][2] * positions[-1][3])
                            capital += net_sell_amount
                            positions.append(('Sell (DEMA Condition)', sell_candidate.name.strftime('%Y-%m-%d'), sell_price, positions[-1][3], capital, company_index))
                            invested = False
                            invested_company = None
                            sell_occurred = True
                            break

                        # Check max holding period
                        elif future_date == future_dates[-1]:
                            sell_price = sell_candidate['Close']
                            sell_amount = sell_price * positions[-1][3]
                            total_charges = calculate_total_charges(positions[-1][2], positions[-1][3], sell_price, positions[-1][3])
                            net_sell_amount = sell_amount - total_charges
                            profit += (net_sell_amount - positions[-1][2] * positions[-1][3])
                            capital += net_sell_amount
                            positions.append(('Sell (Max Holding Period)', sell_candidate.name.strftime('%Y-%m-%d'), sell_price, positions[-1][3], capital, company_index))
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

    # Calculate additional performance metrics
    for action, date, price, quantity, cap, company_index in positions:
        if 'Sell' in action:
            trades += 1
            trade_profit = (price * quantity) - (positions[positions.index((action, date, price, quantity, cap, company_index)) - 1][2] * quantity)
            if trade_profit > 0:
                wins += 1
            else:
                losses += 1
            max_profit = max(max_profit, trade_profit)
            max_loss = min(max_loss, trade_profit)

            peak_capital = max(peak_capital, cap)
            drawdown = (peak_capital - cap) / peak_capital * 100
            max_drawdown = max(max_drawdown, drawdown)

    accuracy = (wins / trades) * 100 if trades > 0 else 0

    return positions, capital, final_profit_percentage, max_profit, max_loss, accuracy, max_drawdown

# Load historical stock data for multiple companies from CSV files
file_paths = [
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ADANIENT-EQ_ONE_DAY_candle_data.csv",  #0
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ADANIPORTS-EQ_ONE_DAY_candle_data.csv",  #1
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\APOLLOHOSP-EQ_ONE_DAY_candle_data.csv",  #2
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ASIANPAINT-EQ_ONE_DAY_candle_data.csv",  #3
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\AXISBANK-EQ_ONE_DAY_candle_data.csv",  #4
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BAJAJ-AUTO-EQ_ONE_DAY_candle_data.csv",  #5
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BAJFINANCE-EQ_ONE_DAY_candle_data.csv",  #6
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BAJAJFINSV-EQ_ONE_DAY_candle_data.csv",  #7
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BPCL-EQ_ONE_DAY_candle_data.csv",  #8
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BHARTIARTL-EQ_ONE_DAY_candle_data.csv",  #9
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BRITANNIA-EQ_ONE_DAY_candle_data.csv",  #10
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\CIPLA-EQ_ONE_DAY_candle_data.csv",  #11
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\COALINDIA-EQ_ONE_DAY_candle_data.csv",  #12
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\DIVISLAB-EQ_ONE_DAY_candle_data.csv",  #13
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\DRREDDY-EQ_ONE_DAY_candle_data.csv",  #14
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\EICHERMOT-EQ_ONE_DAY_candle_data.csv",  #15
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\GRASIM-EQ_ONE_DAY_candle_data.csv",  #16
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HCLTECH-EQ_ONE_DAY_candle_data.csv",  #17
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HDFCBANK-EQ_ONE_DAY_candle_data.csv",  #18
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HDFCLIFE-EQ_ONE_DAY_candle_data.csv",  #19
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HEROMOTOCO-EQ_ONE_DAY_candle_data.csv",  #20
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HINDALCO-EQ_ONE_DAY_candle_data.csv",  #21
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HINDUNILVR-EQ_ONE_DAY_candle_data.csv",  #22
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ICICIBANK-EQ_ONE_DAY_candle_data.csv",  #23
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ITC-EQ_ONE_DAY_candle_data.csv",  #24
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\INDUSINDBK-EQ_ONE_DAY_candle_data.csv",  #25
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\INFY-EQ_ONE_DAY_candle_data.csv",  #26
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\JSWSTEEL-EQ_ONE_DAY_candle_data.csv",  #27
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\KOTAKBANK-EQ_ONE_DAY_candle_data.csv",  #28
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\LTIM-EQ_ONE_DAY_candle_data.csv",  #29
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\LT-EQ_ONE_DAY_candle_data.csv",  #30
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\M&M-EQ_ONE_DAY_candle_data.csv",  #31
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\MARUTI-EQ_ONE_DAY_candle_data.csv",  #32
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\NTPC-EQ_ONE_DAY_candle_data.csv",  #33
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\NESTLEIND-EQ_ONE_DAY_candle_data.csv",  #34
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ONGC-EQ_ONE_DAY_candle_data.csv",  #35
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\POWERGRID-EQ_ONE_DAY_candle_data.csv",  #36
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\RELIANCE-EQ_ONE_DAY_candle_data.csv",  #37
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SBILIFE-EQ_ONE_DAY_candle_data.csv",  #38
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SHRIRAMFIN-EQ_ONE_DAY_candle_data.csv",  #39
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SBIN-EQ_ONE_DAY_candle_data.csv",  #40
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SUNPHARMA-EQ_ONE_DAY_candle_data.csv",  #41
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TCS-EQ_ONE_DAY_candle_data.csv",  #42
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TATACONSUM-EQ_ONE_DAY_candle_data.csv",  #43
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TATAMOTORS-EQ_ONE_DAY_candle_data.csv",  #44
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TATASTEEL-EQ_ONE_DAY_candle_data.csv",  #45
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TECHM-EQ_ONE_DAY_candle_data.csv",  #46
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TITAN-EQ_ONE_DAY_candle_data.csv",  #47
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ULTRACEMCO-EQ_ONE_DAY_candle_data.csv",  #48
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\WIPRO-EQ_ONE_DAY_candle_data.csv",  #49

    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ABB-EQ_ONE_DAY_candle_data.csv",  #50
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ADANIENSOL-EQ_ONE_DAY_candle_data.csv",  #51
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ADANIGREEN-EQ_ONE_DAY_candle_data.csv",  #52
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ADANIPOWER-EQ_ONE_DAY_candle_data.csv",  #53
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ATGL-EQ_ONE_DAY_candle_data.csv",  #54
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\AMBUJACEM-EQ_ONE_DAY_candle_data.csv",  #55
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\DMART-EQ_ONE_DAY_candle_data.csv",  #56
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BAJAJHLDNG-EQ_ONE_DAY_candle_data.csv",  #57
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BANKBARODA-EQ_ONE_DAY_candle_data.csv",  #58
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BERGEPAINT-EQ_ONE_DAY_candle_data.csv",  #59
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BEL-EQ_ONE_DAY_candle_data.csv",  #60
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BOSCHLTD-EQ_ONE_DAY_candle_data.csv",  #61
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\CANBK-EQ_ONE_DAY_candle_data.csv",  #62
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\CHOLAFIN-EQ_ONE_DAY_candle_data.csv",  #63
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\COLPAL-EQ_ONE_DAY_candle_data.csv",  #64
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\DLF-EQ_ONE_DAY_candle_data.csv",  #65
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\DABUR-EQ_ONE_DAY_candle_data.csv",  #66
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\GAIL-EQ_ONE_DAY_candle_data.csv",  #67
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\GODREJCP-EQ_ONE_DAY_candle_data.csv",  #68
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HAVELLS-EQ_ONE_DAY_candle_data.csv",  #69
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HAL-EQ_ONE_DAY_candle_data.csv",  #70
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ICICIGI-EQ_ONE_DAY_candle_data.csv",  #71
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ICICIPRULI-EQ_ONE_DAY_candle_data.csv",  #72
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\IOC-EQ_ONE_DAY_candle_data.csv",  #73
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\IRCTC-EQ_ONE_DAY_candle_data.csv",  #74
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\IRFC-EQ_ONE_DAY_candle_data.csv",  #75
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\NAUKRI-EQ_ONE_DAY_candle_data.csv",  #76
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\INDIGO-EQ_ONE_DAY_candle_data.csv",  #77
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\JINDALSTEL-EQ_ONE_DAY_candle_data.csv",  #78
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\JIOFIN-EQ_ONE_DAY_candle_data.csv",  #79
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\LICI-EQ_ONE_DAY_candle_data.csv",  #80
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\MARICO-EQ_ONE_DAY_candle_data.csv",  #81
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\PIDILITIND-EQ_ONE_DAY_candle_data.csv",  #82
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\PFC-EQ_ONE_DAY_candle_data.csv",  #83
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\PNB-EQ_ONE_DAY_candle_data.csv",  #84
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\RECLTD-EQ_ONE_DAY_candle_data.csv",  #85
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SBICARD-EQ_ONE_DAY_candle_data.csv",  #86
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SRF-EQ_ONE_DAY_candle_data.csv",  #87
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\MOTHERSON-EQ_ONE_DAY_candle_data.csv",  #88
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SHREECEM-EQ_ONE_DAY_candle_data.csv",  #89
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SIEMENS-EQ_ONE_DAY_candle_data.csv",  #90
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TVSMOTOR-EQ_ONE_DAY_candle_data.csv",  #91
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TATAMTRDVR-EQ_ONE_DAY_candle_data.csv",  #92
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TATAPOWER-EQ_ONE_DAY_candle_data.csv",  #93
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TORNTPHARM-EQ_ONE_DAY_candle_data.csv",  #94
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TRENT-EQ_ONE_DAY_candle_data.csv",  #95
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\VBL-EQ_ONE_DAY_candle_data.csv",  #96
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\VEDL-EQ_ONE_DAY_candle_data.csv",  #97
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ZOMATO-EQ_ONE_DAY_candle_data.csv",  #98
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ZYDUSLIFE-EQ_ONE_DAY_candle_data.csv",  #99

    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ACC-EQ_ONE_DAY_candle_data.csv",  #100
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\AUBANK-EQ_ONE_DAY_candle_data.csv",  #101
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ABCAPITAL-EQ_ONE_DAY_candle_data.csv",  #102
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ALKEM-EQ_ONE_DAY_candle_data.csv",  #103
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ASHOKLEY-EQ_ONE_DAY_candle_data.csv",  #104
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ASTRAL-EQ_ONE_DAY_candle_data.csv",  #105
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\AUROPHARMA-EQ_ONE_DAY_candle_data.csv",  #106
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BALKRISIND-EQ_ONE_DAY_candle_data.csv",  #107
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BANDHANBNK-EQ_ONE_DAY_candle_data.csv",  #108
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BHARATFORG-EQ_ONE_DAY_candle_data.csv",  #109
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\BHEL-EQ_ONE_DAY_candle_data.csv",  #110
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\COFORGE-EQ_ONE_DAY_candle_data.csv",  #111
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\CONCOR-EQ_ONE_DAY_candle_data.csv",  #112
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\CUMMINSIND-EQ_ONE_DAY_candle_data.csv",  #113
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\DALBHARAT-EQ_ONE_DAY_candle_data.csv",  #114
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\DIXON-EQ_ONE_DAY_candle_data.csv",  #115
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\ESCORTS-EQ_ONE_DAY_candle_data.csv",  #116
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\FEDERALBNK-EQ_ONE_DAY_candle_data.csv",  #117
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\GMRINFRA-EQ_ONE_DAY_candle_data.csv",  #118
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\GODREJPROP-EQ_ONE_DAY_candle_data.csv",  #119
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\GUJGASLTD-EQ_ONE_DAY_candle_data.csv",  #120
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HDFCAMC-EQ_ONE_DAY_candle_data.csv",  #121
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\HINDPETRO-EQ_ONE_DAY_candle_data.csv",  #122
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\IDFCFIRSTB-EQ_ONE_DAY_candle_data.csv",  #123
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\INDHOTEL-EQ_ONE_DAY_candle_data.csv",  #124
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\INDUSTOWER-EQ_ONE_DAY_candle_data.csv",  #125
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\JUBLFOOD-EQ_ONE_DAY_candle_data.csv",  #126
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\LTF-EQ_ONE_DAY_candle_data.csv",  #127
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\LTTS-EQ_ONE_DAY_candle_data.csv",  #128
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\LUPIN-EQ_ONE_DAY_candle_data.csv",  #129
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\MRF-EQ_ONE_DAY_candle_data.csv",  #130
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\M&MFIN-EQ_ONE_DAY_candle_data.csv",  #131
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\MFSL-EQ_ONE_DAY_candle_data.csv",  #132
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\MAXHEALTH-EQ_ONE_DAY_candle_data.csv",  #133
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\MPHASIS-EQ_ONE_DAY_candle_data.csv",  #134
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\NMDC-EQ_ONE_DAY_candle_data.csv",  #135
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\OBEROIRLTY-EQ_ONE_DAY_candle_data.csv",  #136
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\OFSS-EQ_ONE_DAY_candle_data.csv",  #137
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\PIIND-EQ_ONE_DAY_candle_data.csv",  #138
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\PAGEIND-EQ_ONE_DAY_candle_data.csv",  #139
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\PERSISTENT-EQ_ONE_DAY_candle_data.csv",  #140
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\PETRONET-EQ_ONE_DAY_candle_data.csv",  #141
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\POLYCAB-EQ_ONE_DAY_candle_data.csv",  #142
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SAIL-EQ_ONE_DAY_candle_data.csv",  #143
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\SUZLON-EQ_ONE_DAY_candle_data.csv",  #144
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TATACOMM-EQ_ONE_DAY_candle_data.csv",  #145
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\TIINDIA-EQ_ONE_DAY_candle_data.csv",  #146
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\UPL-EQ_ONE_DAY_candle_data.csv",  #147
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\IDEA-EQ_ONE_DAY_candle_data.csv",  #148
    r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\YESBANK-EQ_ONE_DAY_candle_data.csv",  #149
]

# Load data into a list of DataFrames
data_list = [pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp') for file_path in file_paths]

# Run the backtest
positions, final_capital, final_profit_percentage, max_profit, max_loss, accuracy, max_drawdown = backtest_trading_strategy(data_list, initial_capital=30000, max_holding_period=23)

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
with open('backtest_results1.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([])
    writer.writerow(['Final Capital:', final_capital])
    writer.writerow(['Final Profit Percentage:', final_profit_percentage])
    writer.writerow(['Maximum Profit:', max_profit])
    writer.writerow(['Maximum Loss:', max_loss])
    writer.writerow(['Accuracy:', accuracy])
    writer.writerow(['Maximum Drawdown:', max_drawdown])

print("Backtest results saved to backtest_results.csv")
