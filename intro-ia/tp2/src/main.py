from src.utils import parse_args, read_map, build_output, print_output
from .settings import *
from src.algorithms import *

METHODS = {
    "standard": standard,
    "stochastic": stochastic,
    "positive": positive
}

def main(tester=None):
    
    if tester is not None:
        args = tester

    else:
        args = parse_args()

    try:
        func = METHODS[args.mod_id]

        reward_matrix = read_map(args.filename, args.mod_id)

        Q_matrix = func(reward_matrix, args.yi, args.xi, args.n)
        
        output_matrix = build_output(Q_matrix, reward_matrix)
        
        print_output(output_matrix)
        
        if tester is not None:
            return output_matrix
        
    except KeyError:
        print(f"Error: The algorithm '{args.mod_id}' is not registered.")
        return -1
