from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
from threading import Thread
import pandas as pd

class SentimentalAnalyzer:
    def __init__(self):
        """
        Initializes the SentimentalAnalyzer class.

        This constructor initializes the SentimentIntensityAnalyzer from the vaderSentiment library.
        """
        self.analyzer = SentimentIntensityAnalyzer()


    def polarity(self, phrase: str) -> int:
        """
        Calculates the polarity score of a given phrase.

        Args:
            phrase (str): The phrase for which the polarity score is calculated.

        Returns:
            int: The polarity score of the given phrase.
        """
        return self.analyzer.polarity_scores(phrase)['compound']


    def classify(self, phrase_or_score: str | float) -> int:
        """
        Classifies the sentiment of a given phrase or score.

        Args:
            phrase_or_score (str | float): The phrase or score to classify.

        Returns:
            int: The sentiment classification of the given phrase or score.
                 1: Positive sentiment
                 0: Neutral sentiment
                -1: Negative sentiment
        """
        score : float = 0
        if isinstance(phrase_or_score, str):
            score = self.analyzer.polarity_scores(phrase_or_score)['compound']
        else:
            score = phrase_or_score

        if score >= 0.05:
            return 1
        elif score <= -0.05:
            return -1
        else:
            return 0


    def classify_list(self, phrases: list[str]) -> list[int]:
        """
        Classifies the sentiment of a list of phrases.

        Args:
            phrases (list[str]): The list of phrases to classify.

        Returns:
            list[int]: The list of sentiment classifications corresponding to each input phrase.
        """
        return [self.classify(phrase) for phrase in tqdm(phrases)]


    def classify_list_parallel(self, phrases: list[str]) -> list[int]:
        """
        Classifies the sentiment of a list of phrases in parallel using threads.

        Args:
            phrases (list[str]): The list of phrases to classify.

        Returns:
            list[int]: The list of sentiment classifications corresponding to each input phrase.
        """
        scores = []

        def execute_classification(phrase: str):
            score = self.classify(phrase)
            scores.append(score)

        threads = []

        for phrase in tqdm(phrases):
            t = Thread(target=execute_classification, args=[phrase])
            threads.append(t)
            t.start()

        for t in tqdm(threads):
            t.join()

        return scores


    def classify_df(self, df: pd.DataFrame, column_name: str) -> list:
        """
        Classifies the sentiment of a DataFrame column containing phrases.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to classify.
            column_name (str): The name of the column to classify.

        Returns:
            list: a list with the polarities
        """
        return self.classify_list(df[column_name].tolist())


    def classify_df_parallel(self, df: pd.DataFrame, text_column_name: str, 
                             add_col: bool = False,
                             new_col_name: str = 'polarity') -> pd.DataFrame|list:
        """
        Classifies the sentiment of a DataFrame column containing phrases in parallel using threads.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to classify.
            column_name (str): The name of the column to classify.
            add_col (bool, optional): Whether to add a new column for sentiment classifications. Defaults to False.
            new_col_name (str, optional): The name of the new column to add for sentiment classifications. Defaults to 'sentiment'.

        Returns:
            pd.DataFrame: The modified DataFrame with an additional column containing sentiment classifications.
            or
            list: if add_col is False, returns a list containing polarities

        Notes:
            - If `add_col` is set to False, the sentiment classifications will replace the values in the `column_name` column.
            - If `add_col` is set to True, a new column with the name specified in `new_col_name` will be added to the DataFrame,
            containing the sentiment classifications.
        """
        df_new = pd.DataFrame()
        
        # add new col
        if add_col:
            df[new_col_name] = self.classify_list_parallel(df[text_column_name].tolist())

        # do not add new col and return just the polarities
        else:
            return self.classify_list_parallel(df[text_column_name].tolist())
            
        return df

