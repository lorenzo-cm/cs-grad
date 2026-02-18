import random

def drop_vertices(graph, n, seed=42):
    """
    Remove n random vertices from the given graph.

    Args:
    graph (networkx.Graph): The graph from which vertices are to be removed.
    n (int): The number of vertices to remove.

    Returns:
    networkx.Graph: The modified graph after removing n vertices.
    """
    if n >= len(graph.nodes()):
        raise ValueError(f"Number of vertices to remove is equal to or greater than the total number of vertices in the graph | {n}/{len(graph.nodes())}.")

    random.seed(seed)

    # Select n random vertices
    vertices_to_remove = random.sample(graph.nodes(), n)

    # Remove selected vertices
    graph.remove_nodes_from(vertices_to_remove)

    return graph