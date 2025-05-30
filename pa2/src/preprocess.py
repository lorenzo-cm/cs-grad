from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import re

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
tokenizer = re.compile(r"[A-Za-z]+")

def preprocess(text: str) -> list[str]:
    """
    Tokenize in only letters and numbers
    Remove stop words
    Stem words
    Remove words with len 1
    """
    terms = []
    for match in tokenizer.finditer(text.lower()):
        term = match.group(0)
        if term not in stop_words:
            stemmed = stemmer.stem(term)
            if len(stemmed) > 1:
                terms.append(stemmed)
            
    return terms
