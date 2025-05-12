import numpy as np
from src.utils import get_neighbors

def bfs(cost_matrix, x0, y0, xf, yf):
    queue = []
    visited = []

    len_y = len(cost_matrix)
    len_x = len(cost_matrix[0])
    costs = np.full((len_y, len_x), np.inf)
    costs[x0, y0] = 0

    path = {}

    queue.append((x0, y0))
    path[(x0, y0)] = None

    while queue:
        x, y = queue.pop(0)
        visited.append((x,y))

        if x == xf and y == yf:
            return costs[xf, yf], get_path(path, xf, yf)

        for nx, ny in get_neighbors(cost_matrix, x, y):
            if (nx,ny) not in visited:
                queue.append((nx,ny))
                
            new_cost = costs[x, y] + cost_matrix[nx][ny]
            
            if new_cost < costs[nx, ny]:
                costs[nx, ny] = new_cost
                path[(nx, ny)] = (x, y)
                
    return np.inf, []

def get_path(path_dict, x, y):
    full_path = [(x, y)]
    while path_dict[(x, y)] is not None:
        x, y = path_dict[(x, y)]
        full_path.append((x, y))
    full_path.reverse()
    return full_path