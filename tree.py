import csv
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# create an empty directed graph
G = nx.DiGraph()
nodeObj = []
tempNodeObj = []
no_of_tags = 0

with open('TED_Talk_TagsRelated_cols.csv', 'r', errors='ignore') as infile:
  reader = csv.reader(infile, dialect='excel')
  next(reader)

  try:
    for in_line in reader:
      if(no_of_tags != int(in_line[2])):
        no_of_tags = int(in_line[2])
        nodeObj = tempNodeObj
        tempNodeObj = []

      if no_of_tags == 0:
        continue

      elif no_of_tags == 1:
        G.add_node(in_line[0])
        in_line[1] = eval(in_line[1])
        tempNodeObj.append(in_line)

      else:
        in_line[1] = eval(in_line[1])
        setSpecific = set(in_line[1])
      for i in nodeObj:
        setGeneral = set(i[1])
        if setGeneral.issubset(setSpecific):
            G.add_edge(i[0], in_line[0])

      G.add_node(in_line[0])
      tempNodeObj.append(in_line)
  except Exception as e:
    print(e)

isolated_nodes = list(nx.isolates(G))
G.remove_nodes_from(isolated_nodes)
nx.draw(G)
plt.show()
