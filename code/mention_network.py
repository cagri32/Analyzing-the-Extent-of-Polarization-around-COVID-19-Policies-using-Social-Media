import time
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

def get_same_columns(preprocessed_tweets, hydrated_tweets):
    print(f'hydrated_tweets cols: {list(hydrated_tweets.columns)}')
    print(f'preprocessed_tweets cols: {list(preprocessed_tweets.columns)}')
    preprocessed_tweets['created_at'] = hydrated_tweets['created_at']
    preprocessed_tweets['id'] = hydrated_tweets['id']
    preprocessed_tweets['text'] = hydrated_tweets['text']
    print(preprocessed_tweets.head(n=3))

    return preprocessed_tweets

def get_users(preprocessed_tweets, hydrated_tweets):
    preprocessed_tweets["screen_name"] = hydrated_tweets["user"].apply(lambda x: ast.literal_eval(x)["screen_name"])
    preprocessed_tweets["user_id"] = hydrated_tweets["user"].apply(lambda x: ast.literal_eval(x)["id"])
    return preprocessed_tweets

def get_usermentions(preprocessed_tweets, hydrated_tweets):
    preprocessed_tweets["user_mentions_screen_name"] = hydrated_tweets["entities"].apply(lambda x: ast.literal_eval(x)["user_mentions"][0]["screen_name"] if ast.literal_eval(x)["user_mentions"] else np.nan)
    preprocessed_tweets["user_mentions_id"] = hydrated_tweets["entities"].apply(lambda x: ast.literal_eval(x)["user_mentions"][0]["id"] if ast.literal_eval(x)["user_mentions"] else np.nan)
    
    return preprocessed_tweets

def get_screen_name_by_user_id(id, tweets, tweepy_api):
    user = {}
    try: 
        print(f'{id}\t{type(id)}')
        user = tweepy_api.get_user(user_id=id)
    except:
        user = tweets['user_id'].loc[tweets['user_id'] == id]
        print(user)
        print(f'user not found. loading from csv: {user}')
    return user.screen_name if 'screen_name' in user else -1

def preprocess_hydrated_tweets(hydrated_tweets_csv, filename):
    print(f'Reading {hydrated_tweets_csv}')
    hydrated_tweets = pd.read_csv(hydrated_tweets_csv)
    preprocessed_tweets = pd.DataFrame(columns = ["created_at", "id", "in_reply_to_screen_name", "in_reply_to_status_id", "in_reply_to_user_id",
                                          "retweeted_id", "retweeted_screen_name", "user_mentions_screen_name", "user_mentions_id",
                                          "text", "user_id", "screen_name", "followers_count"])

    print('Getting user mentions')                                    
    tweets_for_graph = get_usermentions(preprocessed_tweets, hydrated_tweets)

    print('Getting users')                                    
    tweets_for_graph = get_users(preprocessed_tweets, hydrated_tweets)

    print(f'Writing preprocessed tweets to {filename}.csv')
    export_dataframe_to_csv(tweets_for_graph, filename)


def create_graphs(tweets, dataset_date, type='mention'):
    graphs = {}

    source = 'user_id'
    destination = 'user_mentions_id' if type == 'mention' else 'retweet_status'
    
    network_name = f'{dataset_date}.network.{type}'
    gcc_network_name = f'{dataset_date}.gcc_network.{type}'
    core_network_name = f'{dataset_date}.core_network.{type}'
    weighted_network_name = f'{dataset_date}.weighted_network.{type}'

    graphs[network_name] = graph(tweets, source, destination)
    graphs[gcc_network_name] = giant_connected_component(graphs[network_name])
    graphs[core_network_name] = core_graph(graphs[gcc_network_name])
    graphs[weighted_network_name] = weighted_graph(tweets, source, destination)

    return graphs

def export_graph_to_pickle(graph, filename):
    nx.write_gpickle(graph, f'{filename}.gpickle')
    print(f'export_graph_to_pickle: Exported graph "{filename}" to gpickle..')

def export_graph_to_gephi_gml(graph, filename):
    nx.write_gml(graph, f'{filename}.gml')
    print(f'export_graph_to_gephi_gml: Exported graph "{filename}" to gml..')

def export_dataframe_to_csv(dataframe, filename):
    csv_prefix_exists = filename.split('.')[-1] == 'csv'
    dataframe.to_csv(filename if csv_prefix_exists else f'{filename}.csv')

# TODO - export_network_analysis after doing network analysis
def export_network_analysis(graphs, output_dir):
    for graph_name, graph in graphs.items():
        print(f'{graph_name}: {graph}')
        # TODO - check if network analysis exists before running & exporting network analysis
        export_dataframe_to_csv(top_n_edge_betweenness_centrality(graph), f'{output_dir}{graph_name}.edge_betweenness_centrality')
        export_dataframe_to_csv(top_n_pagerank(graph), f'{output_dir}{graph_name}.pagerank')

def export_graphs(graphs, output_dir):
    for graph_name, graph in graphs.items():
        export_graph_to_pickle(graph, f'{output_dir}{graph_name}')
        export_graph_to_gephi_gml(graph, f'{output_dir}{graph_name}')

def graph(tweets, source, destination, network_type='mention'):
    edges = pd.concat([tweets[source],tweets[destination]], axis=1)
    if (network_type == 'mention'):
        edges.dropna(subset=['user_mentions_id'], inplace=True)
    else:
        edges.dropna(subset=['retweeted_status'], inplace=True) # TODO - test for correctness

    return nx.from_pandas_edgelist(edges, 'user_mentions_id', 'user_id')

def read_pickle_file(filename):
    return nx.read_gpickle(filename)

def giant_connected_component(graph):
  return graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0])

def weighted_graph(tweets, source, destination):
  network_edges = pd.concat([tweets[source], tweets[destination]], axis=1)
  network_weighted_edges = (network_edges.groupby([source,destination]).size().reset_index().rename(columns={0 : 'weight'}))
  print(f'network_weighted_edges:\n{network_weighted_edges.shape}\n{network_weighted_edges}')
  weighted_graph = nx.from_pandas_edgelist(network_weighted_edges, source, destination, ['weight'])
  return weighted_graph  

def core_graph(graph):
  node_degree_pairs = graph.degree()
  subgraph_nodes = list()
  
  for (node, degree) in node_degree_pairs:
    if degree >= 3:
      subgraph_nodes.append(node)

  return graph.subgraph(subgraph_nodes)

def top_n_edge_betweenness_centrality(network, top_n=20):
    edge_betweenness_network = pd.DataFrame.from_dict(nx.edge_betweenness_centrality(network, k=10), orient='index').sort_values(by=[0], ascending=False)
    return edge_betweenness_network.head(n=top_n)

def top_n_pagerank(network, top_n=50):
    pagerank_mention_network = pd.DataFrame.from_dict(nx.pagerank(network), orient='index', columns=['pagerank_score'])
    return pagerank_mention_network.sort_values(by=['pagerank_score'], ascending=False).head(n=top_n)

# TODO - test that graph.subgraph(c) works
def community_detection(graph, num_communities=2):
    iterable_of_communities = nx.algorithms.community.asyn_fluid.asyn_fluidc(graph, num_communities)
    # communities_as_sets_of_nodes = [c for c in iterable_of_communities]
    communities_as_graphs = [graph.subgraph(c) for c in iterable_of_communities]
    # communities_as_graphs = []
    # for c in iterable_of_communities:
    #     sub = graph.subgraph(c)
    #     print(f'sub: {sub}')
    #     communities_as_graphs.append(sub)
    return communities_as_graphs

def main():
    load_dotenv()

    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('OAUTH_TOKEN'), os.getenv('OAUTH_TOKEN_SECRET'))
    api = tweepy.API(auth)

    # TODO - pass in date as an argument or a list of dates
    # date = '2021-07-01' # EXPORTED
    date = '2021-01-27' # EXPORTED
    # date = '2020-12-21' # EXPORTED
    # date = '2020-07-13' # EXPORTED
    # date = '2020-10-02'

    path_to_data = '../data/'
    path_to_hydrated_tweets = f'{path_to_data}tweets/{date}/'
    path_to_preprocessed_dataframe = f'{path_to_data}preprocessed_dataframes/'
    path_to_graph_exports = f'{path_to_data}graph_exports/{date}/'
    path_to_network_analysis = f'{path_to_data}network_analysis/{date}/'

    # hydrated_tweets = f'{date}-hydrated_tweets.csv'
    hydrated_tweets = f'{date}-clean_hydrated_tweets.csv'
    preprocessed_dataframe = f'{date}.tweets_for_graph.csv'

    relative_path_to_hydrated_tweets = f'{path_to_hydrated_tweets}{hydrated_tweets}'
    relative_path_to_preprocessed_dataframe = f'{path_to_preprocessed_dataframe}{preprocessed_dataframe}'

    preprocessed_tweets_exist = os.path.exists(relative_path_to_preprocessed_dataframe)
    print(f'relative_path_to_preprocessed_dataframe: {relative_path_to_preprocessed_dataframe}')

    absolute_path_cwd = os.getcwd()
    cwd = absolute_path_cwd.split('/')[-1] if len(absolute_path_cwd.split('\\')) == 1 else absolute_path_cwd.split('\\')[-1]
    
    repo = 'Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media'
    execution_path = 'code'
    
    try:
        proper_path = f'Please, run this script in the proper path "./{repo}/{execution_path}/"'
        assert (cwd == 'code'), proper_path
        
        print(f'Running network analysis on {hydrated_tweets}')

        if not preprocessed_tweets_exist:
            print('Preprocessing hydrated tweets')
            preprocess_hydrated_tweets(relative_path_to_hydrated_tweets, relative_path_to_preprocessed_dataframe)
        
        graph_type = 'mention'

        relative_path_to_network = f'{path_to_graph_exports}{date}.network.{graph_type}.gpickle'
        relative_path_to_gcc_network = f'{path_to_graph_exports}{date}.gcc_network.{graph_type}.gpickle'
        relative_path_to_core_network = f'{path_to_graph_exports}{date}.core_network.{graph_type}.gpickle'
        relative_path_to_weighted_network = f'{path_to_graph_exports}{date}.weighted_network.{graph_type}.gpickle'

        print(f'path_to_graph_exports: {path_to_graph_exports}')
        path_to_graph_exports_exists = os.path.exists(path_to_graph_exports)
        if not path_to_graph_exports_exists:
            os.mkdir(path_to_graph_exports)

        exported_graphs_exist = os.path.exists(relative_path_to_network) and \
            os.path.exists(relative_path_to_gcc_network) and \
            os.path.exists(relative_path_to_core_network) and \
            os.path.exists(relative_path_to_weighted_network)

        if not exported_graphs_exist:
            print('Reading dataframe csv')
            tweets_for_graph = pd.read_csv(relative_path_to_preprocessed_dataframe) 
            print('Creating graphs')
            all_mention_networks = create_graphs(tweets_for_graph, date, graph_type)
            print('Exporting graphs')
            export_graphs(all_mention_networks, path_to_graph_exports)
        else:
            all_mention_networks = {
                f'{date}.network.{graph_type}': read_pickle_file(relative_path_to_network), 
                f'{date}.gcc_network.{graph_type}': read_pickle_file(relative_path_to_gcc_network), 
                f'{date}.core_network.{graph_type}': read_pickle_file(relative_path_to_core_network), 
                f'{date}.weighted_network.{graph_type}': read_pickle_file(relative_path_to_weighted_network), 
            }

        path_to_network_analysis_exists = os.path.exists(path_to_network_analysis)
        print(f'path_to_network_analysis: {path_to_network_analysis}\nexists: {not path_to_network_analysis_exists}')
        if not path_to_network_analysis_exists:
            os.mkdir(path_to_network_analysis)
        
        # TODO - check if network analysis exists before running & exporting network analysis

        print('Mention Networks (node & edge info)')
        export_network_analysis(all_mention_networks, path_to_network_analysis)
        # for graph_name, graph in all_mention_networks.items():
        #     print(f'{graph_name}: {graph}')
        #     # TODO - check if network analysis exists before running & exporting network analysis
        #     export_dataframe_to_csv(top_n_edge_betweenness_centrality(graph), f'{path_to_network_analysis}{graph_name}.edge_betweenness_centrality')
        #     export_dataframe_to_csv(top_n_pagerank(graph), f'{path_to_network_analysis}{graph_name}.pagerank')

        gcc = all_mention_networks[f'{date}.gcc_network.{graph_type}']
        communities_as_graphs = community_detection(gcc, 2)
        communities = {f'{date}.gcc_network.community_{c+1}.{graph_type}': communities_as_graphs[c] for c in range(len(communities_as_graphs))}
        export_graphs(communities, path_to_network_analysis)
        export_network_analysis(communities, path_to_network_analysis)

        # TODO - check if communities exports exist
        # community_1 = read_pickle_file(f'{path_to_network_analysis}{date}.gcc_network.community_1.{graph_type}.gpickle')
        # community_2 = read_pickle_file(f'{path_to_network_analysis}{date}.gcc_network.community_2.{graph_type}.gpickle')

        # for graph_name, graph in communities.items():
        #     print(f'{graph_name}: {graph}')
        #     # TODO - check if network analysis exists before running & exporting network analysis
        #     export_dataframe_to_csv(top_n_edge_betweenness_centrality(graph), f'{path_to_network_analysis}{graph_name}.edge_betweenness_centrality')
        #     export_dataframe_to_csv(top_n_pagerank(graph), f'{path_to_network_analysis}{graph_name}.pagerank')

        mod = nx.algorithms.community.quality.modularity(gcc, communities_as_graphs)
        print(f'mod: {mod}')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    startTime = time.time()
    main()
    executionTime = (time.time() - startTime)
    print(f'\nExecution time in seconds: {str(executionTime)}')