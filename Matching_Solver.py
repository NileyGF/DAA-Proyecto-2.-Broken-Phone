from audioop import add
import re
import networkx as nx
from typing import Tuple, List

def Solver_deprecated(G:nx.Graph) -> List[Tuple[nx.Graph,int]]:
    min_degree = get_min_degree(G)
    solution = {k:(None,0) for k in range(min_degree + 1)}
    G_k = G.copy()
    G_k.clear_edges()
    G_p = G.copy()
    solution[0] = (G_k.copy(), 0)
    for i in range(1, min_degree + 1):
        DiG = create_the_flow_graph(G_p,1)
        Flow = Edmonds_Karp(DiG)
        satured, outliers = get_matching_and_outliers(G_p, Flow)
        G_p, G_k, n_edges = arbitrary_get_all_to_k(G_p, G_k, satured, outliers)        
        solution[i] = (G_k.copy(), n_edges)
    return solution

def Solver(G:nx.Graph) -> List[Tuple[nx.Graph,int]]:
    min_degree = get_min_degree(G)
    solution = {k:(None,0) for k in range(min_degree + 1)}
    # print("G:\t",G)
    G_k = G.copy()
    G_k.clear_edges()
    G_p = G.copy()
    solution[0] = (G_k.copy(), 0)
    for i in range(1, min_degree + 1):
        # print("i = ",i,".  G_k:\t", G_k)            
        # print("i = ",i,".  G_p:\t", G_p)
        DiG = create_the_flow_graph(G_p,i)
        # print("i = ",i,".  Dig:\t", DiG)
        Flow = Edmonds_Karp(DiG)
        # print("i = ",i,".  Flow:\t", Flow, Flow.graph["flow_value"])
        # satured, outliers = get_matching_and_outliers(G_p, Flow)
        # G_p, G_k, n_edges = arbitrary_get_all_to_k(G_p, G_k, satured, outliers)
        solution[i] = get_everyone_to_k(G,Flow,i)
        # if cover:
        #     solution[i] = (G_k.copy(), G_k.number_of_edges())
        # else: 
        #     solution[i] = (G_k.copy(), G_k.number_of_edges())
            
    return solution

def get_min_degree(G:nx.Graph):
    min_degree = float('inf')
    for node in G:
        node_degree = G.degree[node]
        if node_degree < min_degree:
            min_degree = node_degree
    print("min degree : ", min_degree)
    return min_degree

def create_the_flow_graph(G:nx.Graph,cap) -> nx.DiGraph:
    Di_G = nx.DiGraph()
    nodes = G.nodes(data=True)
    for n, d in nodes:
        Di_G.add_node(n, bipartite=d['bipartite'])
    Di_G.add_node('s',bipartite=-1)
    Di_G.add_node('t',bipartite=2)
    
    for n, d in nodes:
        if d['bipartite'] == 0:
            Di_G.add_edge('s', n, capacity=cap)
            for v in G[n]:
                Di_G.add_edge(n , v, capacity=1)
        elif d['bipartite'] == 1:
            Di_G.add_edge(n, 't', capacity=cap)
    return Di_G
    
def Edmonds_Karp(G:nx.DiGraph, s='s', t='t') -> nx.DiGraph: 
    # NetworkX DiGraph :  Residual network after computing the maximum flow.returns the residual network
    if s not in G:
        raise nx.NetworkXError(f"node {str(s)} not in graph")
    if t not in G:
        raise nx.NetworkXError(f"node {str(t)} not in graph")
    if s == t:
        raise nx.NetworkXError("source and sink are the same node")
    R = build_residual_network(G)
    # Initialize/reset the residual network.
    for u in R:
        for e in R[u].values():
            e["flow"] = 0
            
    # print("Residual:\t", R)
            
    flow_value = 0    
    # R_nodes = R.nodes
    # R_pred = R.pred
    R_succ = R.succ
    
    def find_aug_path():
        parent = bfs_in_directed()
        if parent is None:
            return None
        path = [t]
        u = t
        while u != s:
            u = parent[u]
            path.append(u)
        path.reverse()
        return path

    def bfs_in_directed():
        """breadth-first search for an augmenting path."""
        visited = {s:None}
        queue = [s]
        while queue:
            q = []
            for u in queue:
                # queue.remove(u)
                for v, attr in R_succ[u].items():
                    if (v not in visited) and (attr["flow"] < attr["capacity"]):
                        visited[v] = u
                        if v == t:
                            return visited
                        q.append(v)
            queue = q
        return None

    def augment(path):
        """Augment flow along a path from s to t."""
        # Determine the path residual capacity.
        flow = float('inf')

        u = path[0]
        for i in range(1,len(path)):
            v = path[i]
            attr = R_succ[u][v]
            flow = min(flow, attr["capacity"] - attr["flow"])
            u = v
        
        # Augment flow along the path.
        u = path[0]
        for i in range(1,len(path)):
            v = path[i]
            R_succ[u][v]["flow"] += flow
            R_succ[v][u]["flow"] -= flow
            u = v
        return flow

    # Look for shortest augmenting paths using breadth-first search.
    while True:
        path = find_aug_path()
        if path is None:
            break
        flow_value += augment(path)
   
    R.graph["flow_value"] = flow_value
    return R

def build_residual_network(G:nx.DiGraph) -> nx.DiGraph:
    R = nx.DiGraph()
    nodes = G.nodes(data=True)
    for n, d in nodes:
        R.add_node(n, bipartite=d['bipartite'])
    edge_list = [
        (u, v, attr)
        for u, v, attr in G.edges(data=True)
        # if u != v and attr.get('capacity') > 0
    ]
    for u, v, attr in edge_list:
            if not R.has_edge(u, v):
                # Both (u, v) and (v, u) must be present in the residual network.
                R.add_edge(u, v, capacity=attr.get('capacity'))
                R.add_edge(v, u, capacity=0)
            else:
                # The edge (u, v) was added when (v, u) was visited.
                R[u][v]["capacity"] = attr.get('capacity')
    return R
    
def get_matching_and_outliers(G:nx.Graph, R:nx.DiGraph):
    satured = []
    queue = []
    for v, attr in R.succ['s'].items(): # bipartite = 0
        queue.append(v)
    while queue:
        for u in queue: # bipartite = 0
            queue.remove(u)
            for v, attr in R.succ[u].items(): # bipartite = 1
                if (attr["flow"] == attr["capacity"]) and (v in G[u]):
                    # satured edges that belonged in the original graph
                    satured.append((u,v))
    # if len(satured) == 0:
    #     return [], []
    outliers = []
    degree_1 = []
    for u,v in satured:
        degree_1 = degree_1 + [u,v]
    outliers = list(set(G.nodes) - set(degree_1))
    return satured, outliers

def arbitrary_get_all_to_k(G_p:nx.Graph, G_k:nx.Graph, satured:List[Tuple], outliers:list):
    k_th_matching = satured 
    for u in outliers:
        adj = G_p.neighbors(u)
        for v in adj:
            k_th_matching.append((u,v))
            break
        
    ## now build G_k such that is K_cover
    if len(k_th_matching) != 0:
        G_k.add_edges_from(k_th_matching)
        G_p.remove_edges_from(k_th_matching)
    return G_p, G_k, G_k.number_of_edges()

def get_everyone_to_k(G:nx.Graph, R:nx.DiGraph,k:int):
    satured = []
    queue = []
    for v, attr in R.succ['s'].items(): # bipartite = 0
        queue.append(v)
    # while queue:
    for u in queue: # bipartite = 0
        # queue.remove(u)
        for v, attr in R.succ[u].items(): # bipartite = 1
            if (attr["flow"] == attr["capacity"]) and (v in G[u]):
                # satured edges that belonged in the original graph
                satured.append((u,v))
    G_p = G.copy()
    G_p.clear_edges()
    G_p.add_edges_from(satured)
    k_cover, nodes_to_fix = K_cover(G_p,k)
    add_edges = edges_between_lesser_k(G,nodes_to_fix)
    for u, v in add_edges:
        if G_p.degree[u] < k or G_p.degree[v] < k:
            G_p.add_edge(u,v)
    return G_p, G_p.number_of_edges()
    

def K_cover(G:nx.Graph,k:int):
    Degrees = G.degree()
    nodes_to_fix = []
    k_cover = True 
    for node in G:
        if Degrees[node] < k:
            nodes_to_fix.append(node)
            k_cover = False
            
    return k_cover, nodes_to_fix

def edges_between_lesser_k(G:nx.Graph, lesser_k:List[int]):
    eblk = []
    one_is_lesser_k = []
    for u, v in G.edges():
        if u in lesser_k and v in lesser_k:
            eblk.append((u,v))
        elif u in lesser_k or v in lesser_k:
            one_is_lesser_k.append((u,v))
    if len(eblk) > 0:
        raise Exception(" the matching wasn't max ")
    return eblk + one_is_lesser_k


