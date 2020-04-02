import json
import re

with open('smallTwitter.json', 'r', encoding='utf-8') as f:
    tweets = json.load(f) # load it as Python dict
# empty dictionaries for tweet and lang
tweet_dic = {}
lang_dic = {}

tweet_rows = tweets.get('rows')

tweet_list = []

for i in tweet_rows:
    tweet = i['doc']
    ind_tweet_text = tweet['text']
    tweets = re.findall('(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',ind_tweet_text)
    tweet_list += tweets
#tweet_list.lower()

# finding hastag tweets
for h_tweet in tweet_list:
    if h_tweet in tweet_dic:
        tweet_dic[h_tweet] = tweet_dic[h_tweet] + 1
    else:
        tweet_dic[h_tweet] = 1

#counding lang of tweets

for lang_data in tweet_rows:
    h_lang = lang_data['doc']['metadata']['iso_language_code']
    if h_lang in lang_dic:
        lang_dic[h_lang] = lang_dic[h_lang] + 1
    else:
        lang_dic[h_lang] = 1


sorted_hastag = sorted(tweet_dic.items(), reverse = True, key=lambda item: item[1])[:10]
sorted_lang = sorted(lang_dic.items(), reverse = True, key=lambda item: item[1])[:10]
print(sorted_hastag)
print(sorted_lang)



