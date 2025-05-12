import numpy as np
import random

random.seed(42)

NEGATIVE_INFINITY = -50

CHAR_REWARDS = {
    '.': -0.1,
    ';': -0.3,
    '+': -1.0,
    'x': -10.0,
    'O': 10.0,
    '@': NEGATIVE_INFINITY
}

CHAR_REWARDS_POSITIVE = {
    '.': 3.0,
    ';': 1.5,
    '+': 1,
    'x': 0,
    'O': 10,
    '@': NEGATIVE_INFINITY
}

DIRECTIONS = {
    'up': lambda x, y: (x-1, y),
    'down': lambda x, y: (x+1, y),
    'right': lambda x, y: (x, y+1),
    'left': lambda x, y: (x, y-1),
}

DIRECTIONS_SYMBOLS = ['^', 'v', '>', '<']