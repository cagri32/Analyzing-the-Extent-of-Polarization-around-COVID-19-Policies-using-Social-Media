import json
import tweepy

import os
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('OAUTH_TOKEN'), os.getenv('OAUTH_TOKEN_SECRET'))
api = tweepy.API(auth)

def get_single_tweet(index):
    with open('./sample-data/sample_data.json', 'r') as tweets:
        data=tweets.readlines()

    single_tweet = json.loads(data[index])

    return single_tweet

def create_node(tweet):
    node = {
        'id': tweet.id,
        'retweeted': tweet.retweeted,
        'user.id': tweet.user.id,
        'user.screen_name': tweet.user.screen_name,
        'entities.user_mentions': tweet.entities['user_mentions']
    }
    return node

def get_screen_name_by_user_id(user_id):
    user = api.get_user(user_id=retweeters[0])
    return user.screen_name

single_tweet = get_single_tweet(1)
tweet = api.get_status(single_tweet['id_str'])

node = create_node(tweet)
print(f'node: {node}')

retweeters = api.get_retweeter_ids(single_tweet['id_str'])
print(f'retweeters: {retweeters}')

expected = 'abdulmshaheed'
actual = get_screen_name_by_user_id(retweeters[0])
print(f'\nTEST: check if retweeter id matches screenname\n\tExpected: {expected}\tActual: {actual}\n\tPASS: {expected ==actual}')