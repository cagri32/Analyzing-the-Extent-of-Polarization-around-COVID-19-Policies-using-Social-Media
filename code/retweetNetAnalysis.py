import glob
import pickle
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community.label_propagation import label_propagation_communities
import operator

date = "2020-10-02"
inputdir = 'D:\\..\\Project\\Dataset to be used\\{}\\**\\graph.txt'.format(date)
# Output graphs
maingraphdir = '.\\..\\Dataset to be used\\{}\\mainGraphUndirected.txt'.format(date)
community1dir = '.\\..\\Dataset to be used\\{}\\community1graph.txt'.format(date)
community2dir = '.\\..\\Dataset to be used\\{}\\community2graph.txt'.format(date)

graphlist = glob.glob(inputdir, recursive=True)

maingraph = nx.DiGraph()

print("Combining SubGraphs in the main folder")
for graph in graphlist:
    with open(graph, 'rb') as f:
        G_loaded = pickle.load(f)
        maingraph.update(G_loaded)
    print(G_loaded)
print()    
print("Main Graph is now a:")
print(maingraph)

# Working on undirected graphs provides more informative and accessible results
maingraphUnd = maingraph.to_undirected()

# Get the core graph. That is the graph with node degrees less than or equal to 2 are removed
unfrozen_graph = nx.Graph(maingraphUnd)
unfrozen_graph.remove_edges_from(nx.selfloop_edges(unfrozen_graph))
maingraphUnd = nx.k_core(unfrozen_graph, 2)

# Get the Giant Connected Component of the graph
Gcc = sorted(nx.connected_components(maingraphUnd), key=len, reverse=True)
mainGraphUndGcc = maingraphUnd.subgraph(Gcc[0])

print("\nGiant Connected Component")
print(mainGraphUndGcc)

# Dump Main Graph to a 
with open(maingraphdir, 'wb') as f:
    pickle.dump(mainGraphUndGcc, f)

print("\nCommunities found with Fluid Communities algorithm")
communities = community.asyn_fluidc(mainGraphUndGcc, 2)
result = [mainGraphUndGcc.subgraph(c) for c in communities]

# Community 1
community1 = result[0]
print("\nCommunity 1 Graph")
print(community1)

# Dump Community 1 to a file
with open(community1dir, 'wb') as f:
    pickle.dump(community1, f)
    
# Analysis of Community 1
print("\nDensity of Community 1")
print(nx.density(community1))
print()

# PageRank Scores of Community 1
prcommunity1=nx.pagerank(community1)
sortedprcommunity1 = dict(sorted(prcommunity1.items(), key=operator.itemgetter(1),reverse=True))

print("Top 10 in PageRank of Community 1 \n")
i = 0
for k in sortedprcommunity1:
    print("%s: %s" % (k,str(sortedprcommunity1[k])))
    i += 1
    if i >9: break
print()

# Edge betweenness score
print("Calculate edge betweenness score of Community 1")
betweennesscommunity1 = nx.edge_betweenness_centrality(community1, k=100)

print("20 most important edges based on edge betweenness score of Community 1 \n")
sortedbetweennesscommunity1 = dict(sorted(betweennesscommunity1.items(), key=operator.itemgetter(1),reverse=True))

i = 0
for k in sortedbetweennesscommunity1:
    print("%s: %s" % (k,sortedbetweennesscommunity1[k]))
    i += 1
    if i >19: break
print()


# Community 2
community2 = result[1]
print("Community 2 Graph")
print(community2)

# Dump Community 2 to a file
with open(community2dir, 'wb') as f:
    pickle.dump(community2, f)
    
# Analysis of Community 2    
print("\nDensity of Community 2")
print(nx.density(community2))
print()

# PageRank Scores of Community 2
prcommunity2=nx.pagerank(community2)
sortedprcommunity2 = dict(sorted(prcommunity2.items(), key=operator.itemgetter(1),reverse=True))

print("Top 10 in PageRank of Community 2 \n")
i = 0
for k in sortedprcommunity2:
    print("%s: %s" % (k,str(sortedprcommunity2[k])))
    i += 1
    if i >9: break
print()

# Edge betweenness scores
print("Calculate Edge Betweenness Score of Community 2")
betweennesscommunity2 = nx.edge_betweenness_centrality(community2, k=100)

print("20 most important edges based on edge betweenness score of Community 2 \n")
sortedbetweennesscommunity2 = dict(sorted(betweennesscommunity2.items(), key=operator.itemgetter(1),reverse=True))
i = 0
for k in sortedbetweennesscommunity2:
    print("%s: %s" % (k,sortedbetweennesscommunity2[k]))
    i += 1
    if i >19: break
print()

''''
Bridge Nodes ??? Nodes found on the border of communities 
can sometime act like a link, loosely interconnecting 
the two communities.

# print("Bridges")
# print(len(list(nx.bridges(mainGraphUndGcc))))
'''

'''
Density ??? More dense collection of nodes implies stronger 
interconnectivity. Sparsity implies weaker interconnectivity.

print("Density")
print(nx.density(mainGraphUndGcc))
'''

print("The biggest 6 communities by Label Propagation Algorithm")
communities1 = label_propagation_communities(mainGraphUndGcc)
sorted_communities1 = sorted(communities1, key=lambda x: len(x), reverse=True)
for communiti in sorted_communities1[:6]:
    #print(list(community)[:10])
    print(len(communiti))

'''
Modularity ??? A measure of clustering quality, 
how disconnected communities are with each other. 
???Highly modular networks are characterized by a few 
highly intraconnected clusters that are loosely interconnected. 
Networks where users are highly interconnected regardless 
of cluster affiliation are, therefore, less modular.???
'''
print("Modularity of GCC based on Fluid Community Detection")
print(community.modularity(mainGraphUndGcc, result))
print()


