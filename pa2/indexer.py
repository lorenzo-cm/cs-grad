from src import Indexer, parse_args_indexer, current_mem

def main():
    args = parse_args_indexer()
    indexer = Indexer(mem_limit=args.m, 
                      corpus_path=args.c, 
                      index_dir=args.i, 
                      num_threads=24,
                      lines_limit=300_000)
    
    indexer.run()

if __name__ == "__main__":
    main()
