import networkx as nx

def get_min_degree(G:nx.Graph):
    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    min_degree = float('inf')
    for node in G:
        node_degree = G.degree[node]
        if node_degree < min_degree:
            min_degree = node_degree
    
    return S, min_degree

def first_fase (G:nx.Graph):
    S, min_degree = get_min_degree(G)
    valid_cc_for_k ={}
    valid_cc_for_k[0] = S 
    
    for k in range(1,min_degree+1):
        valid_cc_for_k[k] = S
        # valid_cc_for_k[k], G_reducing = CC_degree_bigger_k(G_reducing,k)
        # is garanteed that in every connected component the nodes have degree >= k. Later we most find the minimum subgraph that holds that condition
    return valid_cc_for_k

def second_fase(original_G:nx.Graph,valid_cc_for_k:dict):
    result_for_k = {}
    for k in valid_cc_for_k:
        min_curr = float('inf')
        for cc in valid_cc_for_k[k]:
            sub_graph, n_nodes = backtrack_minimum_k_cover(cc,k)
            if n_nodes < min_curr:
                result_for_k[k] = (sub_graph,n_nodes)
                min_curr = n_nodes
    return result_for_k

def backtrack_minimum_k_cover(CC:nx.Graph,k:int):
    minimum_nodes = CC.number_of_nodes()
    min_subgraph = CC.copy()
    for remove_node in CC:
        CC_removed = CC.copy()
        CC_removed.remove_node(remove_node)
        if k_cover(CC_removed,k) and CC_removed.number_of_nodes() > 0:
            # if the node can be removed check if its branch improves min_subgraph
            subtree_min_subgraph,subtree_min_nodes = backtrack_minimum_k_cover(CC_removed,k)
            if subtree_min_nodes < minimum_nodes:
                minimum_nodes = subtree_min_nodes
                min_subgraph = subtree_min_subgraph
            if k != 0 and minimum_nodes == k*2:
                return min_subgraph, minimum_nodes
            if k==0 and minimum_nodes == k+1:
                return min_subgraph, minimum_nodes
    return min_subgraph, minimum_nodes
    
def k_cover(G:nx.Graph,k:int):
    Degrees= G.degree()
    for node in G:
        if Degrees[node] < k:
            return False
    return True

def solver_1(G:nx.Graph):
    valid_cc_for_k = first_fase(G)
    result_for_k = second_fase(G,valid_cc_for_k)
    return result_for_k
