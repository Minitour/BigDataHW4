import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import pickle

stemmer = PorterStemmer()

# returning the stem to clean the text from lower cases -> we will send it to the CountVectorizer
def stem_tokens(tokens, stemmer):
    stemmed = [stemmer.stem(item) for item in tokens]
    return stemmed


# function to remove non-letters and stems
def tokenize(text):
    text = re.sub("[^a-zA-Z]", " ", text)
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return(stems)


# fetching tweets from files
data = []
data_labels = []
with open(".tweets/pos_tweets.txt") as f:
    for i in f:
        data.append(i)
        data_labels.append('pos')
print(data)
with open(".tweets/neg_tweets.txt") as f:
    for i in f:
        data.append(i)
        data_labels.append('neg')


vectorizer = CountVectorizer(
    analyzer = 'word',
    tokenizer = tokenize,
    lowercase = True,
    stop_words = 'english',
    max_features = 85
)


# transforming the data into features vector and to array
features = vectorizer.fit_transform(data)
features_nd = features.toarray()

X_train, X_test, y_train, y_test  = model_selection.train_test_split(
    features_nd[0:len(data)],
    data_labels,
    train_size=0.85,
    random_state=1234
)

# preparing for prediction
log_model = LogisticRegression()
log_model = log_model.fit(X=X_train, y=y_train)
y_pred = log_model.predict(X_test)

# The reported averages include micro average (averaging the
# total true positives, false negatives and false positives), macro
# average (averaging the unweighted mean per label), weighted average
# (averaging the support-weighted mean per label) and sample average
print(classification_report(y_test, y_pred))

# accurate of the algorithm
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

# finally we save the trained model into disk
filename = 'sentimental_score_nlp.sav'
pickle.dump(log_model, open(filename, 'wb'))
