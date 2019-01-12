import pickle
from sklearn.externals import joblib

from modules.nlp.nlp_vectorizer import get_features, vectorizer

filename = 'model.dat'

loaded_model = joblib.load(filename)

vocabulary_to_load = pickle.load(open('_voc', 'rb'))
vectorizer.vocabulary = vocabulary_to_load
vectorizer._validate_vocabulary()


def predict(text):
    features = get_features([text]).toarray()
    print(features)

    return loaded_model.predict(features)


def test():
    tweet = "GitHub finally has unlimited free repositories! Well done Microsoft!"
    pred = predict(tweet)
    print(pred)


if __name__ == '__main__':
    test()
