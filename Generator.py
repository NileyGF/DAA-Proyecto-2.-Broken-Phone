import random
import networkx as nx

def Gen_Bipartite_Graph(min_nodes, max_nodes):
    G = nx.Graph()
    n = random.randint(min_nodes,max_nodes)
    A_size = random.randint(1,n-1)
    A = [i+1 for i in range(A_size)]
    B = [i+1 for i in range(A_size,n)]
    G.add_nodes_from(A,bipartite=0)
    G.add_nodes_from(B,bipartite=1)
    # K_ab has a*b edges at most
    max_edges = len(A) * len(B) 
    m = random.randint(min(n+3,max_edges),max_edges)
    E = []
    edge_count = 0
    while edge_count < m:
        # generate random edge, u,v
        u = random.choice(A)
        v = random.choice(B)
        if v in G[u] or (u,v) in E or (v,u) in E:
            continue
        else:
            E.append((u, v))
            edge_count += 1
    G.add_edges_from(E)
    return G 

def bipartition(G:nx.Graph):
    A = []
    B = []
    nodes = G.nodes(data=True)
    for n, d in nodes:
        if d['bipartite'] == 0:
            A.append(n)
        elif d['bipartite'] == 1:
            B.append(n)
    return A, B

