import pandas as pd
import numpy as np

import ta
from ta.trend import ADXIndicator
from ta.trend import PSARIndicator
from ta.trend import CCIIndicator
from ta.momentum import RSIIndicator
from ta.momentum import StochasticOscillator
from ta.volatility import BollingerBands

import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates  # Import matplotlib dates module
from matplotlib.dates import date2num, DateFormatter

from mplfinance.original_flavor import candlestick_ohlc


def calculate_supertrend(file_path, lookback, multiplier, start_date=None, end_date=None):
    # Read data from CSV file
    data = pd.read_csv(file_path)
    
    # Convert 'Timestamp' column to datetime
    if 'Timestamp' in data.columns:
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    
    # Filter data based on start and end dates
    if start_date is not None and end_date is not None:
        data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]
    elif start_date is not None:
        data = data[data['Timestamp'] >= start_date]
    elif end_date is not None:
        data = data[data['Timestamp'] <= end_date]
    
    # Reset index after filtering
    data.reset_index(drop=True, inplace=True)
    
    # Extract necessary columns
    high = data['High']
    low = data['Low']
    close = data['Close']
    
    # Calculate ATR using ta library
    atr = ta.volatility.average_true_range(high, low, close, window=lookback)
    
    # Calculate HL AVG and BASIC UPPER & LOWER BAND
    hl_avg = (high + low) / 2
    upper_band = hl_avg + multiplier * atr
    lower_band = hl_avg - multiplier * atr
    
    # Initialize arrays for final bands and supertrend
    final_bands = pd.DataFrame(index=data.index, columns=['upper', 'lower'])
    final_bands['upper'] = np.nan
    final_bands['lower'] = np.nan
    
    supertrend = pd.Series(index=data.index, name=f'supertrend_{lookback}')
    
    # Calculate final bands
    for i in range(len(data)):
        if i == 0:
            final_bands.iloc[i, 0] = upper_band[i]
            final_bands.iloc[i, 1] = lower_band[i]
        else:
            if (upper_band[i] < final_bands.iloc[i-1, 0]) or (close[i-1] > final_bands.iloc[i-1, 0]):
                final_bands.iloc[i, 0] = upper_band[i]
            else:
                final_bands.iloc[i, 0] = final_bands.iloc[i-1, 0]
            
            if (lower_band[i] > final_bands.iloc[i-1, 1]) or (close[i-1] < final_bands.iloc[i-1, 1]):
                final_bands.iloc[i, 1] = lower_band[i]
            else:
                final_bands.iloc[i, 1] = final_bands.iloc[i-1, 1]
    
    # Calculate Supertrend
    for i in range(len(data)):
        if i == 0:
            supertrend.iloc[i] = lower_band[i]
        elif supertrend.iloc[i-1] == final_bands.iloc[i-1, 0] and close.iloc[i] < final_bands.iloc[i, 0]:
            supertrend.iloc[i] = final_bands.iloc[i, 0]
        elif supertrend.iloc[i-1] == final_bands.iloc[i-1, 0] and close.iloc[i] > final_bands.iloc[i, 0]:
            supertrend.iloc[i] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i-1] == final_bands.iloc[i-1, 1] and close.iloc[i] > final_bands.iloc[i, 1]:
            supertrend.iloc[i] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i-1] == final_bands.iloc[i-1, 1] and close.iloc[i] < final_bands.iloc[i, 1]:
            supertrend.iloc[i] = final_bands.iloc[i, 0]
    
    # Define uptrend and downtrend
    uptrend = np.where(close > supertrend, supertrend, np.nan)
    downtrend = np.where(close < supertrend, supertrend, np.nan)
    
    return data, supertrend, uptrend, downtrend, close  # Return filtered data and close prices for plotting

def calculation_supertrend(data, atr_period=7, multiplier=3):
    hl2 = (data['High'] + data['Low']) / 2
    atr = data['High'].rolling(atr_period).max() - data['Low'].rolling(atr_period).min()
    atr = atr.rolling(atr_period).mean()

    supertrend = pd.DataFrame(index=data.index, columns=['Supertrend', 'Trend'])
    supertrend['Supertrend'] = hl2 + (multiplier * atr)
    supertrend['Trend'] = 1

    for i in range(1, len(supertrend)):
        if data['Close'].iloc[i] > supertrend['Supertrend'].iloc[i - 1]:
            supertrend.loc[supertrend.index[i], 'Supertrend'] = hl2.iloc[i] - (multiplier * atr.iloc[i])
            supertrend.loc[supertrend.index[i], 'Trend'] = 1
        elif data['Close'].iloc[i] < supertrend['Supertrend'].iloc[i - 1]:
            supertrend.loc[supertrend.index[i], 'Supertrend'] = hl2.iloc[i] + (multiplier * atr.iloc[i])
            supertrend.loc[supertrend.index[i], 'Trend'] = -1

    return supertrend['Supertrend'], supertrend['Trend']

def visualize_supertrend(data, supertrend_values, uptrend, downtrend):
    # Prepare the data for candlestick plot
    ohlc = data[['Timestamp', 'Open', 'High', 'Low', 'Close']].copy()
    ohlc['Timestamp'] = ohlc['Timestamp'].apply(date2num)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot candlesticks
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Plot the Supertrend values
    ax.plot(data['Timestamp'], supertrend_values, color='green', linewidth=2, label='Supertrend')
    ax.plot(data['Timestamp'], uptrend, color='green', linestyle='--', label='ST Uptrend')
    ax.plot(data['Timestamp'], downtrend, color='red', linestyle='--', label='ST Downtrend')
    
    # Plot the uptrend and downtrend regions with colors
    ax.fill_between(data['Timestamp'], supertrend_values, data['Close'], 
                    where=(data['Close'] > supertrend_values), color='lightgreen', alpha=0.3)
    ax.fill_between(data['Timestamp'], supertrend_values, data['Close'], 
                    where=(data['Close'] < supertrend_values), color='lightcoral', alpha=0.3)
    
    # Add title and labels
    ax.set_title('Supertrend Visualization with Candlesticks')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    
    # Add gridlines and legend
    ax.grid(True)
    ax.legend()
    
    # Set x-axis date format
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    # Set the limits of the x-axis to the range of your data
    ax.set_xlim(data['Timestamp'].iloc[0], data['Timestamp'].iloc[-1])
    
    plt.tight_layout()
    plt.show()



def calculate_EMA(file_path, length, start_date=None, end_date=None):
    # Step 1: Load Data from CSV
    data = pd.read_csv(file_path)
    
    # Filter data based on start and end dates
    if start_date is not None and end_date is not None:
        data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]
    elif start_date is not None:
        data = data[data['Timestamp'] >= start_date]
    elif end_date is not None:
        data = data[data['Timestamp'] <= end_date]
    
    # Calculate EMA
    data['EMA'] = ta.trend.ema_indicator(data['Close'], window=length)
    
    return data['EMA']

def calculation_EMA(close_prices, length):
    return ta.trend.ema_indicator(close_prices, window=length)

def visualize_EMA(file_path, length, ema_values, start_date=None, end_date=None):
    # Read the data from the CSV file
    data = pd.read_csv(file_path)
    
    # Filter data based on start and end dates
    if start_date is not None and end_date is not None:
        data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]
    elif start_date is not None:
        data = data[data['Timestamp'] >= start_date]
    elif end_date is not None:
        data = data[data['Timestamp'] <= end_date]
    
    # Convert 'Timestamp' to datetime
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    
    # Prepare the data for candlestick plot (example with Close price)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot candlesticks (if 'Open', 'High', 'Low', 'Close' columns exist in data)
    candlestick_ohlc(ax, zip(date2num(data['Timestamp']), data['Open'], data['High'], data['Low'], data['Close']),
                     width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Plot the EMA values
    ax.plot(data['Timestamp'], ema_values, label=f'EMA ({length})', color='blue')
    
    # Add title and labels
    ax.set_title(f'EMA ({length}) Visualization with Candlesticks')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    
    # Add gridlines and legend
    ax.grid(True)
    ax.legend()
    
    # Set x-axis date format
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    # Set the limits of the x-axis to the range of your data
    ax.set_xlim(data['Timestamp'].iloc[0], data['Timestamp'].iloc[-1])
    
    plt.tight_layout()
    plt.show()



def calculate_macd(file_path, start_date, end_date, fast_length=14, slow_length=44, signal_length=9, source='Close', sma_source='EMA', sma_signal='EMA'):
    """
    Calculate MACD, Signal, and Histogram for a given file path and date range.

    Parameters:
    file_path (str): Path to the CSV file with OHLC data
    start_date (str): Start date for the data (format: 'YYYY-MM-DD')
    end_date (str): End date for the data (format: 'YYYY-MM-DD')
    fast_length (int): The period for the fast moving average
    slow_length (int): The period for the slow moving average
    signal_length (int): The period for the signal line
    source (str): The column name to calculate the MACD on
    sma_source (str): Type of moving average for the MACD line ('SMA' or 'EMA')
    sma_signal (str): Type of moving average for the signal line ('SMA' or 'EMA')

    Returns:
    pd.DataFrame: DataFrame with MACD, Signal, and Histogram columns
    """
    # Read data from file
    df = pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp')

    # Filter data by date range
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    # Ensure the source column exists
    if source not in df.columns:
        raise ValueError(f"Source column '{source}' not found in data")

    src = df[source]

    if sma_source == 'SMA':
        fast_ma = src.rolling(window=fast_length).mean()
        slow_ma = src.rolling(window=slow_length).mean()
    else:  # EMA
        fast_ma = src.ewm(span=fast_length, adjust=False).mean()
        slow_ma = src.ewm(span=slow_length, adjust=False).mean()

    macd = fast_ma - slow_ma

    if sma_signal == 'SMA':
        signal = macd.rolling(window=signal_length).mean()
    else:  # EMA
        signal = macd.ewm(span=signal_length, adjust=False).mean()

    hist = macd - signal

    df['MACD'] = macd
    df['Signal'] = signal
    df['Histogram'] = hist

    return df

def calculation_macd(data, fast_period=12, slow_period=26, signal_period=9):
    fast_ema = data['Close'].ewm(span=fast_period, adjust=False).mean()
    slow_ema = data['Close'].ewm(span=slow_period, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    return macd_line, signal_line, macd_histogram

def visualize_macd(df):
    """
    Plot MACD, Signal, and Histogram.

    Parameters:
    df (pd.DataFrame): DataFrame with 'MACD', 'Signal', and 'Histogram' columns
    """
    plt.figure(figsize=(12, 8))

    # Plot MACD and Signal
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['MACD'], label='MACD', color='blue')
    plt.plot(df.index, df['Signal'], label='Signal', color='orange')
    plt.title('MACD and Signal Line')
    plt.legend(loc='upper left')

    # Plot Histogram
    plt.subplot(2, 1, 2)
    plt.bar(df.index, df['Histogram'], label='Histogram', color='grey')
    plt.axhline(0, color='red', linewidth=0.5)
    plt.title('MACD Histogram')
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.show()



def calculate_adx(file_path, start_date, end_date, window=14, fillna=False):
    # Read CSV file
    data = pd.read_csv(file_path, parse_dates=['Timestamp'])

    # Filter data by date range
    mask = (data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)
    data = data.loc[mask]

    # Ensure the data is sorted by date
    data.sort_values(by='Timestamp', inplace=True)

    # Initialize ADXIndicator
    adx_indicator = ADXIndicator(
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        window=window,
        fillna=fillna
    )

    # Calculate ADX values
    data['ADX'] = adx_indicator.adx()

    # Return required columns
    return data[['Timestamp', 'Open', 'High', 'Low', 'Close', 'ADX']]

def calculation_adx(data, period=14):
    plus_dm = data['High'].diff()
    minus_dm = data['Low'].diff()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr1 = pd.DataFrame(data['High'] - data['Low'])
    tr2 = pd.DataFrame(abs(data['High'] - data['Close'].shift(1)))
    tr3 = pd.DataFrame(abs(data['Low'] - data['Close'].shift(1)))
    tr = pd.concat([tr1, tr2, tr3], axis=1, join='inner').max(axis=1)

    atr = tr.rolling(window=period, min_periods=1).mean()
    plus_di = 100 * (plus_dm.ewm(alpha=1/period).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha=1/period).mean() / atr))
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.ewm(alpha=1/period).mean()

    return adx

def visualize_adx(data, adx_values):
    # Ensure the data contains the required columns
    if not {'Timestamp', 'Open', 'High', 'Low', 'Close'}.issubset(data.columns):
        raise ValueError("Data must contain 'Timestamp', 'Open', 'High', 'Low', and 'Close' columns")
    
    # Prepare the data for candlestick plot
    ohlc = data[['Timestamp', 'Open', 'High', 'Low', 'Close']].copy()
    ohlc['Timestamp'] = ohlc['Timestamp'].apply(date2num)
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot candlesticks
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Create another axis for the ADX plot sharing the same x-axis
    ax2 = ax1.twinx()
    
    # Plot the ADX values
    ax2.plot(data['Timestamp'], adx_values, color='blue', linewidth=2, label='ADX')
    
    # Add title and labels
    ax1.set_title('Candlestick Chart with ADX')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax2.set_ylabel('ADX')
    
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



def calculate_parabolic_sar(file_path, start_date=None, end_date=None, start=0.02, increment=0.02, maximum=0.2):
    # Load CSV data into a DataFrame
    df = pd.read_csv(file_path, parse_dates=True, index_col='Timestamp')

    # Optionally filter data by start_date and end_date
    if start_date:
        start_date = pd.to_datetime(start_date)
        df = df[df.index >= start_date]
    if end_date:
        end_date = pd.to_datetime(end_date)
        df = df[df.index <= end_date]

    # Calculate Parabolic SAR using ta library
    psar = PSARIndicator(df['High'], df['Low'], df['Close'], step=start, max_step=maximum)
    df['PSAR'] = psar.psar()

    return df

def visualize_parabolic_sar(data, sar_values):
    # Prepare the data for candlestick plot
    ohlc = data.reset_index()
    ohlc['Timestamp'] = ohlc['Timestamp'].apply(date2num)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot candlesticks
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Plot the Parabolic SAR values as dots
    ax.scatter(data.index, sar_values, color='blue', marker='.', label='Parabolic SAR')
    
    # Plot the uptrend and downtrend regions with colors (optional)
    # You can customize this based on your specific visualization needs
    
    # Add title and labels
    ax.set_title('Parabolic SAR Visualization with Candlesticks')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    
    # Add gridlines and legend
    ax.grid(True)
    ax.legend()
    
    # Set x-axis date format
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    # Set the limits of the x-axis to the range of your data
    ax.set_xlim(data.index[0], data.index[-1])
    
    plt.tight_layout()
    plt.show()



def calculate_rsi(start_date, end_date, file_path):
    # Load your data from file_path into a DataFrame
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)

    # Filter data based on start_date and end_date
    df = df.loc[start_date:end_date]

    # Calculate RSI using RSIIndicator class
    rsi_length = 14
    indicator = RSIIndicator(close=df['Close'], window=rsi_length)
    df['RSI'] = indicator.rsi()

    return df

def calculation_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def visualize_rsi(df):
    # Prepare the data for candlestick plot
    ohlc = df[['Open', 'High', 'Low', 'Close']].copy()
    ohlc['Date'] = df.index.map(date2num)
    ohlc = ohlc[['Date', 'Open', 'High', 'Low', 'Close']]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})

    # Plot candlesticks
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Plot the RSI
    ax2.plot(df.index, df['RSI'], label='RSI', color='#7E57C2')

    # Plotting RSI bands
    ax2.axhline(y=70, color='#FF0000', linestyle='-', label='RSI Upper Band')
    ax2.axhline(y=50, color='#FFFF00', linestyle='-', label='RSI Middle Band')
    ax2.axhline(y=30, color='#008000', linestyle='-', label='RSI Lower Band')
    
    # Filling RSI background
    ax2.fill_between(df.index, 70, df['RSI'], where=(df['RSI'] >= 70), facecolor='lightcoral', alpha=0.3)
    ax2.fill_between(df.index, 30, df['RSI'], where=(df['RSI'] <= 30), facecolor='lightgreen', alpha=0.3)
    
    # Add titles and labels
    ax1.set_title('Price Chart with Candlesticks')
    ax1.set_ylabel('Price')
    ax2.set_title('Relative Strength Index (RSI)')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')
    
    # Add gridlines and legend
    ax1.grid(True)
    ax1.legend()
    ax2.grid(True)
    ax2.legend()
    
    # Set x-axis date format for both subplots
    ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.setp(ax1.get_xticklabels(), rotation=45)
    plt.setp(ax2.get_xticklabels(), rotation=45)

    # Set the limits of the x-axis to the range of your data
    ax1.set_xlim(df.index[0], df.index[-1])
    ax2.set_xlim(df.index[0], df.index[-1])
    
    plt.tight_layout()
    plt.show()



def calculate_stochastic_oscillator(file_path: str, start_date: str, end_date: str) -> tuple:

    # Read CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert date columns to datetime type
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Filter DataFrame based on start_date and end_date
    mask = (df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)
    df = df.loc[mask].reset_index(drop=True)

    # Create StochasticOscillator instance
    stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'])

    # Calculate stochastic oscillator values
    stoch_k = stoch.stoch()
    stoch_d = stoch.stoch_signal()

    # Extract date part from Timestamp column
    df['Date'] = df['Timestamp'].dt.date

    # Combine results with dates into a single Series
    stoch_k = pd.Series(stoch_k.values, index=df['Date'], name='Stochastic K')
    stoch_d = pd.Series(stoch_d.values, index=df['Date'], name='Stochastic D')

    return stoch_k, stoch_d, df

def visualize_stochastic_oscillator(stoch_k: pd.Series, stoch_d: pd.Series, df: pd.DataFrame, start_date: str, end_date: str):
    
    # Prepare the data for candlestick plot
    ohlc = df[['Timestamp', 'Open', 'High', 'Low', 'Close']].copy()
    ohlc['Timestamp'] = ohlc['Timestamp'].map(date2num)
    ohlc = ohlc[['Timestamp', 'Open', 'High', 'Low', 'Close']]

    # Filter ohlc data to match the specified date range
    mask = (df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)
    ohlc = ohlc.loc[mask].reset_index(drop=True)

    # Create subplots with specific ratios
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})

    # Plot candlesticks
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

    # Plot Stochastic K and Stochastic D
    ax2.plot(stoch_k.index, stoch_k.values, label='Stochastic K', color='blue')
    ax2.plot(stoch_d.index, stoch_d.values, label='Stochastic D', color='orange')

    # Add horizontal lines for overbought and oversold levels
    ax2.axhline(y=80, color='r', linestyle='--', linewidth=1, label='Overbought (80)')
    ax2.axhline(y=20, color='g', linestyle='--', linewidth=1, label='Oversold (20)')

    # Highlight regions where Stochastic K is above/below Stochastic D
    ax2.fill_between(stoch_k.index, stoch_k.values, stoch_d.values,
                     where=(stoch_k > stoch_d), interpolate=True, color='lightgreen', alpha=0.3)
    ax2.fill_between(stoch_k.index, stoch_k.values, stoch_d.values,
                     where=(stoch_k < stoch_d), interpolate=True, color='lightcoral', alpha=0.3)

    # Set titles and labels
    ax1.set_title('Price Chart with Candlesticks')
    ax1.set_ylabel('Price')
    ax2.set_title('Stochastic Oscillator Visualization')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Stochastic Oscillator Value')

    # Add gridlines and legend
    ax1.grid(True)
    ax1.legend()
    ax2.grid(True)
    ax2.legend()

    # Set x-axis date format
    ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    # Rotate date labels for better readability
    plt.setp(ax1.get_xticklabels(), rotation=45)
    plt.setp(ax2.get_xticklabels(), rotation=45)

    # Set x-axis limits to match the date range of the data
    ax1.set_xlim(ohlc['Timestamp'].iloc[0], ohlc['Timestamp'].iloc[-1])
    ax2.set_xlim(ohlc['Timestamp'].iloc[0], ohlc['Timestamp'].iloc[-1])

    # Adjust layout to prevent clipping of labels
    plt.tight_layout()
    plt.show()



def calculate_cci(file_path: str, start_date: str, end_date: str, window: int, constant: float, fillna: bool) -> pd.DataFrame:
    # Read the CSV file
    data = pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp')
    
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data by date range
    data = data.loc[start_date:end_date]
    
    # Ensure required columns are present
    if not {'High', 'Low', 'Close'}.issubset(data.columns):
        raise ValueError("The input data must contain 'High', 'Low', and 'Close' columns.")
    
    # Initialize the CCI indicator
    cci_indicator = CCIIndicator(
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        window=window,
        constant=constant,
        fillna=fillna
    )
    
    # Calculate CCI and add to DataFrame
    data['CCI'] = cci_indicator.cci()
    
    return data

def visualize_cci(df):
    # Prepare the data for candlestick plot
    ohlc = df[['Open', 'High', 'Low', 'Close']].copy()
    ohlc['Date'] = df.index.map(date2num)
    ohlc = ohlc[['Date', 'Open', 'High', 'Low', 'Close']]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})

    # Plot candlesticks
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Plot the CCI
    ax2.plot(df.index, df['CCI'], label='CCI', color='#7E57C2')

    # Plotting CCI bands
    ax2.axhline(y=100, color='#FF0000', linestyle='-', label='CCI Upper Band')
    ax2.axhline(y=0, color='#FFFF00', linestyle='-', label='CCI Middle Band')
    ax2.axhline(y=-100, color='#008000', linestyle='-', label='CCI Lower Band')
    
    # Filling CCI background
    ax2.fill_between(df.index, 100, df['CCI'], where=(df['CCI'] >= 100), facecolor='lightcoral', alpha=0.3)
    ax2.fill_between(df.index, -100, df['CCI'], where=(df['CCI'] <= -100), facecolor='lightgreen', alpha=0.3)
    
    # Add titles and labels
    ax1.set_title('Price Chart with Candlesticks')
    ax1.set_ylabel('Price')
    ax2.set_title('Commodity Channel Index (CCI)')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('CCI')
    
    # Add gridlines and legend
    ax1.grid(True)
    ax1.legend()
    ax2.grid(True)
    ax2.legend()
    
    # Set x-axis date format for both subplots
    ax1.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y'))
    ax2.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y'))
    plt.setp(ax1.get_xticklabels(), rotation=45)
    plt.setp(ax2.get_xticklabels(), rotation=45)

    # Set the limits of the x-axis to the range of your data
    ax1.set_xlim(df.index[0], df.index[-1])
    ax2.set_xlim(df.index[0], df.index[-1])
    
    plt.tight_layout()
    plt.show()



def calculate_bollinger_bands(file_path: str, start_date: str, end_date: str) -> pd.DataFrame:
    # Load the data from the file
    df = pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp')
    
    # Filter the data by the given date range
    df = df.loc[start_date:end_date]
    
    # Ensure there is a 'Close' column in the DataFrame
    if 'Close' not in df.columns:
        raise ValueError("DataFrame must contain a 'Close' column")
    
    # Calculate Bollinger Bands
    bb = BollingerBands(df['Close'])
    
    # Combine the original DataFrame with the Bollinger Bands
    df['Bollinger_MAVG'] = bb.bollinger_mavg()  # Middle Band  
    df['Bollinger_HBAND'] = bb.bollinger_hband()    # Upper Band 
    df['Bollinger_LBAND'] = bb.bollinger_lband()    # Lower Band
    df['Bollinger_WBAND'] = bb.bollinger_wband()    # Width of the Band
    df['Bollinger_PBAND'] = bb.bollinger_pband()    # Percentage of how close the prise is to the upper or lower Band
    df['Bollinger_HBAND_IND'] = bb.bollinger_hband_indicator()  # (1 or 0) 1 when closing price is above upper band and viceversa
    df['Bollinger_LBAND_IND'] = bb.bollinger_lband_indicator()  # (1 or 0) 1 when closing price is below lower band and viceversa
    
    return df

def calculation_bollinger_bands(data, window=20, num_of_std=2):
    rolling_mean = data['Close'].rolling(window).mean()
    rolling_std = data['Close'].rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return upper_band, lower_band

def visualize_bollinger_bands(data):
    # Prepare the data for candlestick plot
    ohlc = data[['Timestamp', 'Open', 'High', 'Low', 'Close']].copy()
    ohlc['Timestamp'] = ohlc['Timestamp'].apply(date2num)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot candlesticks
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Plot the Bollinger Bands
    ax.plot(data['Timestamp'], data['Bollinger_MAVG'], color='blue', linewidth=2, label='Bollinger MAVG')
    ax.plot(data['Timestamp'], data['Bollinger_HBAND'], color='red', linewidth=1, linestyle='--', label='Bollinger HBAND')
    ax.plot(data['Timestamp'], data['Bollinger_LBAND'], color='green', linewidth=1, linestyle='--', label='Bollinger LBAND')
    
    # Fill the area between the upper and lower bands
    ax.fill_between(data['Timestamp'], data['Bollinger_HBAND'], data['Bollinger_LBAND'], color='gray', alpha=0.2)
    
    # Add title and labels
    ax.set_title('Bollinger Bands Visualization with Candlesticks')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    
    # Add gridlines and legend
    ax.grid(True)
    ax.legend()
    
    # Set x-axis date format
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    # Set the limits of the x-axis to the range of your data
    ax.set_xlim(data['Timestamp'].iloc[0], data['Timestamp'].iloc[-1])
    
    plt.tight_layout()
    plt.show()
