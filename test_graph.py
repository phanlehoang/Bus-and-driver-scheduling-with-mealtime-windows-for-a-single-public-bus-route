import networkx as nx 

# Khởi tạo 1 Undirected Graph G:
G = nx.Graph()

# Khởi tạo 1 Directed Graph H:
H = nx.DiGraph()


G.add_node(0, feature="nature", label=0)
print("Node 0 attribute is: {}".format(G.nodes[0]))

# Thêm nhiều node bằng cách mô tả attribute của các nodes trong 1 dict
# sử dụng lệnh nx.add_nodes_from()

G.add_nodes_from([
  (1, {"feature": "animals", "label": 1}),
  (2, {"feature": "forest", "label": 2})
]) #(node, attribute_dict)

# In mô tả của các nodes
for node in G.nodes(data=True):
  print(node)
  
 # In ra thông tin số lượng nodes
num_nodes = G.number_of_nodes()
print("G has {} nodes".format(num_nodes))

# Thêm Edges giữa 2 node:
G.add_edge(0, 1, weight=3)
print("Attribute of edge (0,1) is: {}".format(G.edges[(0,1)]))

# Thêm nhiều Edges bằng cách mô tả attribute của các nodes trong 1 dict
# sử dụng lệnh nx.add_edges_from()

G.add_edges_from([
  (1, 2, {"weight": 2}),
  (2, 0, {"weight": 2.5})
])

# In mô tả của các Edges
for edge in G.edges():
  print(edge)
  
# In số lượng Edges trong Graph
num_edges = G.number_of_edges()
print("G has {} edges".format(num_edges))
nx.draw(G, with_labels=True)