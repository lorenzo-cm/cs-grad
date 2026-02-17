import json
from threading import Lock

from numpy import mean
from src.preprocess import preprocess

term_id = 0

lexicon_lock = Lock()
doc_idx_lock = Lock()
inv_idx_lock = Lock()

sizes: list = []

def parse_doc(doc) -> tuple[int, str]:
    """Return id, parsed_text"""
    parsed_text = ''
    data = json.loads(doc)
    
    parsed_text += data['title']
    parsed_text += ' ' + data['text']
    parsed_text += ' ' + ' '.join(data['keywords'])

    return int(data['id']), parsed_text
    
def index_doc(inv_idx: dict[str, list[tuple[int, int]]],
              doc_idx: dict[int, dict],
              lexicon: dict[str, dict],
              doc: str,
              access_structures_lock: Lock) -> None:
    
    global term_id
    
    doc_id, text = parse_doc(doc)
    terms = preprocess(text)
    
    with doc_idx_lock:
        doc_idx[doc_id] = {
            'length': len(terms)
        }
    
    term_freq: dict = {}
    for term in terms:
        if term_freq.get(term, None) is None:
            term_freq[term] = 0
        
        term_freq[term] += 1
        
    with access_structures_lock:
        
        for term in term_freq:
            if lexicon.get(term, None) is None:
                lexicon[term] = {
                        'id': term_id,
                        'doc_freq': 0,
                        'total_freq': 0,
                    }
                term_id += 1
                
            lexicon[term]['doc_freq'] += 1
            lexicon[term]['total_freq'] += term_freq[term]
        
            if inv_idx.get(term, None) is None:
                inv_idx[term] = []
                
            inv_idx[term].append((doc_id, term_freq[term]))
