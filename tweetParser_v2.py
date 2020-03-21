import json
import re

tweet_list = []


filehandle = open("smallTwitter.json", 'r',encoding='utf-8')
while True:
    # read a single line
    line = filehandle.readline()
    if not line:
        break
        
    if "text" in line:
        """
        line_to_consider = line[:-1]
        tweet_row = json.loads(line_to_consider)
        tweet = tweet_row['doc']
        ind_tweet_text = tweet['text']
        """
        tweets = re.findall('(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',line)
        tweet_list += tweets
    



tweet_list.sort()


print(tweet_list)
print(len(tweet_list))