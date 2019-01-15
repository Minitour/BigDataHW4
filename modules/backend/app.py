import os

from flask import Flask, jsonify
from flask import render_template

template_dir = os.path.abspath('./../frontend')
print(template_dir)
app = Flask(__name__, template_folder=template_dir)

tweets = []
stocks = {}


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/getData", methods=['POST'])
def get_data():
    """
    method to fetch the data (used by the frontend)
    :return: the data (tweets + stocks)
    """
    global tweets, stocks
    return jsonify({'tweets': tweets, 'stocks': stocks})


@app.route("/updateStocks", methods=['POST'])
def update_stocks():
    """
    method to update the data (used by the spark service)
    :return:
    """
    global stocks
    # TODO: update stocks
    return "success", 200


@app.route("/updateTweets", methods=['POST'])
def update_tweet():
    """
    method to update the data (used by the spark service)
    :return:
    """
    global tweets
    # TODO: update traindata
    return "success", 200


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
