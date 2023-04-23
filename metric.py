# -*- coding: utf-8 -*-
"""metric.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ftwl_FexUv3wvSgTM80ZqXoJh0j9J8q6
"""

#read csv file and store data in appropriate  objects

import pandas as pd
import ast
import networkx as nx
import csv

try:
    df = pd.read_csv('/content/TED_Talk.csv', error_bad_lines=False, engine='python')
except FileNotFoundError as e:
    print(f"Error: {e}")
    # exit(1)
except pd.errors.ParserError as e:
    print(f"Error: {e}")
    # exit(1)

df = df.iloc[:, :-2]

def similarity(original_tags, recommended_tags):
  original_tags = set(original_tags)
  recommended_tags = set(recommended_tags)
  # print(original_tags)
  # print(recommended_tags)
  similarity_score = len(original_tags.intersection(recommended_tags)) / len(original_tags.union(recommended_tags))
  # print(len(original_tags.intersection(recommended_tags)))
  # print(len(original_tags.union(recommended_tags)))
  return similarity_score

def dissimilarity(similarity):
  return 1 - similarity

def views(views, threshold):
  if views > threshold:
    difference = views - threshold
    reward = difference ** 3 #gradual increase, steeper for higher values
    normalized_views = max(0, min(1, reward / (threshold ** 3)))
    return normalized_views
  else:
    return 0

import math
def duration(duration, threshold, k):
  if duration > threshold:
    difference = duration - threshold
    penalty = difference ** 2 # gradual fall
    normalized_duration =  - 1 / (1 + math.exp((720 - duration) / k))
    return normalized_duration
  else:
    return 0

def duration2(duration, threshold):
    if duration > threshold:
        difference = duration - threshold
        penalty = difference ** 2 # gradual fall
        K = 20575296 # maximum possible penalty valuex
        normalized_penalty = penalty / (penalty + K)
        return normalized_penalty
    else:
        return 0.0

def score(similarity_score, dissimilarity_score, normalized_views, normalized_duration):
  return 0.2*similarity_score + 0.3*dissimilarity_score + 0.3*normalized_views + 0.2*normalized_duration

def calculate_score(df):
  scores = {}
  for index, row in df.iterrows():
    talk_id = row['talk_id']
    related_talks = row['related_talks']
    original_tags = row['talks__tags']
    # print(type(original_tags))
    # related_talks = ast.literal_eval(related_talks)
    # print(type(related_talks))
    # print(related_talks)
    mylist = []
    try:
      for talk in ast.literal_eval(related_talks):
        qry = 'talk_id == '
        qry += str(talk['id'])
        try:
          for tg in ast.literal_eval(df.query(qry)['talks__tags'].values[0]):
            mylist.append(tg)
        # print(talks_df.query(qry)['talks__tags'])
          # print(mylist)
        except Exception as e:
          # print(e)
          continue
        
        similarity_score = similarity(ast.literal_eval(original_tags), mylist)
        dissimilarity_score = dissimilarity(similarity_score)
        duration_score = duration(talk["duration"], 720, 2)
        views_score = views(talk["viewed_count"], 1000000)
        scores[talk_id] = score(similarity_score, dissimilarity_score, views_score, duration_score)
        # print(scores[talk_id])
    except Exception as e:
      # print(e)
      continue
  # print(scores)
  return scores

print(calculate_score(df))



#@title Algorithm 2- Using Tags graph and a rating parameter
import pandas as pd
import ast
import networkx as nx
import random

# read the tags from the csv file
df = pd.read_csv('TED_Talk.csv')

# drop rows with NaN values in the 'talks_tags' column
df = df.dropna(subset=['talks__tags'])

# create an empty directed graph
G = nx.DiGraph()

# add nodes to the graph for each unique tag
for tags in df['talks__tags']:
  try:
    if isinstance(tags, str):
        tags_list = ast.literal_eval(tags)
        for tag in tags_list:
            G.add_node(tag)
  except Exception as e:
    # print(e)
    continue
# add edges based on shared tags
for tags in df['talks__tags']:
  try:
    if isinstance(tags, str):
        tags_list = ast.literal_eval(tags)
        for i in range(len(tags_list)-1):
            for j in range(i+1, len(tags_list)):
                G.add_edge(tags_list[i], tags_list[j])
  except Exception as e:
    # print(e)
    continue

# Define the seed tag for the playlist
seed_tag = 'education'

# Find the neighborhood of the seed tag
neighborhood = set(G.neighbors(seed_tag))

# Find the TED Talks that are tagged with at least one tag in the neighborhood
recommended_talks = []
for index, row in df.iterrows():
  try:
    talk_tags = ast.literal_eval(row['talks__tags'])
    if len(set(talk_tags).intersection(neighborhood)) > 0:
        recommended_talks.append(row)
  except Exception as e:
    # print(e)
    continue
# Rank the recommended talks by view count
# ranked_talks = sorted(ast.literal_eval(recommended_talks), key=lambda x: x['views'], reverse=True)
try:
  talks_list = ast.literal_eval(recommended_talks)
except Exception as e:
  # print(e)
  pass
ranked_talks = []
try:    
  for talk in sorted(talks_list, key=lambda x: x['views'], reverse=True):
      ranked_talks.append(talk)
except Exception as e:
  # print(e)
  pass
print(ranked_talks)
# Select the top talks for the playlist
playlist = [talk['talk_name'] for talk in ranked_talks[:10]]

print("\n\n")
print("Recommendeded TED Talks playlist based on the tag:", seed_tag)
print(playlist)
new_df = pd.DataFrame(playlist)
score = calculate_score(new_df)

print(score)

import pandas as pd
import ast
import networkx as nx
import random

# read the tags and user views from the csv file
df = pd.read_csv('TED_Talk.csv')

# drop rows with NaN values in the 'talks_tags' and 'user_views' columns
df = df.dropna(subset=['talks__tags', 'views'])

# create an empty directed graph
G = nx.DiGraph()

# add nodes to the graph for each unique tag
for tags in df['talks__tags']:
  try:
    if isinstance(tags, str):
        tags_list = ast.literal_eval(tags)
        for tag in tags_list:
            G.add_node(tag)
  except:
    continue

# add edges based on shared tags
for tags in df['talks__tags']:
  try:
    if isinstance(tags, str):
        tags_list = ast.literal_eval(tags)
        for i in range(len(tags_list)-1):
            for j in range(i+1, len(tags_list)):
                G.add_edge(tags_list[i], tags_list[j])
  except:
    continue

# Define the seed tag for the playlist
seed_tag = 'education'

# Find the neighborhood of the seed tag
neighborhood = set(G.neighbors(seed_tag))

# Find the TED Talks that are tagged with at least one tag in the neighborhood
recommended_talks = []
for index, row in df.iterrows():
  try:
    talk_tags = ast.literal_eval(row['talks__tags'])
    if len(set(talk_tags).intersection(neighborhood)) > 0:
        recommended_talks.append(row)
  except:
    continue

# Rank the recommended talks by average user views
ranked_talks = []
for talk in recommended_talks:
  try:
    views_dict = ast.literal_eval(talk['views'])
    avg_views = sum(views_dict.values()) / len(views_dict)
    talk['avg_views'] = avg_views
    ranked_talks.append(talk)
  except:
    continue

ranked_talks = sorted(ranked_talks, key=lambda x: x['avg_views'], reverse=True)

# Select the top talks for the playlist
playlist = [talk['talk_name'] for talk in ranked_talks[:10]]

print("\n\n")
print("Recommended TED Talks playlist based on the tag:", seed_tag)
for talk in playlist:
    print(talk)

print("\n\n")

print(playlist)

#@title Algorithm 4- Based on talk tags' subset tree graph
import csv
import networkx as nx
import heapq

# create an empty directed graph
G = nx.DiGraph()

# read the TED Talk tags and related talks from a CSV file
with open('TED_Talk.csv', 'r', errors='ignore') as infile:
    reader = csv.reader(infile, dialect='excel')
    next(reader)
    
    count = 0
    for in_line in reader:
        if count == 200:
            break
        
        talk_tags = in_line[1].strip('[]').replace('\'', '').split(', ')
        G.add_node(in_line[0])
        for node in G.nodes():
            if node != in_line[0]:
                node_tags = nx.get_node_attributes(G, 'tags')[node]
                if set(node_tags).issubset(set(talk_tags)):
                    G.add_edge(node, in_line[0], weight=len(set(node_tags).intersection(set(talk_tags))))
        nx.set_node_attributes(G, {in_line[0]: {'tags': talk_tags}})
        count += 1

# remove isolated nodes
isolated_nodes = list(nx.isolates(G))
G.remove_nodes_from(isolated_nodes)

# define a function to compute the relevance score of a talk based on its PageRank score and edge weights
def relevance_score(talk, damping_factor=0.85):
    pagerank_score = nx.pagerank(G, alpha=damping_factor, weight='weight')[talk]
    return pagerank_score * len(G.in_edges(talk))

# define a function to recommend related talks based on a given talk
def recommend(talk, top_k=10):
    related_talks = []
    for neighbor in G.neighbors(talk):
        score = relevance_score(neighbor)
        heapq.heappush(related_talks, (-score, neighbor))
    return [talk[1] for talk in heapq.nsmallest(top_k, related_talks)]

for node in G.nodes():
    recommendations = recommend(node)
    if recommendations:
        print(f"Recommendations for node {node}:")
        print(recommendations)

print(G)

