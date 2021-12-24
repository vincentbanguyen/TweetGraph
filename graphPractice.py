import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# ADD NODES
#G.add_node('A')

# ADD EDGES
#G.add_edge('A','B')

G = nx.complete_graph(10)


print(nx.info(G))


# SHOW GRAPH
nx.draw(G, with_labels = True)
plt.show()

## Dhruv was here