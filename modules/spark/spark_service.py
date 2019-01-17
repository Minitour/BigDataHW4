import json
from datetime import datetime

import requests
from pyspark import SparkConf, SparkContext
from pyspark.sql import Row, SQLContext
from pyspark.streaming import StreamingContext

from modules.nlp.predict import predict
from modules.spark.symbol_lookup import get_symbols, symbol_name_map

import os

os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3'

# create spark configuration
conf = SparkConf()
conf.setAppName("TweeStocks")

# create spark instance with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

# creat the Streaming Context from the above spark context with window size 2 seconds
ssc = StreamingContext(sc, 2)

# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_1")

# read data from servers
iex_service_stream = ssc.socketTextStream("localhost", 3001)
twitter_service_stream = ssc.socketTextStream("localhost", 9009)

iex_sub_server = "http://localhost:3000/api/subscribe"
flask_server = "http://localhost:5001/"


def notify_iex(symbols_df):
    """
    makes an api call to the iex server to subscribe for symbols.
    :param symbols_df:
    """
    stock_symbols = [str(t.stock_symbol) for t in symbols_df.select("stock_symbol").collect()]

    for symbol in stock_symbols:
        payload = '{"symbol" : "%s"}' % symbol
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
        requests.request("POST", iex_sub_server, data=payload, headers=headers)


def notify_server(tweets):
    """
    This function sends tweets data to the flask server.
    :param tweets: tweets dataframe from which collect the data.
    """
    user_ids = [str(t.user_id) for t in tweets.select("user_id").collect()]
    followers = [str(t.followers) for t in tweets.select("followers").collect()]
    tweet_ids = [str(t.tweet_id) for t in tweets.select("tweet_id").collect()]
    sentimental_scores = [str(t.sentimental_score) for t in tweets.select("sentimental_score").collect()]

    res = []

    for a, b, c, d in zip(user_ids, followers, tweet_ids, sentimental_scores):
        res.append({'user_id': a, 'followers': b, 'tweet_id': c, 'score': d})

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    payload = json.dumps({'data': res})
    try:
        requests.request("POST", flask_server + 'updateTweets', data=payload, headers=headers)
    except:
        print("unreachable server")


def notify_server_stocks(stocks_df):
    # select symbol,askPrice,lastSaleTime,ti
    # mestamp from stocks

    symbols = [str(t.symbol) for t in stocks_df.select("symbol").collect()]
    askPrices = [str(t.askPrice) for t in stocks_df.select("askPrice").collect()]
    lastSaleTimes = [str(t.lastSaleTime) for t in stocks_df.select("lastSaleTime").collect()]
    timestamps = [int(t.timestamp) for t in stocks_df.select("timestamp").collect()]

    comps = {}

    res = []

    for symbol, askPrice, lastSaleTime, ts in zip(symbols, askPrices, lastSaleTimes, timestamps):
        obj = {'symbol': symbol, 'ask_price': askPrice, 'last_sale_time': lastSaleTime, 'timestamp': ts}
        res.append(obj)

        if symbol not in comps:
            comps[symbol] = symbol_name_map[symbol]

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    payload = json.dumps({'data': res, 'companies': comps})
    try:
        requests.request("POST", flask_server + 'updateStocks', data=payload,headers=headers)
    except:
        print("unreachable server")


def get_sql_context_instance(spark_context):
    if 'sqlContextSingletonInstance' not in globals():
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']


def json_map(obj):
    """
    converts string to json object
    :param obj:
    :return:
    """
    try:
        return json.loads(obj)
    except:
        return {}


def ts_map(js_obj):
    """
    converts json object to tuple (user_id,followers,tweet,tweet_id)
    :param js_obj:
    :return:
    """
    return js_obj['user_id'], js_obj['followers'], js_obj['tweet'], js_obj['tweet_id']


def ts_sent_score_map(tuple):
    """
    :param tuple: (user_id,followers,tweet,tweet_id)
    :return: (user_id,followers,tweet,tweet_id,sentimental_score)
    """
    return tuple[0], tuple[1], tuple[2], tuple[3], predict(tuple[2])


def ts_stock_flat_map(tuple):
    """
    :param tuple: (user_id,followers,tweet,sentimental_score)
    :return: list[(user_id,followers,tweet,sentimental_score,stock_symbol,company_name,confidence)]
    """
    symbols = get_symbols(tuple[2])
    res = []
    for item in symbols:
        res.append((tuple[0],  # user_id
                    tuple[1],  # followers
                    tuple[2],  # tweet (text)
                    tuple[3],  # tweet_id
                    tuple[4],  # sentimental score
                    item[0],  # symbol
                    item[1],  # company name
                    item[2]))  # confidence
    return res


def ts_rdd_process(time, rdd):
    if rdd.isEmpty():
        return

    sql_context = get_sql_context_instance(rdd.context)

    row_rdd = rdd.map(lambda w: Row(user_id=w[0],
                                    followers=w[1],
                                    tweet=w[2],
                                    tweet_id=w[3],
                                    sentimental_score=w[4],
                                    stock_symbol=w[5],
                                    company_name=w[6],
                                    confidence=w[7]))

    entries = sql_context.createDataFrame(row_rdd)
    entries.registerTempTable("entries")

    # notify IEX about symbols
    symbols_df = sql_context.sql("select stock_symbol from entries where confidence > 0.4")
    symbols_df = symbols_df.dropDuplicates()
    notify_iex(symbols_df)

    # notify flask server about tweets
    tweets = sql_context.sql("select user_id,followers,tweet_id,sentimental_score from entries")
    notify_server(tweets)


def iex_map(obj):
    if 'symbol' not in obj or 'lastSalePrice' not in obj or 'lastSaleTime' not in obj:
        return {}

    return obj['symbol'], obj['lastSalePrice'], obj['lastSaleTime'], datetime.now().microsecond


def iex_rdd_process(time, rdd):
    if rdd.isEmpty():
        return

    sql_context = get_sql_context_instance(rdd.context)

    row_rdd = rdd.map(lambda w: Row(symbol=w[0],
                                    askPrice=w[1],
                                    lastSaleTime=w[2],
                                    timestamp=w[3]))

    stocks = sql_context.createDataFrame(row_rdd)
    stocks.registerTempTable("stocks")

    stocks_df = sql_context.sql("select symbol,askPrice,lastSaleTime,timestamp from stocks order by timestamp desc")
    stocks_df = stocks_df.dropDuplicates()
    notify_server_stocks(stocks_df)


# setup iex stream pipeline
iex_service_stream \
    .map(json_map) \
    .map(iex_map) \
    .filter(lambda stock_data: stock_data[1] > 0)\
    .foreachRDD(iex_rdd_process)

# setup twitter stream pipeline
twitter_service_stream \
    .map(json_map) \
    .map(ts_map) \
    .map(ts_sent_score_map) \
    .flatMap(ts_stock_flat_map) \
    .foreachRDD(ts_rdd_process)

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
