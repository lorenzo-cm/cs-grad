import heapq
import numpy as np
from src.utils import get_neighbors

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def astar(cost_matrix, x0, y0, xf, yf) -> tuple[int, list[tuple]]:
    open_set = []
    heapq.heappush(open_set, (0, x0, y0))
    
    # cost from origin
    g_score = { (x0, y0): 0 }
    
    # cost to goal
    f_score = { (x0, y0): manhattan_distance(x0, y0, xf, yf) }

    visited = set()
    came_from = {}

    while open_set:
        # node with the lowest f score
        _, x, y = heapq.heappop(open_set)
        
        # achieved goal and reconstruct the path
        if (x, y) == (xf, yf):
            path = []
            while (x, y) in came_from:
                path.append((x, y))
                x, y = came_from[(x, y)]
            path.append((x0, y0))
            path.reverse()
            return g_score[(xf, yf)], path
        
        visited.add((x, y))
        
        neighbors = get_neighbors(cost_matrix, x, y)
        for nx, ny in neighbors:
            if (nx, ny) in visited:
                continue

            tentative_g_score = g_score[(x, y)] + cost_matrix[nx, ny]
            
            # check if it is a better score or is a new path
            # if so, update scores and came from and queue it
            if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                came_from[(nx, ny)] = (x, y)
                g_score[(nx, ny)] = tentative_g_score
                f_score[(nx, ny)] = tentative_g_score + manhattan_distance(nx, ny, xf, yf)
                heapq.heappush(open_set, (f_score[(nx, ny)], nx, ny))
    
    return np.inf, []
