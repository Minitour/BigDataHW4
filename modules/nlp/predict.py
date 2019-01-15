import pickle
from sklearn.externals import joblib
import os

from modules.nlp.vectorizer import get_features, vectorizer

filename = 'model.dat'

dir_path = os.path.dirname(os.path.realpath(__file__))
loaded_model = joblib.load(dir_path + '/' + filename)

vocabulary_to_load = pickle.load(open(dir_path + '/_voc', 'rb'))
vectorizer.vocabulary = vocabulary_to_load
vectorizer._validate_vocabulary()


def predict(text):
    features = get_features([text]).toarray()
    return loaded_model.predict(features)[0] == 'pos'
