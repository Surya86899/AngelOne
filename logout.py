import requests
from headers import headers 

def my_logout():
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/logout"

    payload = {
        "clientcode": "K423710"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")