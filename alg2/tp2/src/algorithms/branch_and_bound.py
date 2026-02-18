import numpy as np
import networkx as nx
import heapq

def branch_and_bound(G):
    def path_cost(path):
        return sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))

    def min_edge(G, node, exclude_nodes):
        # Retorna o peso da aresta mínima conectada ao 'node', excluindo 'exclude_nodes', que é o caminho já percorrido
        connected_edges = [G[node][nbr]['weight'] for nbr in G.neighbors(node) if nbr not in exclude_nodes]
        return min(connected_edges) if connected_edges else 0

    def lower_bound(G, path):
        cost = path_cost(path)
        remaining_nodes = set(G.nodes) - set(path)
        if remaining_nodes:
            # Soma dos custos mínimos das arestas para entrar e sair dos nós restantes
            min_edges_cost = sum(min_edge(G, node, path) for node in remaining_nodes)
            cost += min_edges_cost
        return cost

    best_cost = float('inf')
    best_path = None
    heap = []

    # Escolhe um nó inicial arbitrário e o adiciona à heap
    initial_path = [next(iter(G.nodes))]
    heapq.heappush(heap, (lower_bound(G, initial_path), initial_path))

    while heap:
        _, path = heapq.heappop(heap)

        if len(path) == G.number_of_nodes():
            # Verifica se encontrou um caminho completo
            complete_path = path + [path[0]]  # Retorna ao ponto de partida
            cost = path_cost(complete_path)
            if cost < best_cost:
                best_cost, best_path = cost, complete_path
        else:
            # Explora os vizinhos do último nó no caminho
            for neighbor in G.neighbors(path[-1]):
                if neighbor not in path:
                    new_path = path + [neighbor]
                    bound = lower_bound(G, new_path)
                    if bound < best_cost:
                        heapq.heappush(heap, (bound, new_path))

    return best_cost, best_path
