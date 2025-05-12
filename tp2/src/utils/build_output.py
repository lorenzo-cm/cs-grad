import numpy as np
from src.settings import * 

def build_output(Q_matrix: np.ndarray, reward_matrix: np.ndarray) -> np.ndarray:
    a, b = reward_matrix.shape
    output_matrix = []

    for i in range(a):
        temp_list = []
        for j in range(b):
            if reward_matrix[i, j] in [CHAR_REWARDS['@'], CHAR_REWARDS_POSITIVE['@']]:
                temp_list.append('@')
            
            elif reward_matrix[i, j] in [CHAR_REWARDS['x'], CHAR_REWARDS_POSITIVE['x']]:
                temp_list.append('x')
            
            elif reward_matrix[i, j] in [CHAR_REWARDS['O'], CHAR_REWARDS_POSITIVE['O']]:
                temp_list.append('O')
            
            else:
                best_move_index = np.argmax(Q_matrix[i, j, :])
                symbol = DIRECTIONS_SYMBOLS[best_move_index]
                temp_list.append(symbol)
                
                # print(i,j)
                # print(f"build options {Q_matrix[i, j, :]}")
                # print(f"chosen index: {best_move_index} \n\n")
            
        output_matrix.append(temp_list)
                
    return output_matrix


def print_output(output_matrix):
    for row in output_matrix:
        print(''.join(row))
