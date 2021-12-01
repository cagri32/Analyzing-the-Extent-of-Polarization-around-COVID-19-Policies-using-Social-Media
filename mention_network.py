
import time
startTime = time.time()

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import ast
import operator

import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('OAUTH_TOKEN'), os.getenv('OAUTH_TOKEN_SECRET'))
api = tweepy.API(auth)

path_to_data = './data/'

# can't find this csv file
file = 'tweets/2021-07-01/2021-07-01-hydrated_tweets.csv'

def get_users(tweets_final):
    tweets_final["screen_name"] = tweets["user"].apply(lambda x: ast.literal_eval(x)["screen_name"])
    tweets_final["user_id"] = tweets["user"].apply(lambda x: ast.literal_eval(x)["id"])
    return tweets_final

def get_usermentions(tweets_final):
    tweets_final["user_mentions_screen_name"] = tweets["entities"].apply(lambda x: ast.literal_eval(x)["user_mentions"][0]["screen_name"] if ast.literal_eval(x)["user_mentions"] else np.nan)
    tweets_final["user_mentions_id"] = tweets["entities"].apply(lambda x: ast.literal_eval(x)["user_mentions"][0]["id"] if ast.literal_eval(x)["user_mentions"] else np.nan)
   
    return tweets_final

def network_from_source_and_destination_nodes(source_nodes, destination_nodes, network_type='mention'):
    edges = pd.concat([source_nodes,destination_nodes], axis=1)
    if (network_type == 'mention'):
        edges.dropna(subset=['user_mentions_id'], inplace=True)
    else:
        edges.dropna(subset=['retweeted_status'], inplace=True) # TODO - test for correctness

    return nx.from_pandas_edgelist(edges, 'user_mentions_id', 'user_id')

def export_graph_to_pickle(graph, filename):
    nx.write_gpickle(graph, filename)

def export_graph_to_gephi_gml(graph, filename):
    nx.write_gml(graph, filename)

def read_pickle_file(filename):
    return nx.read_gpickle(filename)

def get_screen_name_by_user_id(id):
    user = {}
    try: 
        print(f'{id}\t{type(id)}')
        user = api.get_user(user_id=id)
    except:
        user = tweets_for_graph['user_id'].loc[tweets_for_graph['user_id'] == id]
        print(user)
        print(f'user not found. loading from csv: {user}')
    return user.screen_name if 'screen_name' in user else -1


tweets = pd.read_csv(f'{path_to_data}{file}')
preprocessed_tweets = pd.DataFrame(columns = ["created_at", "id", "in_reply_to_screen_name", "in_reply_to_status_id", "in_reply_to_user_id",
                                      "retweeted_id", "retweeted_screen_name", "user_mentions_screen_name", "user_mentions_id", 
                                       "text", "user_id", "screen_name", "followers_count"])

print('get_usermentions')                                    
tweets_for_graph = get_usermentions(preprocessed_tweets)

print('get_users')                                    
tweets_for_graph = get_users(preprocessed_tweets)

print('writing to csv')
tweets_for_graph.to_csv('tweets_for_graph.csv')

print('network_from_source_and_destination_nodes')
g = network_from_source_and_destination_nodes(tweets_for_graph['user_mentions_id'], tweets_for_graph['user_id'])
print(g)

print('exporting graph to gephi gml file')
export_graph_to_gephi_gml(g, '2021-07-01-hydrated_tweets.mention_network.gml')

print('\nexporting graph to gpickle file')
export_graph_to_pickle(g, '2021-07-01-hydrated_tweets.mention_network.gpickle')

mention_network = read_pickle_file('./data/tweets/2021-07-01/2021-07-01-hydrated_tweets.mention_network.gpickle')
edge_betweenness_mention_network = pd.DataFrame.from_dict(nx.edge_betweenness_centrality(mention_network, k=10), orient='index').sort_values(by=[0], ascending=False)
top20 = edge_betweenness_mention_network.head(n=20)

pagerank_mention_network = pd.DataFrame.from_dict(nx.pagerank(mention_network), orient='index', columns=['pagerank_score'])
top50_most_important_authors = pagerank_mention_network.sort_values(by=['pagerank_score'], ascending=False).head(n=50)

print(f'top20:\n{top20}')
print(f'top50_most_important_authors:\n{top50_most_important_authors}')

executionTime = (time.time() - startTime)
print(f'\nExecution time in seconds: {str(executionTime)}')