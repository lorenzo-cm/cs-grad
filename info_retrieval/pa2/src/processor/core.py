from src.utils import (
    read_inv_idx,
    read_doc_idx,
    read_lexicon,
    read_queries,
    print_json_processor,
)
from .rankers import tfidf, bm25


class Processor:
    def __init__(self, index_dir, queries_path, ranker):

        self.index_dir = index_dir
        self.queries_path = queries_path
        self.ranker = ranker

        self._init_index()

    def run(self):
        queries = read_queries(self.queries_path)
        for query in queries:
            results = self.query(query, self.ranker, top_k=10, is_conjuctive=True)
            print_json_processor(query, results)

    def query(self, query, ranker, top_k=10, is_conjuctive=True):
        results = []
        if ranker == "TFIDF":
            results = tfidf(
                inv_idx=self.inv_idx,
                doc_idx=self.doc_idx,
                lexicon=self.lexicon,
                query=query,
                top_k=top_k,
                is_conjuctive=is_conjuctive,
            )

        elif ranker == "BM25":
            results = bm25(
                inv_idx=self.inv_idx,
                doc_idx=self.doc_idx,
                lexicon=self.lexicon,
                query=query,
                k=1.2,
                b=0.75,
                top_k=top_k,
                is_conjuctive=is_conjuctive,
            )

        return results

    def _init_index(self):
        self.inv_idx = read_inv_idx(self.index_dir)
        self.doc_idx = read_doc_idx(self.index_dir)
        self.lexicon = read_lexicon(self.index_dir)
        # print('finish loading')
