from src.settings import *

def get_neighbors(matrix, x, y):
    neighbors = [
        direction(x, y) for direction in DIRECTIONS.values()
        if is_valid(matrix, *direction(x, y))
    ]
    return neighbors

def is_valid(matrix, x, y):
    len_vertical = len(matrix)
    len_horizontal = len(matrix[0])

    if 0 <= y < len_horizontal and 0 <= x < len_vertical:
        if matrix[x, y] != np.inf:
            return True
    
    return False