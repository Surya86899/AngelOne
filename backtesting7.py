# Training AIML model
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# List of file paths to your data files
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


# Helper function to calculate technical indicators using TA-Lib
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD

def calculate_technical_indicators(data):
    # Calculate Moving Averages (SMA and EMA)
    sma_indicator = SMAIndicator(close=data['Close'], window=20)
    data['SMA_20'] = sma_indicator.sma_indicator()

    ema_indicator_20 = EMAIndicator(close=data['Close'], window=20)
    data['EMA_20'] = ema_indicator_20.ema_indicator()

    ema_indicator_50 = EMAIndicator(close=data['Close'], window=50)
    data['EMA_50'] = ema_indicator_50.ema_indicator()

    # RSI
    rsi_indicator = RSIIndicator(close=data['Close'], window=14)
    data['RSI'] = rsi_indicator.rsi()

    # MACD
    macd_indicator = MACD(close=data['Close'], window_slow=26, window_fast=12, window_sign=9)
    data['MACD'] = macd_indicator.macd()
    data['MACD_Signal'] = macd_indicator.macd_signal()
    data['MACD_Hist'] = macd_indicator.macd_diff()

    # Bollinger Bands
    bollinger = BollingerBands(close=data['Close'], window=20, window_dev=2)
    data['BB_upper'] = bollinger.bollinger_hband()
    data['BB_middle'] = bollinger.bollinger_mavg()
    data['BB_lower'] = bollinger.bollinger_lband()

    return data

# Function to add previous day's high, low as features
def add_previous_day_features(data):
    data['Prev_High'] = data['High'].shift(1)
    data['Prev_Low'] = data['Low'].shift(1)
    data['Prev_Close'] = data['Close'].shift(1)
    return data

# Function to load data and perform feature engineering
def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp')
    
    # Sort data by Timestamp (important for time series)
    data = data.sort_index()

    # Add technical indicators
    data = calculate_technical_indicators(data)
    
    # Add previous day's High, Low, Close
    data = add_previous_day_features(data)
    
    # Drop rows with NaN values (can happen because of shift and indicator calculations)
    data = data.dropna()

    # Add Target: 1 for Price up, 0 for Price down (binary classification)
    data['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

    return data

# Function to train machine learning model (Random Forest)
def train_rf_model(X_train, y_train, X_test, y_test):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Classification Report for Random Forest Model:")
    print(classification_report(y_test, y_pred))

# Function to train deep learning model (LSTM)
def train_lstm_model(X_train, y_train, X_test, y_test):
    # Reshape X for LSTM input [samples, time steps, features]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Define LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=10, batch_size=32)

    # Evaluate the model
    y_pred = model.predict(X_test)
    y_pred = (y_pred > 0.5)  # Convert probabilities to 0 or 1

    print("Classification Report for LSTM Model:")
    print(classification_report(y_test, y_pred))

# Main function to loop over the file paths and train models
def main():
    for file_path in file_paths:
        print(f"Training model for file: {file_path}")
        
        # Load and preprocess the data
        data = load_and_preprocess_data(file_path)

        # Prepare features and target
        features = ['SMA_20', 'EMA_20', 'EMA_50', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist', 'BB_upper', 'BB_middle', 'BB_lower', 'Prev_High', 'Prev_Low', 'Prev_Close']
        X = data[features]
        y = data['Target']

        # Normalize the features using MinMaxScaler
        scaler = MinMaxScaler(feature_range=(0, 1))
        X_scaled = scaler.fit_transform(X)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Train and evaluate Random Forest model
        print("Training Random Forest model...")
        train_rf_model(X_train, y_train, X_test, y_test)

        # Train and evaluate LSTM model
        print("Training LSTM model...")
        train_lstm_model(X_train, y_train, X_test, y_test)

# Run the main function
if __name__ == "__main__":
    main()
