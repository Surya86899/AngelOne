# package import statement
from SmartApi import SmartConnect
import pyotp
from logzero import logger
from headers import headers

def my_login(api_key, username, pwd):
    smartApi = SmartConnect(api_key)

    try:
        token = "TCLINC5Z7VAZCVKJ4Y2FYRIVPE"
        totp = pyotp.TOTP(token).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    correlation_id = "abcde"
    data = smartApi.generateSession(username, pwd, totp)

    if data['status'] == False:
        logger.error(data)
    else:
        # login api call
        logger.info(f"You Credentials: {data}")
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        
        # Update the Authorization header with the received JWT token
        headers['Authorization'] = f'{authToken}'

        # Save the modified headers back to the headers.py file
        with open('headers.py', 'w') as file:
            file.write('headers = ' + str(headers))

