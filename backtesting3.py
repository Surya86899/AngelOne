import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Supertrend(df, period=10, multiplier=3):
    hl2 = (df['High'] + df['Low']) / 2
    df['ATR'] = df['High'].rolling(window=period).max() - df['Low'].rolling(window=period).min()
    df['Upperband'] = hl2 + (multiplier * df['ATR'])
    df['Lowerband'] = hl2 - (multiplier * df['ATR'])
    df['Supertrend'] = np.nan
    df['Supertrend Direction'] = 0

    for current in range(1, len(df.index)):
        previous = current - 1

        if (df['Close'].iloc[current] > df['Upperband'].iloc[previous]):
            df.loc[df.index[current], 'Supertrend'] = df['Lowerband'].iloc[current]
            df.loc[df.index[current], 'Supertrend Direction'] = 1
        elif (df['Close'].iloc[current] < df['Lowerband'].iloc[previous]):
            df.loc[df.index[current], 'Supertrend'] = df['Upperband'].iloc[current]
            df.loc[df.index[current], 'Supertrend Direction'] = -1
        else:
            df.loc[df.index[current], 'Supertrend'] = df['Supertrend'].iloc[previous]
            df.loc[df.index[current], 'Supertrend Direction'] = df['Supertrend Direction'].iloc[previous]

    return df

# Load historical price data
df = pd.read_csv(r'C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)

# Calculate Supertrend indicator
df = Supertrend(df)

# Implement the strategy
initial_balance = 10000
balance = initial_balance
position = None
entry_price = 0
stop_loss = 0
take_profit = 0
risk_reward_ratio = 3
risk_percentage = 0.01

trade_log = []
min_gap = 5  # Minimum number of bars to wait before taking a new trade

i = 0
while i < len(df):
    if position is None:
        if i > 0 and df['Supertrend Direction'].iloc[i] == 1 and df['Supertrend Direction'].iloc[i-1] == 1:
            position = 'long'
            entry_price = df['Close'].iloc[i]
            stop_loss = entry_price - (entry_price * risk_percentage)
            take_profit = entry_price + ((entry_price - stop_loss) * risk_reward_ratio)
            trade_log.append(('BUY', df.index[i], entry_price, stop_loss, take_profit, balance))
    elif position == 'long':
        if df['Close'].iloc[i] <= stop_loss or df['Close'].iloc[i] >= take_profit or df['Supertrend Direction'].iloc[i] == -1:
            exit_price = df['Close'].iloc[i]
            profit = exit_price - entry_price
            balance += profit
            trade_log.append(('SELL', df.index[i], exit_price, stop_loss, take_profit, balance))
            position = None
            i += min_gap  # Add a gap before the next trade
    i += 1

# Convert trade log to DataFrame for better visualization
trade_log_df = pd.DataFrame(trade_log, columns=['Action', 'Date', 'Price', 'Stop Loss', 'Take Profit', 'Balance'])

# Plot results
plt.figure(figsize=(14, 7))
plt.plot(df['Close'], label='Close Price')
plt.plot(df['Supertrend'], label='Supertrend')
buy_signals = trade_log_df[trade_log_df['Action'] == 'BUY']
sell_signals = trade_log_df[trade_log_df['Action'] == 'SELL']
plt.scatter(buy_signals['Date'], buy_signals['Price'], marker='^', color='green', label='Buy Signal')
plt.scatter(sell_signals['Date'], sell_signals['Price'], marker='v', color='red', label='Sell Signal')
plt.title('Supertrend Strategy Backtest')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Print trade log
print(trade_log_df)

# Print final balance
print(f"Initial Balance: ${initial_balance}")
print(f"Final Balance: ${balance}")
