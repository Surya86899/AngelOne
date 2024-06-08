import pandas as pd
import math

def backtest_trading_strategy(data, initial_capital):
    # Calculate necessary indicators (volume, price changes, moving averages)
    data['VolumeRatio'] = data['Volume'] / data['Volume'].shift(1)
    data['CloseChange'] = data['Close'].pct_change() * 100
    data['DEMA_5'] = data['Close'].ewm(span=5, adjust=False).mean()
    data['DEMA_8'] = data['Close'].ewm(span=8, adjust=False).mean()
    data['DEMA_13'] = data['Close'].ewm(span=13, adjust=False).mean()

    # Initialize variables to track trades and performance
    positions = []
    capital = initial_capital  # Use the full initial capital for trading
    profit = 0

    # Iterate through each day's data to apply the trading strategy
    for i in range(1, len(data)):
        today = data.iloc[i]
        previous = data.iloc[i - 1]

        # Buy condition
        if (today['VolumeRatio'] >= 3 and
            today['CloseChange'] >= 4 and
            today['High'] > previous['High'] and
            today['DEMA_5'] > today['DEMA_8'] > today['DEMA_13'] and
            today['Close'] > today['Open']):
            
            
            # Calculate maximum number of shares that can be bought with available capital
            max_shares = math.floor(capital / today['Close'])
            
            if max_shares > 0:
                # Buy the maximum number of shares
                buy_amount = max_shares * today['Close']
                positions.append(('Buy', today.name.strftime('%Y-%m-%d'), today['Close'], max_shares, capital))
                # Deduct purchase amount from trading capital
                capital -= buy_amount

        # Sell condition
        if positions and positions[-1][0] == 'Buy':
            # Hold the position until we find a sell opportunity
            for j in range(i + 1, len(data)):
                sell_candidate = data.iloc[j]
                next_day_open = data.iloc[j]['Open'] if j < len(data) else None
                
                if next_day_open is not None and next_day_open >= (positions[-1][2] * 1.03):
                    # Intraday sell for at least 3% profit
                    intraday_sell_price = next_day_open
                    sell_amount = intraday_sell_price * positions[-1][3]
                    profit += (sell_amount - positions[-1][2] * positions[-1][3])
                    capital += sell_amount  # Add sell amount to trading capital
                    positions.append(('Sell (Intraday)', sell_candidate.name.strftime('%Y-%m-%d'), intraday_sell_price, positions[-1][3]))
                    break
                elif next_day_open is not None and sell_candidate['Close'] >= (positions[-1][2] * 1.04):
                    # Normal sell at least 4% higher
                    sell_price = sell_candidate['Close']
                    sell_amount = sell_price * positions[-1][3]
                    profit += (sell_amount - positions[-1][2] * positions[-1][3])
                    capital += sell_amount  # Add sell amount to trading capital
                    positions.append(('Sell', sell_candidate.name.strftime('%Y-%m-%d'), sell_price, positions[-1][3]))
                    break

    # Calculate final profit percentage
    final_profit_percentage = ((capital - initial_capital) / initial_capital) * 100

    return positions, capital, final_profit_percentage

# Load historical stock data from CSV file
file_path = r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
df = pd.read_csv(file_path, parse_dates=['Timestamp'])

# Rename columns for easier access
df.rename(columns={'Timestamp': 'Date'}, inplace=True)
df.set_index('Date', inplace=True)

# Set initial capital for backtesting
initial_capital = 50000  # Total initial capital

# Perform backtesting
positions, final_capital, final_profit_percentage = backtest_trading_strategy(df, initial_capital)

# Output results
print("Positions:")
for position in positions:
    print(position)

print(f"\nFinal Capital: ${final_capital:.2f}")
print(f"Final Profit Percentage: {final_profit_percentage:.2f}%")
