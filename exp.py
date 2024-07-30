from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
api_key = os.getenv('API_KEY')
pwd = os.getenv('PWD')
username = os.getenv('USERNAME')
token = os.getenv('TOKEN')
email_pass = os.getenv('EMAIL_PASS')

# Print or use these variables as needed
print(f"API Key: {api_key}")
print(f"Password: {pwd}")
print(f"Username: {username}")
print(f"Token: {token}")
print(f"Token: {email_pass}")

print(type(api_key))
print(type(pwd))
print(type(username))
print(type(token))
print(type(email_pass))

