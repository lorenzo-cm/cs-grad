# from googletrans import Translator as GoogleTranslator
from deep_translator import GoogleTranslator
from time import sleep
from threading import Thread
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class Translator:

    def __init__(self) -> None:
        self.translator = GoogleTranslator()
    
    
    def translate(self, text: str, language: str = 'auto'):
        try:
            translated_text = self.translator.translate(text, dest='en')
            return translated_text
        except:
            return ''


    def translate_list(self, texts: list):
        translated_texts = []
        for text in tqdm(texts):
            translated_text = self.translate(text)
            translated_texts.append(translated_text)
        return translated_texts


    # def translate_list_parallel(self, texts: list):

    #     translated_texts = []

    #     def execute_translation(text: str):
    #         translated_text = self.translate(text)
    #         translated_texts.append(translated_text)

    #     threads = []

    #     for text in tqdm(texts):
    #         t = Thread(target=execute_translation, args=[text])
    #         threads.append(t)
    #         t.start()

    #     print('Join Phase')

    #     for t in threads:
    #         t.join()

    #     print('Return Phase')
    
    #     return translated_texts

    def translate_list_parallel(self, texts: list):
        translated_texts = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.translate, text) for text in texts]

            for future in tqdm(as_completed(futures), total=len(texts)):
                translated_text = future.result()
                translated_texts.append(translated_text)

        return translated_texts


    def translate_df(self, df: pd.DataFrame, column_name: str):
        df[column_name] = self.translate_list(df[column_name].tolist())
        return df
    

    def translate_df_parallel(self, df: pd.DataFrame, column_name: str):
        df[column_name] = self.translate_list_parallel(df[column_name].tolist())
        return df