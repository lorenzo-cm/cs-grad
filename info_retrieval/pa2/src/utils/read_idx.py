import os
import json
from typing import Any


def read_inv_idx(
    index_dir, index_filename="inv_idx_final"
) -> dict[str, dict[int, int]]:
    inv_idx = {}
    index_file_path = os.path.join(index_dir, index_filename)

    with open(index_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()

            term = parts[0]
            postings = {}

            # doc_id:freq
            for posting in parts[1:]:
                if ":" in posting:
                    doc_id, freq = posting.split(":")
                    postings[int(doc_id)] = int(freq)

            inv_idx[term] = postings

    return inv_idx


def read_doc_idx(
    index_dir, index_filename="doc_idx.jsonl"
) -> dict[int, dict[str, Any]]:
    doc_idx = {}
    index_file_path = os.path.join(index_dir, index_filename)

    with open(index_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            data = json.loads(line)

            for str_doc_id, doc_data in data.items():
                int_doc_id = int(str_doc_id)  # "1" → 1
                doc_idx[int_doc_id] = doc_data

    return doc_idx


def read_lexicon(
    index_dir, index_filename="lexicon_final.jsonl"
) -> dict[str, dict[str, int]]:
    lexicon = {}
    index_file_path = os.path.join(index_dir, index_filename)

    with open(index_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)
            lexicon.update(data)

    return lexicon
