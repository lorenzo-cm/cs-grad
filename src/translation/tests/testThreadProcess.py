from googletrans import Translator
import pandas as pd
import multiprocessing
import threading
import time
from tqdm import tqdm

def translate(series: pd.Series, target_language: str = 'en') -> pd.Series:
    translated_texts = []

    translator = Translator()
    texts = series.to_list()

    for text in tqdm(texts):
        try:
            translated_text = translator.translate(text, dest='en')
        except:
            continue
        translated_texts.append(translated_text.text)

    return pd.Series(translated_texts)

df = pd.read_csv('../../data/chatgpt_daily_tweets.csv')
df = df['text']

print(f'Shape of dataset: {df.shape}')
data_set = []
old_index = 0
for index in range(round((df.shape[0]) / 1000)):
    data_set.append(df[old_index * 1000:(index + 1) * 1000])
    old_index = index + 1


def translate_parallel(list_of_series, index):
    threads = []

    for _ in range(10):
        index_of_data_set = index * 10 + _
        t = threading.Thread(target=translate, args=(data_set[index_of_data_set], 'en'))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()


if __name__ == '__main__':
    start = time.perf_counter()

    processes = []
    num_of_processes = 12
    for _ in range(num_of_processes):
        p = multiprocessing.Process(target=translate_parallel, args=(data_set, _))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    finish = time.perf_counter()

    print(f'Time taken: {finish - start} seconds')
