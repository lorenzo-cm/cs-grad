import numpy as np
from src.utils import get_moves
import random

from src.settings import CHAR_REWARDS, NEGATIVE_INFINITY

def stochastic(reward_matrix, xi, yi, n, alpha=0.1, gamma=0.9, epsilon=0.1, perpendicular_chance=0.2):
    rows, cols = reward_matrix.shape
    Q = np.zeros((rows, cols, 4))

    # Interpretacao:
    # tuple[int, int]: coords
    # bool: if the move is legal
    move: tuple[tuple[int, int], bool] = None
    x, y = xi, yi
    nx, ny = None, None
    move_index = None
    reward = None

    verbose = False

    for i in range(n):
        # verbose = False
        # if (x,y) == (7,6):
        #     verbose=True
            
        possible_moves = get_moves(reward_matrix, x, y)
        
        if verbose:
            print(f"possible moves {possible_moves}")

        if random.random() <= epsilon:
            if verbose:
                print('random')
            # random move
            move_index = random.randint(0,3)
        else:
            # best move
            move_index = np.argmax(Q[x, y, :])
        
        move = possible_moves[move_index]
        
        if verbose:
            print(f'move scores: {Q[x, y, :]}')
            print(f"move {move}, move index {move_index}")

        
        # Movimento para a parede ou para fora do mapa
        # Permanece no mesmo estado
        nx, ny = move[0] if move[1] else (x, y)
        reward = reward_matrix[nx, ny] if move[1] else NEGATIVE_INFINITY
        
        if verbose:
            print(f"nx, ny {nx, ny}, reward {reward}")
        
        if random.random() <= perpendicular_chance:
            # if move is vertical
            if move_index in [0, 1]:
                perpendicular_move = random.choice(possible_moves[2:])
                
            # if move is horizontal
            else:
                perpendicular_move = random.choice(possible_moves[0:2])
            
            nx, ny = perpendicular_move[0] if perpendicular_move[1] else (x, y)
            reward = reward_matrix[nx, ny] if perpendicular_move[1] else NEGATIVE_INFINITY
            
            if verbose:
                print(f"PERPENDICULAR nx, ny {nx, ny}, reward {reward}")

        # Se chegar em fogo ou objetivo
        # Nao tem lance futuro nesse caso
        if reward_matrix[nx, ny] in [CHAR_REWARDS['x'], CHAR_REWARDS['O']]:
            oldQ= Q[x, y, move_index]
            Q[x, y, move_index] += alpha * (reward - Q[x, y, move_index])
            if verbose:
                print(f"oldq: {oldQ}, new Q {Q[x, y, move_index]}\n\n")
            x, y = xi, yi
        
        else:
            best_next_move_reward = np.max(Q[nx, ny, :])
            oldQ= Q[x, y, move_index]
            Q[x, y, move_index] += alpha * (reward + gamma * best_next_move_reward - Q[x, y, move_index])
            if verbose:
                print(f"oldq: {oldQ}, new Q {Q[x, y, move_index]}\n\n")
            x, y = nx, ny

    return Q
