from datetime import datetime
import pandas as pd
import numpy as np
import requests
import logging
import os
from dotenv import load_dotenv
import pyotp
from SmartAPI import SmartConnect
import datetime as dt

# Example purchase date
purchase_date = dt.datetime.strptime("2024-06-07", '%Y-%m-%d')

# Generate business date range
bdate_range = pd.bdate_range(start=purchase_date, periods=24)  # Get the next 24 business days
print(bdate_range)
if len(bdate_range) >= 24:
    max_holding_date = bdate_range[-1].date()  # Ensure it's a date object

# Get today's date
today = dt.datetime.now().date()

# Check if today's date is greater than or equal to the max holding date
if today >= max_holding_date:
    print("Sell")



