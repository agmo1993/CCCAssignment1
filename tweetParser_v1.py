import json
import re

with open('smallTwitter.json', 'r', encoding='utf-8') as f:
    tweets = json.load(f) # load it as Python dict


tweet_rows = tweets.get('rows')

tweet_list = []

for i in tweet_rows:
    tweet = i['doc']
    ind_tweet_text = tweet['text']
    tweets = re.findall('(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',ind_tweet_text)
    tweet_list += tweets

tweet_list.sort()

print(tweet_list)