import networkx as nx
import math

from utils.utils import euclidean_distance

def haversine(coord1, coord2):
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def create_tsp_graph_from_file(file_path):
    """
    Cria um grafo NetworkX para o problema TSP a partir de um arquivo de coordenadas.

    Args:
    file_path (str): Caminho para o arquivo contendo os dados do TSP.

    Returns:
    networkx.Graph: Grafo representando o problema TSP.
    """
    G = nx.Graph()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    edge_weight_type_line = next(line for line in lines if "EDGE_WEIGHT_TYPE" in line)
    edge_weight_type = edge_weight_type_line.split(":")[1].strip()

    start = lines.index("NODE_COORD_SECTION\n") + 1
    
    # Modifique esta parte para lidar com diferentes formatos de EOF
    for i in range(start, len(lines)):
        if "EOF" in lines[i]:
            end = i
            break
    else:
        raise ValueError("EOF not found in file")

    coord_lines = lines[start:end]

    coords = {}
    for line in coord_lines:
        parts = line.split()
        coords[parts[0]] = (float(parts[1]), float(parts[2]))

    # Adiciona os nós com suas coordenadas
    for node, coord in coords.items():
        G.add_node(node, coord=coord)

    # Adiciona as arestas com pesos baseados na distância euclidiana
    for node1, coord1 in coords.items():
        for node2, coord2 in coords.items():
            if node1 != node2:
                if edge_weight_type == "EUC_2D":
                    distance = euclidean_distance(coord1, coord2)
                elif edge_weight_type == "GEO":
                    distance = haversine(coord1, coord2)
                G.add_edge(node1, node2, weight=distance)

    return G