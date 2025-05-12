import heapq
import numpy as np
from src.utils import get_neighbors

def ucs(cost_matrix, x0, y0, xf, yf):
    len_y = len(cost_matrix)
    len_x = len(cost_matrix[0])
    
    costs = np.full((len_y, len_x), np.inf)
    costs[x0, y0] = 0
    
    # cost, x, y
    pq = [(0, x0, y0)]
    
    path = {}
    path[(x0, y0)] = None
    
    while pq:
        current_cost, x, y = heapq.heappop(pq)

        if x == xf and y == yf:
            return costs[xf, yf], get_path(path, xf, yf)

        for nx, ny in get_neighbors(cost_matrix, x, y):
            new_cost = current_cost + cost_matrix[nx][ny]

            if new_cost < costs[nx, ny]:
                costs[nx, ny] = new_cost
                heapq.heappush(pq, (new_cost, nx, ny))
                path[(nx, ny)] = (x, y)
    
    return np.inf, []

def get_path(path_dict, x, y):
    full_path = [(x, y)]
    while path_dict[(x, y)] is not None:
        x, y = path_dict[(x, y)]
        full_path.append((x, y))
    full_path.reverse()
    return full_path
