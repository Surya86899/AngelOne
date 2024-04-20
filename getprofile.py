import requests
import json
from headers import headers

def profile():
    url = 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getProfile'

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        print(json.dumps(response_data, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")
