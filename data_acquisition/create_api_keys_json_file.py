import json
import tweepy
from tweepy import OAuthHandler
import os
from dotenv import load_dotenv

load_dotenv()

#Creates a JSON Files with the API credentials
with open('api_keys.json', 'w') as outfile:
    json.dump({
    "consumer_key":os.getenv('CONSUMER_KEY'),
    "consumer_secret":os.getenv('CONSUMER_SECRET'),
    "access_token":os.getenv('OAUTH_TOKEN'),
    "access_token_secret":os.getenv('OAUTH_TOKEN_SECRET')
     }, outfile)

#The lines below are just to test if the twitter credentials are correct
# Authenticate
#auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)

#api = tweepy.API(auth, wait_on_rate_limit=True,
#				   wait_on_rate_limit_notify=True)

#if (not api):
#    print ("Can't Authenticate")
#    sys.exit(-1)