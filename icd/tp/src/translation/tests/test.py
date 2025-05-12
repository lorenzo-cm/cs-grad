from googletrans import Translator
from deep_translator import GoogleTranslator
import pandas as pd
import multiprocessing
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

df_new1 = df[0:1000]['text']
df_new2 = df[1000:2000]['text']
df_new3 = df[2000:3000]['text']
df_new4 = df[3000:4000]['text']

def translate_parallel(s):
    translate(s, target_language='en')
    print('finish')

p1 = multiprocessing.Process(target=translate_parallel, args=[df_new1])
p2 = multiprocessing.Process(target=translate_parallel, args=[df_new2])
p3 = multiprocessing.Process(target=translate_parallel, args=[df_new3])
p4 = multiprocessing.Process(target=translate_parallel, args=[df_new4])

if __name__ == '__main__':
    start = time.perf_counter()
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    finish = time.perf_counter()
    print(f'Time taken: {finish - start} ')