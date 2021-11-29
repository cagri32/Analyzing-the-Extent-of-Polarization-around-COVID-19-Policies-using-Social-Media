import json
import os
from dotenv import load_dotenv

load_dotenv()

with open('api_keys.json', 'w') as outfile:
    json.dump({
    "consumer_key":os.getenv('CONSUMER_KEY'),
    "consumer_secret":os.getenv('CONSUMER_SECRET'),
    "access_token":os.getenv('OAUTH_TOKEN'),
    "access_token_secret":os.getenv('OAUTH_TOKEN_SECRET')
     }, outfile)