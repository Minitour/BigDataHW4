import pickle
from sklearn.externals import joblib

from modules.nlp.vectorizer import get_features, vectorizer

filename = 'model.dat'

loaded_model = joblib.load(filename)

vocabulary_to_load = pickle.load(open('_voc', 'rb'))
vectorizer.vocabulary = vocabulary_to_load
vectorizer._validate_vocabulary()


def predict(text):
    features = get_features([text]).toarray()
    return loaded_model.predict(features)[0] == 'pos'
