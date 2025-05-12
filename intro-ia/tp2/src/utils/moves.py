from src.settings import *

def get_moves(reward_matrix, x, y):
    moves = []
    for direction_fn in DIRECTIONS.values():
        new_x, new_y = direction_fn(x,y)
        valid = is_valid(reward_matrix, new_x, new_y)
        moves.append(
            (
                (new_x, new_y),
                valid
            )
        )
        
    return moves

def is_valid(reward_matrix, x, y):
    len_vertical = len(reward_matrix)
    len_horizontal = len(reward_matrix[0])

    if 0 <= y < len_horizontal and 0 <= x < len_vertical:        
        if reward_matrix[x, y] != CHAR_REWARDS['@']:
            return True
    
    return False