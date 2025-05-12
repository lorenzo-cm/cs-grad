import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="QLearning")
    
    parser.add_argument('filename', type=str, help="Path to the map file.")
    parser.add_argument('mod_id', type=str, help="")
    parser.add_argument('xi', type=int,help="X")
    parser.add_argument('yi', type=int, help="Y")
    parser.add_argument('n', type=int, help="num steps")

    return parser.parse_args()