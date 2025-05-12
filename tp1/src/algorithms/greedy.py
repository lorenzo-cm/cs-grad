import numpy as np
from src.utils import get_neighbors

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def greedy(cost_matrix, x0, y0, xf, yf) -> tuple[int, list[tuple]]:
    path = [(x0, y0)]
    visited = []
    cost = 0
    x = x0
    y = y0
    while x != xf or y != yf:
        visited.append((x, y))
        
        neighbors = get_neighbors(cost_matrix, x, y)
        
        unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if (nx, ny) not in visited]
        
        neighbors_costs = [
            cost_matrix[nx, ny] + manhattan_distance(nx, ny, xf, yf) 
            for nx, ny in unvisited_neighbors
        ]
        
        if not unvisited_neighbors:
            return np.inf, [] 
        
        min_index = np.argmin(neighbors_costs)
        
        x, y = unvisited_neighbors[min_index]
        cost += cost_matrix[x, y]
        path.append((x, y))
    
    return cost, path
