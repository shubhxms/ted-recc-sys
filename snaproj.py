import networkx as nx
import pandas as pd
import ast
import matplotlib.pyplot as plt

df = pd.read_csv('final.csv')

df['related_talks'] = df['related_talks'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

edges = []
for i, related_talks in enumerate(df['related_talks']):
    if isinstance(related_talks, list):
        for related_talk in related_talks:
            edges.append((df.at[i, 'id'], related_talk['id']))

G = nx.DiGraph()

# add nodes for each talk
for i, row in df.iterrows():
    G.add_node(row['id'], name=row['talk_name'], speakers=row['speaker_name'], tags=row['talks_tags'])

# add edges between related talks
for i, related_talks in enumerate(df['related_talks']):
    if isinstance(related_talks, list):
        for related_talk in related_talks:
            edges.append((df.at[i, 'id'], related_talk['id']))

G.add_edges_from(edges)

# analyze the network structure
# degree centrality
degree_centrality = nx.degree_centrality(G)
top_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by degree centrality:")
for node, centrality in top_degree_centrality:
    if 'name' in G.nodes[node]:
        print(f"{G.nodes[node]['name']} ({node}) - {centrality:.3f}")
    else:
        print(f"Node {node} - {centrality:.3f}")

print("\n")
G.remove_nodes_from(list(nx.isolates(G)))

# betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)
top_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by betweenness centrality:")
for node, centrality in top_betweenness_centrality:
    if 'name' in G.nodes[node]:
        print(f"{G.nodes[node]['name']} ({node}) - {centrality:.3f}")
    else:
        print(f"Node {node} - {centrality:.3f}")

print("\n")
# closeness centrality
closeness_centrality = nx.closeness_centrality(G)
top_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by closeness centrality:")
for node, centrality in top_closeness_centrality:
    if 'name' in G.nodes[node]:
        print(f"{G.nodes[node]['name']} ({node}) - {centrality:.3f}")
    else:
        print(f"Node {node} - {centrality:.3f}")

print("\n")

# draw the network
# draw the graph
pos = nx.spring_layout(G, k=0.15, iterations=20)
nx.draw(G, pos, node_size=100, node_color='#336699', alpha=0.7, with_labels=False)
nx.draw_networkx_edges(G, pos, alpha=0.4)
nx.draw_networkx_labels(G, pos, labels={node: G.nodes[node]['name'] if 'name' in G.nodes[node] else str(node) for node in G.nodes()}, font_size=8)
plt.show()

