"""
Project Name: TP ICD
Version: 1.0
Author: Lorenzo, Francisco
Date: June 28, 2023

Description:

-> Multithreaded Parallel Translation Processing

This code aims to provide an efficient solution for processing translations in parallel using multiple processes and threads.
It is specifically designed to leverage the capabilities of multicore CPUs with more than 13 cores.

To run on other datasets or other computers, remember to calculate the parameters again

The expected runtime is around 6 minutes on a ryzen 5700x

OBS: to see how the parameters are calculated, check the end of the file
"""



from deep_translator import GoogleTranslator
import pandas as pd
import multiprocessing
import threading
import time
from tqdm import tqdm


def translate(index, series_list):
    """
    Translates a series of texts using Google Translate and saves the translations to a CSV file.

    Args:
        index (int): The index of the series to translate.
        series_list (list): A list of series objects.

    Note:
        - The function uses the GoogleTranslator class from the Googletrans library to perform the translations.
        - The translated texts are saved to a CSV file named "{index}translation.csv" in the "./translationsLorenzo/" directory.
        - If an exception occurs during translation, the function will skip that particular text and continue with the remaining texts.
        - It is called by the parallel version of translate function to implement multiparallelism

    Example:
        >>> translate(0, [series1, series2, series3])
    """

    series = series_list[index]

    translated_texts = []

    translator = GoogleTranslator(source='auto', target='en')
    texts = series.to_list()

    for text in tqdm(texts):
        try:
            translated_text = translator.translate(text)
            translated_texts.append(translated_text)
        except:
            continue

    return pd.Series(translated_texts, name='text').to_csv(f'./translationsLorenzo/{index}translation.csv', index=False)


def translate_parallel(index, series_list):
    """
    Translates a series of texts in parallel by calling multiple threads with translate function.

    Args:
        index (int): The index of the series to translate.
        series_list (list): A list of series objects.

    Note:
        - The function creates multiple threads to perform translations in parallel.
        - Each thread calls the `translate` function with a different index, calculated based on the given index by the process and thread number.
        - The number of threads created is set to 10 in this implementation.
        - The function uses the `threading` module from the Python standard library.

    Example:
        >>> translate_parallel(0, [series1, series2, series3])
    """

    threads = []

    for _ in range(10):
        t = threading.Thread(target=translate, args=[index*10 + _, series_list])
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

# To execute the processes
if __name__ == '__main__':

    # Start the timer
    start = time.perf_counter()

    # Read the CSV file and extract the 'text' column
    df = pd.read_csv('../../data/chatgpt_daily_tweets.csv')
    df = df['text']

    # Limit the dataset to the first 60,000 rows (it has 66.000)
    df = df[0:60000]

    print(f'Shape of dataset: {df.shape}')

    # Create a list of Series to be passed as arguments to the function executed in threads (only solution found)
    series_list = []
    old_index = 0

    num_of_rows = 500 # the calculated is 500 (do not put a number > 500)

    # Split the data into smaller series of size num_of_rows
    for index in range(round((df.shape[0]) / 500)):
        series_list.append(df[old_index * num_of_rows:(index + 1) * num_of_rows])
        # print(f'{old_index * 500}:{(index + 1) * 500}')
        old_index = index + 1

    print(f'len data_set: {len(series_list)}')

    max_processes = multiprocessing.cpu_count()
    processes = []
    num_of_processes = 12

    if num_of_processes >= max_processes:
        raise Exception(f'Number of processes must be less than {max_processes}')
    
    # Create and start multiple processes for parallel translation
    for _ in range(num_of_processes):
        p = multiprocessing.Process(target=translate_parallel, args=[_, series_list])
        p.start()
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Finish the counter
    finish = time.perf_counter()

    print(f'Time taken: {finish - start} seconds')


"""
How it is calculated

Variables:
    - Num of lines of the dataset -> N
    - Num of cores to be used -> C
    - Num of threads to be used -> T
    - Num of samples per Thread -> S

Goal:
    - Decide S

Decisions:
    - Determine how many cores wil be used
    - Determine how many threads wil be used

Result:
    S = N / C * t


Observations:
    - It is not good to hardly overload the CPU
"""