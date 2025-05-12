import numpy as np


TERRAIN_COSTS = {
    "grass": 1,
    "high_grass": 1.5,
    "water": 2.5,
    "fire": 6,
    "wall": np.inf
}

CHAR_TERRAINS = {
    '.': 'grass',
    ';': 'high_grass',
    '+': 'water',
    'x': 'fire',
    '@': 'wall'
}

CHAR_COSTS = {
    '.': 1,
    ';': 1.5,
    '+': 2.5,
    'x': 6,
    '@': np.inf
}

DIRECTIONS = {
    'up': lambda x, y: (x-1, y),
    'down': lambda x, y: (x+1, y),
    'left': lambda x, y: (x, y-1),
    'right': lambda x, y: (x, y+1),
}