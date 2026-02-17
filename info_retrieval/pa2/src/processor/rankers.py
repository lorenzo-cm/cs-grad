from collections import defaultdict
import numpy as np
from src.preprocess import preprocess


def tfidf(
    inv_idx: dict[str, dict[int, int]],
    doc_idx: dict[int, dict],
    lexicon: dict[str, dict],
    query: str,
    top_k: int = 10,
    is_conjuctive=True,
) -> list[tuple[int, float]]:

    doc_scores: dict = defaultdict(float)

    # preprocess
    query_terms = preprocess(query)

    conjunctive_docs = conjunctive_daat(inv_idx, query_terms, is_conjuctive)
    num_docs = len(doc_idx)

    for doc_id in conjunctive_docs:
        score = 0.0

        for term in query_terms:
            if term in inv_idx and doc_id in inv_idx[term]:
                tf = inv_idx[term][doc_id]
                doc_len = doc_idx[doc_id]["length"]
                doc_freq = lexicon[term]["doc_freq"]

                normalized_tf = tf / doc_len
                idf = np.log((num_docs + 1) / doc_freq)
                score += normalized_tf * idf

        doc_scores[doc_id] = score

    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]


def bm25(
    inv_idx: dict[str, dict[int, int]],
    doc_idx: dict[int, dict],
    lexicon: dict[str, dict],
    query: str,
    k: float = 1.2,
    b: float = 0.75,
    top_k: int = 10,
    is_conjuctive=True
) -> list[tuple[int, float]]:

    doc_scores: dict = defaultdict(float)

    # preprocess
    query_terms = preprocess(query)

    conjunctive_docs = conjunctive_daat(inv_idx, query_terms, is_conjuctive)
    num_docs = len(doc_idx)

    if num_docs == 0:
        return []

    # calculate avg doc for BM25
    sum_length = sum(doc_idx[doc_id]["length"] for doc_id in doc_idx)
    avg_length = sum_length / num_docs

    for doc_id in conjunctive_docs:
        score = 0.0

        for term in query_terms:
            if term in inv_idx and doc_id in inv_idx[term]:
                tf = inv_idx[term][doc_id]
                doc_len = doc_idx[doc_id]["length"]
                doc_freq = lexicon[term]["doc_freq"]

                # TF
                numerator = tf * (k + 1)
                denominator = tf + k * (1 - b + b * (doc_len / avg_length))

                normalized_tf = numerator / denominator

                # IDF
                # did not used the one in the slides
                idf_numerator = num_docs - doc_freq + 0.5
                idf_denominator = doc_freq + 0.5
                idf = np.log(idf_numerator / idf_denominator)

                # BM25 score
                score += normalized_tf * idf

        doc_scores[doc_id] = score

    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]


def conjunctive_daat(
    inv_idx: dict[str, dict[int, int]],
    query_terms: list[str],
    is_conjuctive=True
) -> set[int]:

    # allow all docs
    if not is_conjuctive:
        return {doc_id for term in query_terms if term in inv_idx for doc_id in inv_idx[term].keys()}

    if not query_terms:
        return set()

    for term in query_terms:
        if term not in inv_idx:
            return set()

    candidate_docs = set(inv_idx[query_terms[0]].keys())

    # intersect with the next docs
    for term in query_terms:

        if term not in inv_idx:
            return set()

        term_docs = set(inv_idx[term].keys())
        candidate_docs = candidate_docs.intersection(term_docs)

        if not candidate_docs:
            break

    return candidate_docs
