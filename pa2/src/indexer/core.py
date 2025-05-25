from threading import Lock, Thread
import time

from src.utils.print_json import print_json_indexer

from .mem_handler import MemHandler
from .index_doc import index_doc
from .merger import merge_indexes
from src.utils import get_folder_size

class Indexer:
    def __init__(self, mem_limit: int, corpus_path: str, index_dir: str, num_threads: int = 16, lines_limit=None):
        self.mem_limit = mem_limit
        self.corpus_path = corpus_path
        self.index_dir = index_dir
        
        self.inv_idx: dict[str, list[tuple[int, int]]] = {} # word -> [(id, freq), ..., (id, freq)] 
        self.doc_idx: dict[int, dict] = {} # doc -> len
        self.term_lexicon: dict[str, dict] = {} # offset, freq, doc-freq
        
        self.access_structures_lock = Lock()
        
        # MemHandler
        self.mem_handler = MemHandler(mem_limit=self.mem_limit,
                                       corpus_path=self.corpus_path,
                                       index_dir=self.index_dir,
                                       inv_idx=self.inv_idx,
                                       doc_idx=self.doc_idx,
                                       lexicon=self.term_lexicon,
                                       access_structures_lock=self.access_structures_lock,
                                       num_threads=num_threads,
                                       lines_limit=lines_limit)
        
        self.num_threads = num_threads
    
    def run(self):
        start_time = time.perf_counter()
        threads = [Thread(target=self.create_index) for _ in range(self.num_threads)]
        for t in threads: t.start()
        for t in threads: t.join()
        self.mem_handler._flush_and_save()
        num_lines, avg_inv_idx_size = merge_indexes(index_dir=self.index_dir)
        end_time = time.perf_counter() - start_time
        index_size = get_folder_size(self.index_dir)
        print_json_indexer(index_size, end_time, num_lines, avg_inv_idx_size)
    
    def create_index(self):
        while True:
            doc = self.mem_handler.read_line()
            if not doc:
                break
            
            # index docs
            index_doc(inv_idx=self.inv_idx,
                    doc_idx=self.doc_idx,
                    lexicon=self.term_lexicon,
                    doc=doc,
                    access_structures_lock=self.access_structures_lock)
        
    
    