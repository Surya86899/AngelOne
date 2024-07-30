import pandas as pd
from ta.volatility import AverageTrueRange
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import DateFormatter, date2num

def calculate_atr(file_path: str, start_date: str, end_date: str) -> pd.Series:
    # Load the data
    df = pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp')

    # Filter the data by date range
    df = df.loc[start_date:end_date]

    # Calculate the ATR
    atr = AverageTrueRange(df['High'], df['Low'], df['Close'])
    return atr.average_true_range()

def visualize_atr(file_path: str, atr_values: pd.Series, start_date: str, end_date: str):
    # Load the data for visualization, ensuring the 'Timestamp' column is parsed correctly
    df = pd.read_csv(file_path, parse_dates=['Timestamp'])

    # Filter the data for visualization to match the ATR calculation period
    data = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]

    # Ensure the data contains the required columns
    if not {'Timestamp', 'Open', 'High', 'Low', 'Close'}.issubset(data.columns):
        raise ValueError("Data must contain 'Timestamp', 'Open', 'High', 'Low', and 'Close' columns")
    
    # Prepare the data for candlestick plot
    ohlc = data[['Timestamp', 'Open', 'High', 'Low', 'Close']].copy()
    ohlc['Timestamp'] = ohlc['Timestamp'].apply(date2num)
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot candlesticks
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Create another axis for the ATR plot sharing the same x-axis
    ax2 = ax1.twinx()
    
    # Plot the ATR values
    ax2.plot(data['Timestamp'], atr_values, color='blue', linewidth=2, label='ATR')
    
    # Add title and labels
    ax1.set_title('Candlestick Chart with ATR')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax2.set_ylabel('ATR')
    
    # Add gridlines and legend
    ax1.grid(True)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    # Set x-axis date format
    ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    # Set the limits of the x-axis to the range of your data
    ax1.set_xlim(data['Timestamp'].iloc[0], data['Timestamp'].iloc[-1])
    
    plt.tight_layout()
    plt.show()

# Example usage:
file_path = r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
start_date = '2024-01-01'
end_date = '2024-06-20'
atr_series = calculate_atr(file_path, start_date, end_date)
print(atr_series)
visualize_atr(file_path, atr_series, start_date, end_date)
