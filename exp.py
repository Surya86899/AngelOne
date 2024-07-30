import nselib
import numpy as np
import pandas as pd
import datetime as dt

# def is_business_day(now):
#     today = now.date()
#     holidays_df = nselib.trading_holiday_calendar()
#     holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'], format='%d-%b-%Y').dt.date
#     holidays = holidays_df['tradingDate'].values  # Convert to array of datetime.date objects

#     # Ensure all columns used in np.select have consistent data types
#     holidays_df['HolidayType'] = holidays_df['HolidayType'].astype(str)

#     condition1 = (holidays_df['HolidayType'] == 'National')
#     conditions = [condition1]

#     value1 = 'National Holiday'
#     values = [value1]
#     default_value = 'Other'

#     holidays_df['Product'] = np.select(conditions, values, default=default_value)

#     if today.weekday() >= 5 or today in holidays:
#         return False
#     return True

def is_business_day(now):
    today = now.date()
    holidays_df = nselib.trading_holiday_calendar()  # Assuming this returns a DataFrame
    holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'], format='%d-%b-%Y').dt.date
    holidays = holidays_df['tradingDate'].values  # Convert to array of datetime.date objects

    if today.weekday() >= 5 or today in holidays:
        return False
    return True

now = dt.datetime.now()
print(is_business_day(now))