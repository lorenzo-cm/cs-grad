import numpy as np
from src.settings import *

def read_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    matrix = [list(line.strip()) for line in lines[1:]]    
    cost_matrix = np.array([[CHAR_COSTS[char] for char in row] for row in matrix])
    
    return cost_matrix
