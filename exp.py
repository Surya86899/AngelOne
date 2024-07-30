from datetime import datetime
import pandas as pd
import nselib

def is_business_day(now):
    today = now.date()
    holidays_df = nselib.trading_holiday_calendar()  # Get the DataFrame from nselib

    # Convert 'tradingDate' to datetime.date
    holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'], format='%d-%b-%Y').dt.date
    
    # Convert 'tradingDate' column to list for easy comparison
    holidays = holidays_df['tradingDate'].tolist()

    # Check if today is a weekend or a holiday
    if today.weekday() >= 5 or today in holidays:
        return False
    return True

# Test the function with a specific date
now = datetime.now()
print(f"Is today ({now}) a business day? {is_business_day(now)}")
