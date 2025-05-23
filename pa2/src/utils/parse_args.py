import argparse

def parse_args_indexer():
    parser = argparse.ArgumentParser(description="Indexer")
    parser.add_argument('-i', type=str, required=True, 
                        help='The path to the corpus file to be indexed')
    
    parser.add_argument('-m', type=int, required=True,
                        help='The memory available to the indexer in megabytes')
    
    parser.add_argument('-c', type=str, required=True,
                        help='The path to the corpus file to be indexed')

    return parser.parse_args()

def parse_args_processor():
    parser = argparse.ArgumentParser(description="Query Processor")
    parser.add_argument('-i', type=str, required=True, 
                        help='The path to an index file')
    
    parser.add_argument('-q', type=str, required=True,
                        help='The path to a file with the list of queries to process')
    
    parser.add_argument('-r', type=str, required=True,
                        help='Ranking function: TFIDF or BM25')

    return parser.parse_args()