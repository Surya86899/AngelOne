from datetime import datetime, timedelta
import pandas as pd
import requests

def is_business_day(date: datetime.date):
    headers = {'user-agent': 'PostmanRuntime/7.26.5'}
    endpoint = "https://www.nseindia.com/api/holiday-master?type=trading"
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        holidays_json = response.json().get('FO', [])
        holidays_df = pd.DataFrame(holidays_json)
        holidays_df['tradingDate'] = pd.to_datetime(holidays_df['tradingDate'])
        return not(pd.Timestamp(date) in holidays_df['tradingDate'].values)
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching holiday data: {e}")
        return True

# Check if today is a holiday
print(is_business_day('2024-11-15'))

# print(datetime.now().date() + timedelta(days=3))
