import json

def print_json_indexer(index_size, elapsed_time, number_of_lists, average_list_size):
    data = {
        "Index Size": index_size,
        "Elapsed Time": elapsed_time,
        "Number of Lists": number_of_lists,
        "Average List Size": average_list_size
    }
    print(json.dumps(data, indent=4))

def print_json_processor(query, results):
    ids, results = zip(*results) if results else ([], [])
    data = {
        "Query": query,
        "Results": [
            {
                "ID": ids[i],
                "Score": results[i]
            }
            for i in range(len(results))
        ]
    }
    print(json.dumps(data, indent=4))
