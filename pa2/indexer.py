from src import Indexer, parse_args_indexer

def main():
    args = parse_args_indexer()
    indexer = Indexer(mem_limit=args.m, 
                      corpus_path=args.c, 
                      index_dir=args.i, 
                      num_threads=16,
                      lines_limit=1_000_000)
    
    indexer.run()

if __name__ == "__main__":
    main()
