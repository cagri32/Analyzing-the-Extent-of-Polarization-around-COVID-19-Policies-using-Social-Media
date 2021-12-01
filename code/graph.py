import glob
import pickle
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community.label_propagation import label_propagation_communities
from multiprocessing import Pool
import itertools
import operator


graphlist = glob.glob('D:\\Users\\Cagri\\Desktop\\YORK\\4414\\Project\\Dataset to be used\\2020-12-21\\**\\graph.txt', recursive=True)

maingraph = nx.DiGraph()

for graph in graphlist:
    with open(graph, 'rb') as f:
        G_loaded = pickle.load(f)
        maingraph.update(G_loaded)
    print(G_loaded)
print()    
print("Main Graph is now a:")
print(maingraph)

maingraphUnd = maingraph.to_undirected()

Gcc = sorted(nx.connected_components(maingraphUnd), key=len, reverse=True)
mainGraphUndGcc = maingraphUnd.subgraph(Gcc[0])
print()
print("Gcc")
print(mainGraphUndGcc)

print()
print("Communities found with Fluid Communities algorithm")
communities = community.asyn_fluidc(mainGraphUndGcc, 2)
result = [mainGraphUndGcc.subgraph(c) for c in communities]
community1 = result[0]
print()
print("Community 1")
print(result[0])
print()
print("Density of Community 1")
print(nx.density(community1))
print()

with open('\\Dataset to be used\\2020-12-21\\community1graph.txt', 'wb') as f:
    pickle.dump(community1, f)

prcommunity1=nx.pagerank(community1)
sortedprcommunity1 = dict(sorted(prcommunity1.items(), key=operator.itemgetter(1),reverse=True))

print("Top 10 in PageRank of Community 1 \n")
i = 0
for k in sortedprcommunity1:
    print("%s: %s" % (k,str(sortedprcommunity1[k])))
    i += 1
    if i >9: break
print()

# Calculate edge betweenness score
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

print("Modularity of Community 1")
print(community.modularity(community1, result))
print()

community2 = result[1]
print("Community 2")
print(community2)
print()
print("Density of Community 2")
print(nx.density(community2))
print()
with open('\\Dataset to be used\\2020-12-21\\community2graph.txt', 'wb') as f:
    pickle.dump(community2, f)

prcommunity2=nx.pagerank(community2)
sortedprcommunity2 = dict(sorted(prcommunity2.items(), key=operator.itemgetter(1),reverse=True))

print("Top 10 in PageRank of Community 2 \n")
i = 0
for k in sortedprcommunity2:
    print("%s: %s" % (k,str(sortedprcommunity2[k])))
    i += 1
    if i >9: break
print()

# Calculate edge betweenness score
print("Calculate Edge Betweenness Score of Community 2")
betweennesscommunity2 = nx.edge_betweenness_centrality(community2, k=100)

print("20 most important edges based on edge betweenness score of Community 2 \n")
sortedbetweennesscommunity2 = dict(sorted(betweennesscommunity2.items(), key=operator.itemgetter(1),reverse=True))
i = 0
for k in sortedbetweennesscommunity2:
    print("%s: %s" % (k,sortedbetweennesscommunity2[k]))
    i += 1
    if i >9: break
print()

print("Modularity of Community 2")
print(community.modularity(community2, result))
print()
''''
Bridge Nodes — Nodes found on the border of communities 
can sometime act like a link, loosely interconnecting 
the two communities.
'''
# print("Bridges")
# print(len(list(nx.bridges(mainGraphUndGcc))))
# print()
'''
Density — More dense collection of nodes implies stronger 
interconnectivity. Sparsity implies weaker interconnectivity.
'''
# print("Density")
# print(nx.density(mainGraphUndGcc))
# print()


# print("The biggest 6 communities by Label Propagation Algorithm")
# communities1 = label_propagation_communities(mainGraphUndGcc)
# sorted_communities1 = sorted(communities1, key=lambda x: len(x), reverse=True)
# for communiti in sorted_communities1[:6]:
#     #print(list(community)[:10])
#     print(len(communiti))

'''
Modularity — A measure of clustering quality, 
how disconnected communities are with each other. 
“Highly modular networks are characterized by a few 
highly intraconnected clusters that are loosely interconnected. 
Networks where users are highly interconnected regardless 
of cluster affiliation are, therefore, less modular.”
'''
print("Modularity of GCC")
print(community.modularity(mainGraphUndGcc, result))
print()


