import time
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import random
import Generator
import Vertices_Solver, Edges_Solver, Matching_Solver

def print_bip(G:nx.Graph,save=False,name="graph",edge_labels=False):
    pos = nx.multipartite_layout(G,'bipartite')
    nx.draw(G,pos=pos,with_labels=True )
    if edge_labels:
        labels = nx.get_edge_attributes(G,'capacity')
        # curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
        # straight_edges = list(set(G.edges()) - set(curved_edges))
        nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=labels)
        # nx.draw_networkx(G,pos=pos,edgelist=curved_edges, connectionstyle='arc3, rad = 0.1' )
        # nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=labels)
    if save: plt.savefig(name)
    plt.show()

def print_flow(G,Flow,save=False,name="flow"):
    pos = nx.multipartite_layout(Flow,'bipartite')
    nx.draw_networkx_nodes(Flow,pos=pos )
    edges = Flow.edges(data=True)
    flow_edges = []
    for u, v, d in edges:
        if d["flow"] > 0 and v in G[u]:
            flow_edges.append((u, v))
 
    nx.draw_networkx(Flow,pos=pos,edgelist=flow_edges)
    # nx.draw_networkx_edge_labels(Flow,pos=pos,edge_labels=nx.get_edge_attributes(Flow,'flow'))
    if save: plt.savefig(name)
    plt.show()

def Generate_and_Save_Test_Cases(test_cases, min_n, max_n):
    cases = []    
    random.seed(time.time())
    for i in range(test_cases):
        G = Generator.Gen_Bipartite_Graph(min_n,max_n)
        cases.append(G)
    file = open('test_cases.bin','wb')
    pickle.dump(cases,file)
    file.close()

def Solve_and_Compare(solver:str, read_from:str, save_to:str, compare:bool, compare_to:str):
    solvers = {'vertices':Vertices_Solver.solver_1,
               'edges_backtrack_td':Edges_Solver.top_down_solver,
               'edges_backtrack_bu':Edges_Solver.bottom_up_solver,
               'matching':Matching_Solver.Solver}
    solver = solvers[solver]
    test_cases_f = open(read_from,'rb')
    test_cases = pickle.load(test_cases_f)
    test_cases_f.close()
    if compare:
        other_res_f = open(compare_to,'rb')
        other_res = pickle.load(other_res_f)
        other_res_f.close()
        
    result = []    
    for i in range(len(test_cases)):
        g=test_cases[i]
        st = time.time()
        solution = solver(g)
        et = time.time()
        duration = round(et-st,5)
        result.append((solution,duration))
        if compare:
            for k in solution:
                if other_res[i][0][k][1] != solution[k][1]:
                    save_f = open(save_to,'wb')
                    pickle.dump(result,save_f)
                    save_f.close()
                    print_bip(other_res[i][0][k][0],True,other_res+"diff_value")
                    print_bip(solution[k][0],True,save_to+"diff_value")
                    msg = "the solution is diferent!!!  "+ str(other_res[i][0][k][1]) + " and " + str(solution[k][1])
                    raise ValueError(msg)
    save_f = open(save_to,'wb')
    pickle.dump(result,save_f)
    save_f.close()
                    
Generate_and_Save_Test_Cases(50,6,30)
Solve_and_Compare('matching','test_cases.bin','matching_solution.bin',False,None)
Solve_and_Compare('edges_backtrack_td','test_cases.bin','backtrack_td_solution.bin',True,'matching_solution.bin')