import indicators

# Example usage
factor = 3
atr_length = 10
file_path = "C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
start_date = '2024-01-01T00:00:00+05:30' 
end_date = '2024-06-14T00:00:00+05:30' 
length = 9 # No of days

# *************************Supertrend Calculation and Visualization*************************

# file_path = "C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"  # Adjust the file path
# lookback = 10
# multiplier = 3.0
# start_date = None#'2023-01-01T00:00:00+05:30' 
# end_date = None#'2023-06-07T00:00:00+05:30'

# data, supertrend, uptrend, downtrend, close = indicators.calculate_supertrend(file_path, lookback, multiplier, start_date, end_date)
# print(supertrend)
# indicators.visualize_supertrend(data, supertrend, uptrend, downtrend)

# *************************Supertrend Calculation and Visualization*************************



# **************Exponential Moving Average(EMA) Calculation and Visualization**************

# ema_values = indicators.calculate_EMA(file_path, length, start_date=None, end_date=None)
# print(ema_values)
# indicators.visualize_EMA(file_path, length, ema_values, start_date=None, end_date=None)

# **************Exponential Moving Average(EMA) Calculation and Visualization**************



# *******Moving Average Convergence Divergence(MACD) Calculation and Visualization*******

# # Calculate MACD
# df = indicators.calculate_macd(file_path, start_date, end_date)
# print(df)
# # Plot MACD
# indicators.visualize_macd(df)

# *******Moving Average Convergence Divergence(MACD) Calculation and Visualization*******



# *************Average Directional Index (ADX) Calculation and Visualization*************

# # Example usage
# file_path = r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
# start_date = '2024-04-01T00:00:00+05:30' 
# end_date = '2024-06-14T00:00:00+05:30' 
# adx_data = indicators.calculate_adx(file_path, start_date, end_date)
# print(adx_data)
# indicators.visualize_adx(adx_data, adx_data['ADX'])

# *************Average Directional Index (ADX) Calculation and Visualization*************



# *************************Parabolic SAR Calculation and Visualization*************************

# # Example usage:
# file_path = r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
# start_date = '2024-01-01T00:00:00+05:30' 
# end_date = '2024-06-14T00:00:00+05:30' 

# # Calculate Parabolic SAR
# df = indicators.calculate_parabolic_sar(file_path, start_date, end_date)
# print(df)
# # Visualize Parabolic SAR
# indicators.visualize_parabolic_sar(df, df['PSAR'])

# *************************Parabolic SAR Calculation and Visualization*************************



# *************************Relative Strength Index (RSI) Calculation and Visualization*************************

# # Example usage:
# file_path = r"C:\Documents\GitHub\AngelOne\historical files\HDFCBANK-EQ_ONE_DAY_candle_data.csv"
# start_date = '2024-01-01T00:00:00+05:30' 
# end_date = '2024-06-14T00:00:00+05:30' 

# df = indicators.calculate_rsi(start_date, end_date, file_path)
# print(df)
# indicators.visualize_rsi(df)

# *************************Relative Strength Index (RSI) Calculation and Visualization*************************



# *************************Stochastic Oscillator Calculation and Visualization*************************

# # Example usage
# file_path = r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
# start_date = '2024-01-01T00:00:00+05:30'
# end_date = '2024-06-14T00:00:00+05:30'

# stoch_k, stoch_d, df = indicators.calculate_stochastic_oscillator(file_path, start_date, end_date)

# print("Stochastic K:")
# print(stoch_k)
# print("\nStochastic D:")
# print(stoch_d)
# print()
# print(df)

# indicators.visualize_stochastic_oscillator(stoch_k, stoch_d, df, start_date, end_date)

# *************************Stochastic Oscillator Calculation and Visualization*************************



# *************************Commodity Channel Index (CCI) Calculation and Visualization*************************

# # Example usage:
# file_path = r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
# start_date = '2024-01-01T00:00:00+05:30'
# end_date = '2024-06-14T00:00:00+05:30'
# window = 20
# constant = 0.015
# fillna = False
# cci_df = indicators.calculate_cci(file_path, start_date, end_date, window, constant, fillna)
# print(cci_df)
# indicators.visualize_cci(cci_df)

# *************************Commodity Channel Index (CCI) Calculation and Visualization*************************



# *************************Bollinger Bands Calculation and Visualization*************************

# # Example usage:
# file_path = r"C:\Documents\GitHub\AngelOne\historical files\ABB-EQ_ONE_DAY_candle_data.csv"
# start_date = '2024-01-01T00:00:00+05:30'
# end_date = '2024-06-20T00:00:00+05:30'
# df_with_bbands = indicators.calculate_bollinger_bands(file_path, start_date, end_date)
# df_with_bbands.reset_index(inplace=True)  # Reset index to get Timestamp as a column
# print(df_with_bbands)
# indicators.visualize_bollinger_bands(df_with_bbands)

# *************************Bollinger Bands Calculation and Visualization*************************



# *************************Average True Range (ATR) Calculation and Visualization*************************



# *************************Average True Range (ATR) Calculation and Visualization*************************


















