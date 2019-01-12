from sklearn import model_selection
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle

from modules.nlp.nlp_vectorizer import get_features_train, vectorizer

# fetching traindata from files
data = []
data_labels = []
with open("traindata/pos_tweets.txt") as f:
    for i in f:
        data.append(i)
        data_labels.append('pos')
print(data)
with open("traindata/neg_tweets.txt") as f:
    for i in f:
        data.append(i)
        data_labels.append('neg')



# transforming the data into features vector and to array
features_nd = get_features_train(data).toarray()
binary_file = open('_voc',mode='wb')
pickle.dump(vectorizer.vocabulary_, binary_file)
binary_file.close()


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
joblib.dump(log_model, 'model.dat')
