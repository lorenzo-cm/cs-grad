import json

def find_doc(file_path, doc_id):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for current_line, line in enumerate(file, start=1):
                if current_line == doc_id:
                    line = line.strip()
                    if line:
                        return json.loads(line)
                    else:
                        return None
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None


if __name__ == '__main__':
    id = 3442552
    documento = find_doc('data/corpus.jsonl', id)
    print(documento)