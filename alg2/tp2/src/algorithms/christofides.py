import networkx as nx

def christofides_algorithm(G, local_search=True):
    # Encontrar uma Árvore Geradora Mínima
    mst = minimum_spanning_tree(G)

    # Encontrar Vértices de Grau Ímpar na MST
    odd_degree_nodes = find_odd_degree_nodes(mst)

    # Emparelhamento Mínimo
    min_matching = minimum_weight_matching(G, odd_degree_nodes)

    # Unir o Emparelhamento com a MST
    multigraph = nx.MultiGraph(mst)
    multigraph.add_edges_from(min_matching)

    # Encontrar um Circuito Euleriano
    eulerian_circuit = list(nx.eulerian_circuit(multigraph))

    # Transformar o Circuito Euleriano em um Circuito Hamiltoniano
    hamiltonian_circuit = make_hamiltonian(eulerian_circuit)

    optimized_circuit = hamiltonian_circuit

    if local_search:
        # Aplicar a heurística 2-opt (testei 3-opt mas demora muito mais)
        optimized_circuit = apply_2_opt(hamiltonian_circuit, G)

    cost = calculate_cost(optimized_circuit, G)

    return cost, hamiltonian_circuit

def minimum_spanning_tree(G):
    return nx.minimum_spanning_tree(G)

def find_odd_degree_nodes(G):
    return [v for v, d in G.degree() if d % 2 == 1]

def minimum_weight_matching(G, odd_degree_nodes):
    min_matching = []
    while odd_degree_nodes:
        v = odd_degree_nodes.pop()
        distance, u = min((G[v][u]['weight'], u) for u in odd_degree_nodes)
        min_matching.append((v, u))
        odd_degree_nodes.remove(u)
    return min_matching

def make_hamiltonian(eulerian_circuit):
    path = []
    visited = set()
    for u, v in eulerian_circuit:
        if u not in visited:
            path.append(u)
            visited.add(u)
    path.append(path[0])  # Returning to the starting point
    return path

def apply_2_opt(route, G):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                if calculate_cost(new_route, G) < calculate_cost(best, G):
                    best = new_route
                    improved = True
        route = best
    return best

def calculate_cost(route, G):
    return sum(G[route[i]][route[i + 1]]['weight'] for i in range(len(route) - 1))