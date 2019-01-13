import re
import nltk
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()


def stem_tokens(tokens, stemmer):
    stemmed = [stemmer.stem(item) for item in tokens]
    return (stemmed)


def tokenize(text):
    text = re.sub("[^a-zA-Z]", " ", text)
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return (stems)


vectorizer = CountVectorizer(
    analyzer='word',
    tokenizer=tokenize,
    lowercase=True,
    stop_words='english',
    max_features=85
)


def get_features_train(list_of_strings):
    """

    :param list_of_strings:  list of strings
    :return: features array
    """
    return vectorizer.fit_transform(list_of_strings)


def get_features(list_of_strings):
    return vectorizer.transform(list_of_strings)
