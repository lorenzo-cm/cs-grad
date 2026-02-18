import networkx as nx
import numpy as np

def twice_around_the_tree(G):
    """
    Implementação do algoritmo Twice Around the Tree para o problema TSP.

    Args:
    G (networkx.Graph): Grafo representando o problema TSP.
    start_node: Nó de início para o ciclo Hamiltoniano.

    Returns:
    tuple: Custo total do ciclo e o ciclo Hamiltoniano como uma lista de nós.
    """

    start_node = next(iter(G.nodes))

    # Constrói uma Árvore Geradora Mínima (MST)
    mst = nx.minimum_spanning_tree(G)

    # Cria um ciclo visitando a MST duas vezes
    cycle = list(nx.dfs_preorder_nodes(mst, source=start_node)) * 2

    # Remove visitas repetidas para formar um ciclo Hamiltoniano
    hamiltonian_cycle = []
    visited = set()
    for node in cycle:
        if node not in visited:
            visited.add(node)
            hamiltonian_cycle.append(node)
    hamiltonian_cycle.append(start_node)  # Retorna ao ponto de partida

    # Calcula o custo total do ciclo Hamiltoniano
    total_cost = sum(G.edges[hamiltonian_cycle[i], hamiltonian_cycle[i + 1]]['weight']
                     for i in range(len(hamiltonian_cycle) - 1))

    return total_cost, hamiltonian_cycle