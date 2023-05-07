import networkx as nx
from typing import Tuple, List
from Generator import bipartition
from Vertices_Solver import solver_1

def top_down_solver(G:nx.Graph):
    min_degree = get_min_degree(G)
    sol = {k:(None,0) for k in range (min_degree+1)}
    A, B = bipartition(G)
    for k in sol:
        sol[k] = backtrack_top_down(G,k, max(len(A),len(B)))
    return sol
        
def bottom_up_solver(G:nx.Graph):
    min_degree = get_min_degree(G)
    sol = {k:(None,0) for k in range (min_degree+1)}
    A, B = bipartition(G)
    for k in sol:
        sol[k] = backtrack_bottom_up(G,k, max(len(A),len(B)))
    return sol

def get_min_degree(G:nx.Graph):
    # S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    min_degree = float('inf')
    for node in G:
        node_degree = G.degree[node]
        if node_degree < min_degree:
            min_degree = node_degree
    print("min degree : ",min_degree)
    return min_degree

def K_cover(G:nx.Graph,k:int,lesser=False):
    Degrees = G.degree()
    nodes_to_fix = []
    k_cover = True 
    for node in G:
        if not lesser:
            if Degrees[node] > k:
                nodes_to_fix.append(node)
            if Degrees[node] < k:
                k_cover = False
                return k_cover, nodes_to_fix
        if lesser:
            if Degrees[node] < k:
                nodes_to_fix.append(node)
                k_cover = False
            
    return k_cover, nodes_to_fix

def edges_between_greater_k(G:nx.Graph, greater_k:List[int]):
    ebgk = []
    for node in greater_k:
        adj = G.neighbors(node)
        for v in adj:
            if v in greater_k:
                if not (v,node) in ebgk:
                    ebgk.append((node,v))
    return ebgk
    
def backtrack_top_down(G:nx.Graph, k:int, prune_min:int) -> Tuple[nx.Graph,int]:
    min_sub_graph, n_edges = backtrack_top_down_recursive(G,k, prune_min) 
    return min_sub_graph, n_edges

def backtrack_top_down_recursive(G:nx.Graph, k:int, prune_min:int) -> Tuple[nx.Graph,int]:
    min_graph = G
    min_n_edges = G.number_of_edges()
    
    k_cover, greater_k = K_cover(G,k)
    if not k_cover:
        raise ValueError("Should'nt happen!!!")
    removable_edges = edges_between_greater_k(G,greater_k)
    if len(removable_edges) == 0 or min_n_edges == (G.number_of_nodes()/2)*k:
        # base case
        return min_graph, min_n_edges
    
    for edge in removable_edges:
        G_p = G.copy()
        G_p.remove_edge(*edge)
        e_min_gr, e_min_n_e = backtrack_top_down_recursive(G_p,k,prune_min)
        if e_min_n_e < min_n_edges:
            min_graph = e_min_gr
            min_n_edges = e_min_n_e
        if min_n_edges == (prune_min)*k:
            return min_graph, min_n_edges
        
    return min_graph, min_n_edges

def edges_between_lesser_k(G:nx.Graph, all_edges:List[Tuple], lesser_k:List[int]):
    eblk = []
    one_is_lesser_k = []
    for u, v in all_edges:
        if u in lesser_k and v in lesser_k:
            eblk.append((u,v))
        elif u in lesser_k or v in lesser_k:
            one_is_lesser_k.append((u,v))
    return eblk + one_is_lesser_k

def backtrack_bottom_up(G:nx.Graph, k:int, prune_min:int) -> Tuple[nx.Graph,int]:
    G_empty = G.copy()
    G_empty.clear_edges()
    all_edges = []
    for u in G:
        adj = G.neighbors(u)
        for v in adj:
            if not (v,u) in all_edges:
                all_edges.append((u,v))
    return backtrack_bottom_up_recursive(G_empty,k,all_edges,prune_min)

def backtrack_bottom_up_recursive(G:nx.Graph, k:int, edges:list, prune_min:int) -> Tuple[nx.Graph,int]:
    min_graph = G
    min_n_edges = G.number_of_edges()
    
    k_cover, lesser_k = K_cover(G,k,True)
    if k_cover:
        return min_graph, min_n_edges
    add_edges = edges_between_lesser_k(G,edges,lesser_k)
    min_n_edges = float('inf')
    for edge in add_edges:
        G_p = G.copy()
        G_p.add_edge(*edge)
        E_p = edges.copy()
        E_p.remove(edge)
        e_min_gr, e_min_n_e = backtrack_bottom_up_recursive(G_p,k,E_p,prune_min)
        if e_min_n_e < min_n_edges:
            min_graph = e_min_gr
            min_n_edges = e_min_n_e
        if min_n_edges == (prune_min)*k:
            return min_graph, min_n_edges
    return min_graph, min_n_edges