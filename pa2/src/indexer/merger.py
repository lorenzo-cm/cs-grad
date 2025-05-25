import heapq, json, glob
from collections import defaultdict
import numpy as np
import os

INV_PATTERN   = "inv_idx_[0-9][0-9][0-9]"
LEX_PATTERN   = "lexicon_*.jsonl"
OUT_INV       = "inv_idx_final"
OUT_LEX       = "lexicon_final.jsonl"
BUFFER_SIZE   = 50_000

def generator(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

def push(it, fid, heap):
    try:
        line = next(it)
        term = line.split()[0]
        heapq.heappush(heap, (term, line, fid))
    except StopIteration:
        pass

def merge_indexes(index_dir):
    inv_paths = sorted(glob.glob(f'{index_dir}/{INV_PATTERN}'))
    lex_paths = sorted(glob.glob(f'{index_dir}/{LEX_PATTERN}'))
    iters = [generator(p) for p in inv_paths]
    heap = []
    
    # coloca primeira linha no heap
    for fid, it in enumerate(iters):
        push(it, fid, heap)

    # abrir arquivos para escrita via flush
    out_inv = open(f'{index_dir}/{OUT_INV}', "w", encoding="utf-8")
    out_lex = open(f'{index_dir}/{OUT_LEX}', "w", encoding="utf-8")

    lex_buffer = []
    term_id = 0
    
    list_sizes = []

    while heap:
        term, line, fid = heapq.heappop(heap)
        lines_same_term = [line]
        push(iters[fid], fid, heap)

        # pegar linhas com mesmo termo
        while heap and heap[0][0] == term:
            _, l2, fid2 = heapq.heappop(heap)
            lines_same_term.append(l2)
            push(iters[fid2], fid2, heap)

        # juntar linhas -> somar frequencias
        merged = defaultdict(int) # default value = 0
        for pl in lines_same_term:
            for pair in pl.split()[1:]:
                doc, freq = pair.split(":")
                merged[int(doc)] += int(freq)

        # escrever nova entrada
        offset = out_inv.tell()
        postings_sorted = " ".join(f"{d}:{merged[d]}" for d in sorted(merged))
        out_inv.write(f"{term} {postings_sorted}\n")

        lex_buffer.append(
            {"term": term,
             "id": term_id,
             "doc_freq": len(merged),
             "total_freq": sum(merged.values()),
             "offset": offset}
        )
        term_id += 1

        # flush (nao salvar toda hora p n ter overhead)
        if len(lex_buffer) >= BUFFER_SIZE:
            for e in lex_buffer:
                out_lex.write(json.dumps({e["term"]: e}) + "\n")
            lex_buffer.clear()
            
        list_sizes.append(len(merged))

    # flush final
    for e in lex_buffer:
        out_lex.write(json.dumps({e["term"]: e}) + "\n")

    out_inv.close()
    out_lex.close()
    
    avg_list_size = np.sum(list_sizes)/term_id if term_id else 0
    
    for path in inv_paths:
        os.remove(path)
        
    for path in lex_paths:
        os.remove(path)
    
    return term_id, float(avg_list_size)

if __name__ == "__main__":
    print(merge_indexes('index'))
