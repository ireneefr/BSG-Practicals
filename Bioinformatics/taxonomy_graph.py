####################################################
###   Generate a Taxonomy Graph from nodes.dmp   ###
###   Author: Irene Fernández Rebollo            ###
###   Date: 11/10/2022                           ###
####################################################

# Required libraries
import networkx as nx
import matplotlib.pyplot as plt
import pickle

# Create Taxonomy Directed Graph
G = nx.DiGraph()
with open("nodes.dmp", 'r') as f:
    for line in f:
        l = line.split("\t|\t")
        G.add_node(l[0], rank = l[2])
        G.add_edge(l[1], l[0])
G.remove_edge("1", "1") #1 is the root

# Generate a plot of the top of the graph (optional)
#top_nodes = ["1", "131567", "2759", "10239", "2", "2157"]
#G_sub = G.subgraph(top_nodes)
#pos = nx.nx_agraph.graphviz_layout(G_sub, prog="dot", args="")
#plt.figure(figsize=(10, 10))
#nx.draw_networkx(G_sub, pos, node_size=2500, alpha=0.6, node_color="blue",
#                 with_labels=True, arrowsize = 5)
#plt.savefig("Graph_taxonomy_top.png", format="PNG")

# Only keep nodes with standard ranks
print(G)
ranks = nx.get_node_attributes(G, "rank")
standard_ranks = ["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
for i in ranks.keys():
    if i != "1":
        if ranks[str(i)] not in standard_ranks:
            parent = next(G.predecessors(str(i)))
            nx.contracted_nodes(G, str(parent), str(i), self_loops= False, copy=False)

# Save graph object to file
pickle.dump(G, open('taxonomy.pickle', 'wb'))