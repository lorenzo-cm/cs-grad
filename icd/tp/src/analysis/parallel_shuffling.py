"""
Project Name: TP ICD
Version: 1.0
Author: Lorenzo, Francisco
Date: June 28, 2023
"""


import numpy as np
import pandas as pd
import multiprocessing
import threading
import time
from tqdm import tqdm


def calc_obs(df):
    return df.groupby('Language')['polarity'].sum()/df.groupby('Language')['polarity'].count().tolist()

def shuffling(data: pd.DataFrame, list_to_append: list, seed):
    np.random.seed(seed)
    np.random.shuffle(data['Language'])
    obs: list = calc_obs(data)
    # list_to_append.append(obs)
    pd.DataFrame(obs).to_csv(f'./csvs/{seed}.csv')


def translate_parallel(data: pd.DataFrame, list_to_append:list, index):

    threads = []
    
    for _ in range(4):
        t = threading.Thread(target=shuffling, args=[data, list_to_append, index*12 + _])
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

# To execute the processes
if __name__ == '__main__':

    # Start the timer
    start = time.perf_counter()

    df = pd.read_csv('../../data/df_filtered_lang_classified.csv', dtype={'Likes': str, 'Retweets': str})
    df = df.drop(['Date', 'Likes', 'Retweets'], axis=1)

    max_processes = multiprocessing.cpu_count()
    processes = []
    num_of_processes = 12

    if num_of_processes >= max_processes:
        raise Exception(f'Number of processes must be less than {max_processes}')
    
    list_to_append = []

    # Create and start multiple processes for parallel translation
    for _ in range(num_of_processes):
        df_new = df.copy()
        p = multiprocessing.Process(target=translate_parallel, args=[df_new, list_to_append, _])
        p.start()
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    final_df = pd.DataFrame(list_to_append)
    final_df.to_csv('./porfavordeus.csv')

    # Finish the counter
    finish = time.perf_counter()

    print(f'Time taken: {finish - start} seconds')