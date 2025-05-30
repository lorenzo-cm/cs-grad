from src import Processor, parse_args_processor

def main():
    args = parse_args_processor()
    processor = Processor(index_dir=args.i,
                          queries_path=args.q,
                          ranker=args.r)
    
    processor.run()

if __name__ == "__main__":
    main()
