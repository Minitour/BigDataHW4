import json
import socket

import pandas as pd
import requests
import requests_oauthlib

# lsof -n -i | grep -e LISTEN -e ESTABLISHED

# Replace the values below with yours
from modules.twitter.users_ids import get_users_usernames, get_users_ids

ACCESS_TOKEN = '1053037342867554304-LguUeIEnjsniVsy0EKvqJzI43jWjUz'
ACCESS_SECRET = 'wsPwYyszpUme2BlmlnwhNzwfM5R2pT5QwgOBjhojgl71O'
CONSUMER_KEY = 'GyMTfKuHNRZfLK1J61MH9wX69'
CONSUMER_SECRET = 'uTymrN5U5kc4uG5obNbX4VhzwrpRulAOKi2FZouxA1UHEoJnB0'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

use_top_500 = True

def load_users():
    usernames = get_users_usernames()
    ids = get_users_ids(usernames)
    return ids


def get_tweets(user_ids):
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    #user_ids = load_users()

    if use_top_500:
        condition = ('follow', ','.join(user_ids))
    else:
        condition = ('track', 'stock')

    query_data = [
        ('language', 'en'),
        condition
    ]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response


def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            json_str = line.decode("utf-8")
            full_tweet = json.loads(json_str)

            tweet_text = full_tweet['text']
            user_id = full_tweet['user']['id_str']
            tweet_id = full_tweet['id_str']
            followers = int(full_tweet['user']['followers_count'])

            obj = {'user_id': user_id,
                   'tweet': tweet_text,
                   'tweet_id': tweet_id,
                   'followers': followers}

            val = json.dumps(obj) + '\n'
            print(val)
            try:
                tcp_connection.send(val.encode())
            except:
                return
        except:
            print("failed decoding")


TCP_IP = "localhost"
TCP_PORT = 9009

# create socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

# allow only one conneciton
s.listen(1)
user_ids = load_users()
print(user_ids)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")
resp = get_tweets(user_ids)
send_tweets_to_spark(resp, conn)

