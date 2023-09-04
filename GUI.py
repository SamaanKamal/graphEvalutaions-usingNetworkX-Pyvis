from tkinter import *
import networkx as nx
from networkx.algorithms import community
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import csv
from pyvis import network as net
from IPython.core.display import HTML
from IPython.display import display
import itertools

# Read nodes from the CSV file
with open('metadata_primaryschool_Nodes.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)
    nodes = [(int(row[0]), {'Class': row[1], 'Gender': row[2]})
             for row in reader]

# Read edges from the CSV file
with open('primaryschool_Edges.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    edges = [(int(row[0]), int(row[1])) for row in reader]

# to get nodes and edges fom csv
# G = nx.Graph()
# G.add_nodes_from(nodes)
# G.add_edges_from(edges)

# create html page with size 500 * 70% with name Zachary’s Karate Club graph and menu and filter
g4 = net.Network(height='500px', width='70%',
                 select_menu=True,
                 filter_menu=True, neighborhood_highlight=True)

# dataset karate_club_graph
G = nx.karate_club_graph()

# Run the Girvan Newman algorithm
comp = community.girvan_newman(G)
# girvan_newman = community.girvan_newman(G)

k = 3
# number of communitis = k+1
for communities in itertools.islice(comp, k):
    comm = tuple(sorted(c) for c in communities)
print(comm)
i = 0
communities = dict()
for c in comm:
    for j in c:
        communities[j] = i+1
    i = i + 1
# scale to change the sizes
scale = 5  # Scaling the size of the nodes by 10*degree
# tp get degree for each node to dict and * by scale
d = dict(G.degree)

# Updating dict
d.update((x, scale*y) for x, y in d.items())
# Setting up size attribute to filter on size
nx.set_node_attributes(G, d, 'size')

betweenness_centrality = nx.betweenness_centrality(G, None, False, None)
closeness_centrality = nx.closeness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)
pagerank = nx.pagerank(G)

nx.set_node_attributes(G, betweenness_centrality, 'betweenness_centrality')
nx.set_node_attributes(G, closeness_centrality, 'closeness_centrality')
nx.set_node_attributes(G, eigenvector_centrality, 'eigenvector_centrality')
nx.set_node_attributes(G, communities, 'community')
nx.set_node_attributes(G, pagerank, 'pagerank')

# g4.from_nx(G)
i = 0

for node in G.nodes(data=True):
    g4.add_node(i, label=str(node[0]), size=node[1]["size"], betweenness_centrality=node[1]["betweenness_centrality"],
                eigenvector_centrality=node[1]["eigenvector_centrality"],
                closeness_centrality=node[1]["closeness_centrality"],
                community=node[1]["community"], pagerank=node[1]["pagerank"])
    i = i+1
g4.from_nx(G)
g4.show_buttons(filter_=['physics'])
g4.write_html('karate.html', False, False)

# TODO: text to view the score of task community detection evaluations
# TODO: create table to view each score of task page rank
# TODO: ask shery is colab ok ?
