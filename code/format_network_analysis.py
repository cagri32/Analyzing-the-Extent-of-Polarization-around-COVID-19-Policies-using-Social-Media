import time
import pandas as pd
import ast
import tweepy
import os
from dotenv import load_dotenv

def export_dataframe_to_csv(dataframe, filename):
    csv_prefix_exists = filename.split('.')[-1] == 'csv'
    dataframe.to_csv(filename if csv_prefix_exists else f'{filename}.csv')

def format_pagerank(pagerank_dataframe, tweets_dataframe, tweepy_api, top_n, filename):
    pagerank_dataframe.columns = ['user', 'pagerank_score']
    formatted = pd.DataFrame(columns=['screen_name', 'pagerank_score'])
    formatted['screen_name'] = pagerank_dataframe["user"].head(n=top_n).apply(lambda x: get_screen_name_by_user_id(x, tweets_dataframe, tweepy_api))
    formatted['pagerank_score'] = pagerank_dataframe['pagerank_score'].head(n=top_n)
    export_dataframe_to_csv(formatted, filename)
    print(f'{filename}:\n{formatted}\n')

def format_centrality(centrality_dataframe, tweets_dataframe, tweepy_api, top_n, filename):
    print(f'pagerank_dataframe\n{centrality_dataframe}')
    centrality_dataframe.columns = ['edge', 'centrality_score']
    formatted = pd.DataFrame(columns=['formatted_edge', 'centrality_score'])
    formatted['formatted_edge'] = centrality_dataframe["edge"].head(n=top_n).apply(lambda x: [get_screen_name_by_user_id(user, tweets_dataframe, tweepy_api) for user in ast.literal_eval(x)])
    formatted['centrality_score'] = centrality_dataframe['centrality_score'].head(n=top_n)
    export_dataframe_to_csv(formatted, filename)
    print(f'{filename}:\n{formatted}\n')

def get_screen_name_by_user_id(id, tweets, tweepy_api):
    user = ''  
    try: 
        user = tweepy_api.get_user(user_id=int(id)).screen_name

    except:
        user = tweets.loc[tweets['user_mentions_id'] == id]['user_mentions_screen_name'].iat[0] 
    
    return user

def main():

    absolute_path_cwd = os.getcwd()
    cwd = absolute_path_cwd.split('/')[-1] if len(absolute_path_cwd.split('\\')) == 1 else absolute_path_cwd.split('\\')[-1]
    
    repo = 'Analyzing-the-Extent-of-Polarization-around-COVID-19-Policies-using-Social-Media'
    execution_path = 'code'
    
    try:
        proper_path = f'Please, run this script in the proper path "./{repo}/{execution_path}/"'
        assert (cwd == 'code'), proper_path
        
        load_dotenv()

        auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
        auth.set_access_token(os.getenv('OAUTH_TOKEN'), os.getenv('OAUTH_TOKEN_SECRET'))
        api = tweepy.API(auth)

        date = '2021-01-27'
        date = '2020-12-21'
        date = '2021-07-01' 
        graph_type = 'mention'

        path_to_data = '../data/'
        path_to_network_analysis = f'{path_to_data}network_analysis/{date}/'
        path_to_preprocessed_dataframe = f'{path_to_data}preprocessed_dataframes/'
        path_to_formatted_network_analysis = f'{path_to_network_analysis}formatted/'
        preprocessed_dataframe = f'{date}.tweets_for_graph.csv'
        relative_path_to_preprocessed_dataframe = f'{path_to_preprocessed_dataframe}{preprocessed_dataframe}'

        gcc_community_1_pagerank_file = f'{date}.gcc_network.community_1.{graph_type}.pagerank.csv'
        gcc_community_2_pagerank_file = f'{date}.gcc_network.community_2.{graph_type}.pagerank.csv'
        relative_path_gcc_community_1_pagerank = f'{path_to_network_analysis}{gcc_community_1_pagerank_file}'
        relative_path_gcc_community_2_pagerank = f'{path_to_network_analysis}{gcc_community_2_pagerank_file}'

        gcc_community_1_centrality_file = f'{date}.gcc_network.community_1.{graph_type}.edge_betweenness_centrality.csv'
        gcc_community_2_centrality_file = f'{date}.gcc_network.community_2.{graph_type}.edge_betweenness_centrality.csv'
        relative_path_to_gcc_community_1_centrality = f'{path_to_network_analysis}{gcc_community_1_centrality_file}'
        relative_path_to_gcc_community_2_centrality = f'{path_to_network_analysis}{gcc_community_2_centrality_file}'

        gcc_community_1_pagerank = pd.read_csv(relative_path_gcc_community_1_pagerank)
        gcc_community_2_pagerank = pd.read_csv(relative_path_gcc_community_2_pagerank)

        gcc_community_1_centrality = pd.read_csv(relative_path_to_gcc_community_1_centrality)        
        gcc_community_2_centrality = pd.read_csv(relative_path_to_gcc_community_2_centrality)

        tweets_for_graph = pd.read_csv(relative_path_to_preprocessed_dataframe) 

        print(f'path_to_formatted_network_analysis: {path_to_formatted_network_analysis}')
        path_to_formatted_network_analysis_exists = os.path.exists(path_to_formatted_network_analysis)
        if not path_to_formatted_network_analysis_exists:
            os.mkdir(path_to_formatted_network_analysis)
            
        format_pagerank(gcc_community_1_pagerank, tweets_for_graph, api, 10, f'{path_to_formatted_network_analysis}{gcc_community_1_pagerank_file}')
        format_pagerank(gcc_community_2_pagerank, tweets_for_graph, api, 10, f'{path_to_formatted_network_analysis}{gcc_community_2_pagerank_file}')
        format_centrality(gcc_community_1_centrality, tweets_for_graph, api, 10, f'{path_to_formatted_network_analysis}{gcc_community_1_centrality_file}')
        format_centrality(gcc_community_2_centrality, tweets_for_graph, api, 10, f'{path_to_formatted_network_analysis}{gcc_community_2_centrality_file}')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    startTime = time.time()
    main()
    executionTime = (time.time() - startTime)
    print(f'\nExecution time in seconds: {str(executionTime)}')    