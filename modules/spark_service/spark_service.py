from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SQLContext
import sys
import requests
import grequests
import json

from modules.nlp.predict import predict
from modules.spark_service.symbol_lookup import get_symbols

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

# read data from port 9009
twitter_service_stream = ssc.socketTextStream("localhost", 9009)
iex_service_stream = ssc.socketTextStream("localhost", 3001)

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
        grequests.request("POST", iex_sub_server, data=payload)


def notify_server(tweets):
    """
    This function sends tweets data to the flask server.
    :param tweets: tweets dataframe from which collect the data.
    """
    user_ids = [str(t.user_id) for t in tweets.select("user_id").collect()]
    followers = [str(t.follower) for t in tweets.select("follower").collect()]
    tweet_ids = [str(t.tweet_id) for t in tweets.select("tweet_id").collect()]
    sentimental_scores = [str(t.sentimental_score) for t in tweets.select("sentimental_score").collect()]

    res = []

    for a, b, c, d in zip(user_ids, followers, tweet_ids, sentimental_scores):
        res.append({'user_id': a, 'followers': b, 'tweet_id': c, 'score': d})

    payload = json.dumps({'data': res})
    grequests.request("POST", flask_server + '/updateTweets', data=payload)


def get_sql_context_instance(spark_context):
    if 'sqlContextSingletonInstance' not in globals():
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']


'''
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)



def send_df_to_dashboard(df):
    # extract the hashtags from dataframe and convert them into array
    top_tags = [str(t.hashtag) for t in df.select("hashtag").collect()]
    # extract the counts from dataframe and convert them into array
    tags_count = [p.hashtag_count for p in df.select("hashtag_count").collect()]
    # initialize and send the data through REST API
    url = 'http://localhost:5001/updateData'
    request_data = {'label': str(top_tags), 'data': str(tags_count)}
    response = requests.post(url, data=request_data)


def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        # Get spark sql singleton context from the current context
        sql_context = get_sql_context_instance(rdd.context)
        # convert the RDD to Row RDD
        row_rdd = rdd.map(lambda w: Row(hashtag=w[0], hashtag_count=w[1]))
        # create a DF from the Row RDD
        hashtags_df = sql_context.createDataFrame(row_rdd)
        # Register the dataframe as table
        hashtags_df.registerTempTable("hashtags")
        # get the top 10 hashtags from the table using SQL and print them
        hashtag_counts_df = sql_context.sql(
            "select hashtag, hashtag_count from hashtags order by hashtag_count desc limit 10")
        hashtag_counts_df.show()
        # call this method to prepare top 10 hashtags DF and send them
        send_df_to_dashboard(hashtag_counts_df)
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

'''


def ts_json_map(obj):
    """
    converts string to json object
    :param obj:
    :return:
    """
    return json.loads(obj)


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
                    item[0],   # symbol
                    item[1],   # company name
                    item[2]))  # confidence
    return res


def ts_rdd_process(time, rdd):
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
    entries.createOrReplaceGlobalTempView("entries")

    # notify IEX about symbols
    symbols_df = sql_context.sql("select stock_symbol from entries where confidence > 0.4")
    notify_iex(symbols_df)

    # notify flask server about tweets
    tweets = sql_context.sql("select user_id,follower,tweet_id,sentimental_score from entries")
    notify_server(tweets)


# setup twitter stream pipeline
twitter_service_stream \
    .map(ts_json_map) \
    .map(ts_map) \
    .flatMap(ts_stock_flat_map) \
    .foreachRDD(ts_rdd_process)

'''
# split each tweet into words
words = twitter_service_stream.flatMap(lambda line: line.split(" "))
# filter the words to get only hashtags, then map each hashtag to be a pair of (hashtag,1)
# hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))
hashtags = words.map(lambda x: (x, 1))
# adding the count of each hashtag to its last count
tags_totals = hashtags.updateStateByKey(aggregate_tags_count)
# do processing for each RDD generated in each interval
tags_totals.foreachRDD(process_rdd)
'''

"""
twitter_service_stream\
    .flatMap(lambda line: line.split(" "))\
    .filter(lambda w: '#' in w)\
    .map(lambda x: (x, 1))\
    .updateStateByKey(aggregate_tags_count)\
    .foreachRDD(process_rdd)
    
json (map) -> user_id,follower,tweet (map) -> [tweet,sent_analysis] (flatMap) -> [tweet, st_analysis, stock, confidence] (forEachRdd) -> processData

"""

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
