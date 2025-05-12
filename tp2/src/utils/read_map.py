import numpy as np
from src.settings import *

def read_map(file_path, mod_id):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    matrix = [list(line.strip()) for line in lines[1:]]    
    
    if mod_id == 'positive':
        return  np.array([[CHAR_REWARDS_POSITIVE[char] for char in row] for row in matrix])
    else:
        return  np.array([[CHAR_REWARDS[char] for char in row] for row in matrix])
