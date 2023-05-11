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
               'mix_backtrack':Edges_Solver.mix_solver,
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
        print(duration,'  sec.')
        if compare:
            for k in solution:
                if other_res[i][0][k][1] != solution[k][1]:
                    save_f = open(save_to,'wb')
                    pickle.dump(result,save_f)
                    save_f.close()
                    print_bip(other_res[i][0][k][0],True,str((i,k))+" diff_value")
                    print_bip(solution[k][0],True,save_to+"diff_value")
                    msg = "the solution is diferent!!!  "+ str(other_res[i][0][k][1]) + " and " + str(solution[k][1])
                    print(msg)
    save_f = open(save_to,'wb')
    pickle.dump(result,save_f)
    save_f.close()

"""Generate test cases and solutions, saving them in binary files"""                  
# uncomment following according to what do you intend to test

# Generate_and_Save_Test_Cases(100,6,30)
# ## solve the test cases with the flow-multimatching solution
# Solve_and_Compare('matching','test_cases.bin','matching_solution.bin',False,None)
# ## solve the test cases with the backtracks solutions, and compares them with the earliers ones. If there is a different solution it will informe it
# Solve_and_Compare('mix_backtrack','test_cases.bin','mix_backtrack.bin',True,'matching_solution.bin')
# ## solve the test cases with the solution for when the minimum subgraph was about removing vertices
Solve_and_Compare('vertices','test_cases.bin','vertices.bin',False,None)

""" Load test cases and solutions and do some printing about them"""  
# f1 = open('test_cases.bin','rb')
# graph_list = pickle.load(f1)
# f1.close()

# f2 = open('matching_solution.bin','rb')
# matching_sol = pickle.load(f2)
# f2.close()

# f3 = open('mix_backtrack.bin', 'rb')
# backtrack_sol = pickle.load(f3)
# f3.close()

# for i in range(len(graph_list)):
#     print("i = ",i, " Flow duration : ", str(matching_sol[i][1]), " sec. Backtrack duration : ", " duration : ", str(backtrack_sol[i][1]), " sec.")
#     # g = graph_list[i]
#     # print_bip(g,True)
#     for k in matching_sol[i][0]:
#        print("\tK = ", str(k), ". Flow solution : ", str(matching_sol[i][0][k][1])) 
#        print("\tK = ", str(k), ". Backtrack solution : ", str(backtrack_sol[i][0][k][1])) 
#        print_bip(matching_sol[i][0][k][0])
#        # print_bip(backtrack_sol[i][0][k][0])

"""Interesting graphs"""

# #   Almost K_35  

# G1 = nx.Graph()
# A = [1,2,3]
# B = [4,5,6,7,8]
# G1.add_nodes_from(A,bipartite=0)
# G1.add_nodes_from(B,bipartite=1)
# E = [(1,4), (1,5), (1,6), (2,6), (2,7), (2,8), (3,7), (3,8)]
# G1.add_edges_from( E )

# #   5 nodes on each side, min_degree = 3

# G2 = nx.Graph()

# A =[1,2,3,4,5]
# B =[6,7,8,9,10]
# G2.add_nodes_from(A,bipartite=0)
# G2.add_nodes_from(B,bipartite=1)
# E =  [(6,1), (1,7), (1,8), (1,10), (2,7), (2,6), (2,8), (2,9), (3,7), (3,8), (3,9), (4,8), (4,9), (4,10), (5,6), (5,9), (5,10)]
# G2.add_edges_from( E )

# G3 = nx.Graph()
# A =[1,2,3]
# B =[4,5,6]
# G3.add_nodes_from(A,bipartite=0)
# G3.add_nodes_from(B,bipartite=1)
# E = [(1,4), (1,5), (2,4), (2,5), (2,6), (3,5), (3,6)]
# G3.add_edges_from( E )


# solution1 = Matching_Solver.Solver(G1)
# print_bip(G1)
# for k in solution1:
#     print(solution1[k][1])
#     print_bip(solution1[k][0])
    
# solution2 = Matching_Solver.Solver(G2)
# print_bip(G2)
# for k in solution2:
#     print(solution2[k][1])
#     print_bip(solution2[k][0])

# solution3 = Matching_Solver.Solver_deprecated(G3)
# print_bip(G3)
# for k in solution3:
#     print(solution3[k][1])
#     print_bip(solution3[k][0])

# solution3 = Matching_Solver.Solver(G3)
# print_bip(G3)
# for k in solution3:
#     print(solution3[k][1])
#     print_bip(solution3[k][0])