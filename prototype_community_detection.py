import networkx as nx

data_path = './data/'

def main():
    #Test Load
    graph = nx.read_gpickle(
        f'{data_path}2021-07-01-hydrated_tweets.mention_network.gpickle')
    print(graph)

    #Analysis
    
    # To review and consider in the meantime:
    # https://networkx.org/documentation/stable/reference/algorithms/community.html
    

if __name__ == "__main__":
    main()
    print("prototype_community_detection.py... Done.")
