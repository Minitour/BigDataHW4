import json
import requests
import re

url = "https://api.iextrading.com/1.0/ref-data/symbols"
headers = {'cache-control': 'no-cache'}
response = requests.request("GET", url, headers=headers)
data = json.loads(response.text)

name_symbol_map = {}
symbo_name_map = {}
single_words_dict = {}

for company in data:
    symbol = company['symbol']
    name = company['name']
    name = re.sub(r'[^a-zA-Z ]', r'', name).lower()
    name = re.sub(' +', ' ', name)
    if len(name) != 0:
        name_symbol_map[name] = symbol

    symbo_name_map[symbol] = name

# for each company name
for key in name_symbol_map:
    # for each word in the comapny name
    for word in key.split(" "):
        if word in single_words_dict:
            arr = single_words_dict[word]
        else:
            # first time appending the word
            arr = []
        arr.append({'index': key, 'weight': (len(word) / len(key))})
        single_words_dict[word] = arr


def get_symbol(tweet):
    '''
    :param tweet: The tweet from which we want to extract the stock symbol
    :return: None if not found or tuple (company_stock,accuracy)
    '''
    # strip tweet from non english chars
    tweet = re.sub(r'[^a-zA-Z ]', r'', tweet).lower()
    tweet = re.sub(' +', ' ', tweet)

    score_map = {}

    # for each word
    for word in tweet.split(" "):
        if word in single_words_dict:
            # look up results
            lookup_res = single_words_dict[word]

            for company_index in lookup_res:
                company_name = company_index['index']
                company_index_score = company_index['weight']

                if company_name in score_map:
                    score_map[company_name] += company_index_score
                else:
                    score_map[company_name] = company_index_score

    maxi = 0
    maxc = None
    for key, val in score_map.items():
        if val > maxi:
            maxc = key
            maxi = val

    if maxc is not None:
        return name_symbol_map[maxc], maxi
