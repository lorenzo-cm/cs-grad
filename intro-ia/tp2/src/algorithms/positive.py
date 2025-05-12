import numpy as np
from src.utils import get_moves
import random

from src.settings import CHAR_REWARDS_POSITIVE, NEGATIVE_INFINITY

def positive(reward_matrix, xi, yi, n, alpha=0.1, gamma=0.9, epsilon=0.1):
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

    for i in range(n):
        possible_moves = get_moves(reward_matrix, x, y)

        if random.random() <= epsilon:
            # random move
            move_index = random.randint(0,3)
        else:
            # best move
            move_index = np.argmax(Q[x, y, :])
        
        move = possible_moves[move_index]
        
        # Movimento para a parede ou para fora do mapa
        # Permanece no mesmo estado
        nx, ny = move[0] if move[1] else (x, y)
        reward = reward_matrix[nx, ny] if move[1] else NEGATIVE_INFINITY
        
        # Se chegar em fogo ou objetivo
        # Nao tem lance futuro nesse caso
        if reward_matrix[nx, ny] in [CHAR_REWARDS_POSITIVE['x'], CHAR_REWARDS_POSITIVE['O']]:
            Q[x, y, move_index] += alpha * (reward - Q[x, y, move_index])
            x, y = xi, yi
        else:
            best_next_move_reward = np.max(Q[nx, ny, :])
            Q[x, y, move_index] += alpha * (reward + gamma * best_next_move_reward - Q[x, y, move_index])
            x, y = nx, ny

    return Q
