# Edge Betweennes

import glob
import pickle
import networkx as nx
import operator
import sys

# Date to analyze
date = "2021-01-27"

# Input graphs directory
maingraphdir = '.\\{}\\mainGraphUndirected.txt'.format(date)

# Output Edge Betweenness
edgeBetweennessOut = '.\\{}\\edgeBetweenness.txt'.format(date)
sys.stdout = open(edgeBetweennessOut, "w")

maingraph = nx.DiGraph()

graphlist = glob.glob(maingraphdir, recursive=True)
print("Combining SubGraphs in the main folder")
for graph in graphlist:
    with open(graph, 'rb') as f:
        G_loaded = pickle.load(f)
        maingraph.update(G_loaded)
    print(G_loaded)

print("\nMain Graph is now a:")
print(maingraph)

# Edge betweenness score
print("Calculate edge betweenness score of Main Graph")
betweennessmaingraph = nx.edge_betweenness_centrality(maingraph, k=100)

print("20 most important edges based on edge betweenness score of Main Graph \n")
sortedbetweennessmaingraph = dict(sorted(betweennessmaingraph.items(), key=operator.itemgetter(1),reverse=True))

i = 0
for k in sortedbetweennessmaingraph:
    print("'%s': %s" % (k,sortedbetweennessmaingraph[k]))
    i += 1
    if i >19: break
print()


sys.stdout.close()
