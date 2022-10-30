########################################################################
###   Build the skeleton tree for each sequence read in sample.inp   ###
###   Author: Irene Fernández Rebollo                                ###
###   Date: 18/10/2022                                               ###
########################################################################

# Required libraries
import networkx as nx
import matplotlib.pyplot as plt
import pickle

# Load graph object from file
with open('taxonomy.pickle', 'rb') as f:
    G = pickle.load(f)

# Create a dictionary with the sequence reads
reads = {}
with open("sample.inp", 'r') as f:
    for line in f:
        l = line.split()
        reads[l[0]] = l[1:]

# Create skeleton trees for each sequence read
for x in reads.keys():
    H = nx.DiGraph()
    for i in reads[x]:
        # Add species nodes to the skeleton
        H.add_node(i)
        # Add edges with their predecessors
        while list(G.predecessors(i)) != []:
            parent = next(G.predecessors(i))
            H.add_edge(parent, i)
            i = parent
    # Delete unneecessary nodes
    for n in list(H.nodes()):
        if H.in_degree(n) == 1 and H.out_degree(n) == 1:
            parent = next(H.predecessors(n))
            nx.contracted_nodes(H, str(parent), n, self_loops= False, copy=False)
    # Save graph object to file
    with open('%s_skeleton.pickle' % x, 'wb') as f:
        pickle.dump(H, f)

    # Generate a plot of the skeleton tree (optional)
    #pos = nx.nx_agraph.graphviz_layout(H, prog="dot", args="")
    #plt.figure(figsize=(10, 10))
    #nx.draw_networkx(H, pos, node_size=2500, alpha=0.6, node_color="blue",
    #            with_labels=True, arrowsize = 5)
    #plt.savefig("%s_skeleton.png" % x, format="PNG")
    #plt.close()