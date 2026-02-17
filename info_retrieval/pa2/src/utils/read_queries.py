def read_queries(queries_path):
    with open(queries_path, "r", encoding="utf-8") as f:
        queries = f.readlines()

    queries = [query.strip() for query in queries if query.strip()]
    return queries
