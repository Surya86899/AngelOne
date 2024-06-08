import pandas as pd

def backtest_trading_strategy(data, initial_capital):
    # Calculate necessary indicators (volume, price changes, moving averages)
    data['VolumeRatio'] = data['Volume'] / data['Volume'].shift(1)
    data['CloseChange'] = data['Close'].pct_change() * 100
    data['DEMA_5'] = data['Close'].ewm(span=5).mean()
    data['DEMA_8'] = data['Close'].ewm(span=8).mean()
    data['DEMA_13'] = data['Close'].ewm(span=13).mean()

    # Initialize variables to track trades and performance
    positions = []
    capital = initial_capital / 2  # Use half of the initial capital for trading
    reserve = initial_capital / 2  # Keep the other half as reserve
    buy_price = 0
    profit = 0

    # Iterate through each day's data to apply the trading strategy
    for i in range(1, len(data)):
        today = data.iloc[i]
        previous = data.iloc[i - 1]

        if (today['VolumeRatio'] >= 3 and
            today['CloseChange'] >= 4 and
            today['High'] > previous['High'] and
            today['DEMA_5'] > today['DEMA_8'] > today['DEMA_13'] and
            today['Close'] > today['Open']):
            # Buy the stock
            positions.append(('Buy', today['Close']))
            buy_price = today['Close']
            # Deduct purchase amount from trading capital
            capital -= buy_price

        if positions and positions[-1][0] == 'Buy':
            # Check if sell condition is met the next day
            next_day_open = data.iloc[i + 1]['Open'] if i + 1 < len(data) else None
            if next_day_open is not None and next_day_open <= buy_price * 1.01:
                # Buy the stock for intraday trading aiming for at least 3% profits
                intraday_sell_price = next_day_open * 1.03
                profit += (intraday_sell_price - buy_price)
                capital += intraday_sell_price  # Add sell amount to trading capital
                positions.append(('Sell (Intraday)', intraday_sell_price))
            else:
                # Sell the stock the next morning before 9:30 am at least 4% higher
                sell_price = buy_price * 1.04
                profit += (sell_price - buy_price)
                capital += sell_price  # Add sell amount to trading capital
                positions.append(('Sell', sell_price))

    # Calculate final profit percentage
    final_profit_percentage = ((capital - (initial_capital / 2)) / (initial_capital / 2)) * 100

    return positions, capital + reserve, final_profit_percentage

# Load historical stock data from CSV file
file_path = r"C:\Documents\GitHub\AngelOne\historical files\M&M-EQ_ONE_DAY_candle_data.csv"
df = pd.read_csv(file_path, parse_dates=['Timestamp'])

# Rename columns for easier access
df.rename(columns={'Timestamp': 'Date'}, inplace=True)
df.set_index('Date', inplace=True)

# Set initial capital for backtesting (use half of the specified initial amount)
initial_capital = 10000  # Total initial capital
trading_capital = initial_capital / 2  # Use half for trading

# Perform backtesting
positions, final_capital, final_profit_percentage = backtest_trading_strategy(df, trading_capital)

# Output results
print("Positions:")
for position in positions:
    print(position)

print(f"\nFinal Capital: ${final_capital:.2f}")
print(f"Final Profit Percentage: {final_profit_percentage:.2f}%")
