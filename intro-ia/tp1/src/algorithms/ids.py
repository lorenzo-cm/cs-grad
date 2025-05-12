import numpy as np
from src.utils import get_neighbors

def ids(cost_matrix, x0, y0, xf, yf, max_depth=20):
    for depth in range(max_depth + 1):
        found, path, cost = dls(cost_matrix, x0, y0, xf, yf, depth, 0, set(), [])
        if found:
            return cost, path
    return np.inf, []


def dls(cost_matrix, x, y, xf, yf, depth, current_cost, visited, path):
    if depth < 0:
        return False, [], np.inf
    
    if (x, y) in visited:
        return False, [], np.inf

    path.append((x, y))
    visited.add((x, y))

    if x == xf and y == yf:
        return True, path[:], current_cost

    found = False
    best_cost = np.inf
    best_path = []

    for nx, ny in get_neighbors(cost_matrix, x, y):
        if (nx, ny) not in visited:
            next_cost = current_cost + cost_matrix[nx][ny]
            result, sub_path, sub_cost = dls(cost_matrix, nx, ny, xf, yf, depth - 1, next_cost, visited, path)

            if result and sub_cost < best_cost:
                found = True
                best_cost = sub_cost
                best_path = sub_path

    path.pop()
    visited.remove((x, y)) # tem que ter para ter todas as permutações de caminhos e para achar caminho mais curto (e nao menos custoso)

    return found, best_path, best_cost