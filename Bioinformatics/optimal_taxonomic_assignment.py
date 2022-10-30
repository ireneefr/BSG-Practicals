##########################################################################
###   Obtain the optimal taxonomic assignment for each sequence read   ###
###   Author: Irene Fernández Rebollo                                  ###
###   Date: 25/10/2022                                                 ###
##########################################################################

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

# Optimal calculation for each sequence read
results = []
for x in reads.keys():
    # Load skeleton tree
    with open('%s_skeleton.pickle' % x, 'rb') as f:
        H = pickle.load(f)
    max_node = ''
    max_F = 0
    for node in H.nodes():
        # Calculate F_measure for each internal node
        if node not in reads[x]:
            TP = len(set(nx.descendants(H, node)).intersection(reads[x]))
            FN = len(reads[x]) - TP
            descendants = 0
            for d in set(nx.descendants(G, node)):
                if G.out_degree(d) == 0:
                    descendants += 1
            FP = descendants - TP
            Precision = TP/(TP + FP)
            Recall = TP/(TP + FN)
            F_measure = 2/(1/Precision + 1/Recall)
            # Get the max F_measure
            if F_measure > max_F:
                max_F = F_measure
                max_node = node
    r = 'The optimal assignment of %s is %s with F_measure = %s' % (x, max_node, max_F)
    results.append(r)

# Save the optimal assignments
with open('optimal_assignments.txt', 'w') as f:
    f.write('\n'.join(results))
