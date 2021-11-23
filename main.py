import pandas as pd
from collections import Counter
import networkx as nx
import pickle


def main():
  graph = nx.DiGraph()

  columns = ['user_id', 'retweeted_user_id']
  df = pd.read_csv('hydrated_tweets.csv',usecols=columns)

  for row in df.itertuples(index=False):
    if row.retweeted_user_id != -1:
      graph.add_edge(row.user_id,str(row.retweeted_user_id))

  #print(graph.edges)
  print(graph)

  with open("graph.txt", 'wb') as f:
    pickle.dump(graph, f)

  #pickle.dump(graph, open('graph.txt', 'w'))

  return graph

if __name__ == "__main__":
    main()
