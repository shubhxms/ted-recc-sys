import networkx as nx
import pandas as pd
import ast
import matplotlib.pyplot as plt

df = pd.read_csv('final.csv')

df['related_talks'] = df['related_talks'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

edges = []
for i, related_talks in enumerate(df['related_talks']):
    for related_talk in related_talks:
        edges.append((df.at[i, 'id'], related_talk['id']))
G = nx.DiGraph()
G.add_nodes_from(df['id'])
G.add_edges_from(edges)

labels = {node: node for node in G.nodes()}

pos = nx.spring_layout(G, k=0.15, iterations=20)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, labels, font_size=10)
plt.axis('off')
plt.show()
