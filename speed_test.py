import time
import networkx as nx
from optimized_ranking_table import readfile, build_graph, normalize_graph, pageRank_weighted

FILENAME = "test_matches.csv"
start = time.time()
data = readfile(FILENAME)
g = build_graph(data)
n = normalize_graph(g)
pageRank_weighted(n)

print(f"Ваш час:      {time.time() - start:.6f} сек")

nx_graph = nx.DiGraph()
for t1, t2, s1, s2 in data:
    if s1 > s2: nx_graph.add_edge(t2, t1, weight=s1-s2)
    elif s2 > s1: nx_graph.add_edge(t1, t2, weight=s2-s1)

start = time.time()
nx.pagerank(nx_graph, weight='weight')
print(f"NetworkX час: {time.time() - start:.6f} сек")

#помітно що зі збільшенням обєму файлу, так виглядає, що бібліотеці стає легше а нашому файлу швидше, проте це вже для надто
#великих об'ємів