import os

from flask import Flask, jsonify, request
from flask import render_template

template_dir = os.path.abspath('./../frontend')
print(template_dir)
app = Flask(__name__, template_folder=template_dir)

tweets = []
stocks = {}

tweet_index = set()


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
    body = request.get_json(silent=True)

    '''
    {
        "data" : [
            {
                "symbol" : "string",
                "ask_price" : "string",
                "last_sale_time" : "string",
                "timestamp" : 0
            }
        ],
        "companies" : {
            "symbol_x" : "string"
        }
    }
    '''

    data = body['data']
    companies = body['companies']

    for stock_data in data:
        symbol = stock_data['symbol']
        # if stock does not exist
        if symbol not in stocks:
            obj = {
                'companyName': companies[symbol],
                'stockPrices': [
                    {
                        'value': stock_data['ask_price'],
                        'timestamp': stock_data['timestamp']
                    }
                ]
            }
            stocks[symbol] = obj
        else:
            # add to existing stock
            stocks[symbol]['stockPrices'].append({'value': stock_data['ask_price'],
                                                  'timestamp': stock_data['timestamp']})

    return "{}", 200


@app.route("/updateTweets", methods=['POST'])
def update_tweet():
    """
    method to update the data (used by the spark service)
    :return:
    """
    global tweets
    global tweet_index

    '''
    {
        "data" : [
            {
                "user_id" : "str",
                "followers" : "str",
                "tweet_id" : "str,
                "score" : "str"
            }
        ]
    }
    '''

    body = request.get_json(silent=True)
    data = body['data']

    for item in data:
        if item['tweet_id'] not in tweet_index:
            tweets.append(item)
            tweet_index.add(item['tweet_id'])

    return "success", 200


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
