import sys
import threading
import time

from algorithms.branch_and_bound import branch_and_bound
from algorithms.twice_around_the_tree import twice_around_the_tree
from algorithms.christofides import christofides_algorithm
from utils.drop_vertex import drop_vertices
from utils.load_graph import create_tsp_graph_from_file

TIME_LIMIT = 1800

def time_limit(timeout):
    time.sleep(timeout)
    print('Time limit exceeded')
    print("Custo: nan")
    print("Caminho: nan")
    exit()

if __name__ == "__main__":

    file_path = sys.argv[1]

    if len(sys.argv) > 2:
        num_vertices_remove = int(sys.argv[2])

    tsp_graph = create_tsp_graph_from_file(file_path)

    if len(sys.argv) > 2:
        tsp_graph = drop_vertices(tsp_graph, (len(tsp_graph.nodes) - num_vertices_remove))

    cost_tw, path_tw = twice_around_the_tree(tsp_graph)

    print("Custo (twice around the tree):", cost_tw)
    print("Caminho:", path_tw)

    print('\n')

    cost_chr, path_chr = christofides_algorithm(tsp_graph, local_search=False)

    print("Custo (christofides):", cost_chr)
    print("Caminho:", path_chr)

    print('\n')

    time_limit(TIME_LIMIT)

    cost, path = branch_and_bound(tsp_graph)

    print("Custo:", cost)
    print("Caminho:", path)

    import networkx as nx
    path_nx = nx.approximation.traveling_salesman_problem(tsp_graph)
    cost_nx = sum(tsp_graph[path_nx[i]][path_nx[i + 1]]['weight'] for i in range(len(path_nx) - 1))
    print("Custo (networkx):", cost_nx)