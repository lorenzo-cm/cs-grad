from src.utils import parse_args, read_map, invert_xy_path
from .settings import *
from src.algorithms import *

METHODS = {
    "BFS": bfs,
    "IDS": ids,
    "UCS": ucs,
    "Greedy": greedy,
    "Astar": astar,
}

def main(tester=None):
    
    if tester is not None:
        args = tester

    else:
        args = parse_args()

    try:
        func = METHODS[args.method]

        cost_matrix = read_map(args.filename)

        cost, path = func(cost_matrix, args.yi, args.xi, args.yf, args.xf)

        path = invert_xy_path(path)
        
        print(cost, *path)
        
    except KeyError:
        print(f"Error: The algorithm '{args.method}' is not registered.")
        return -1

    finally:
        if tester is not None:
            return cost,path