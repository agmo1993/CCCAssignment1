import json
import re

import numpy as np
from mpi4py import MPI


tweet_list = []
dict_of_tweets = {}
dict_of_lang = {}

comm = MPI.COMM_WORLD

rank, size = comm.Get_rank(), comm.Get_size()

filehandle = open("smallTwitter.json", 'r',encoding='utf-8')

def tweetsToDict(tweetlist, tweetDict):
    for i in tweetlist:
        tweet = i.encode("UTF-8")
        if tweet in tweetDict:
            tweetDict[tweet] += 1
        else:
            tweetDict[tweet] = 1
    return tweetDict


comm.Barrier()

while True:
    
    if rank == 0:
        line = filehandle.readline()
        if line:
            comm.send(line, dest=1)
            comm.send(line, dest=3)
        if not line:
            comm.send("break", dest=1)
            comm.send("break", dest=3)
            break

    elif rank == 1:
        line = comm.recv(source=0)
        if line == "break":
            comm.send("break",dest=2)
            break

        if "text" in line:
            """
            line_to_consider = line[:-1]
            tweet_row = json.loads(line_to_consider)
            tweet = tweet_row['doc']
            ind_tweet_text = tweet['text']
            """
            tweets = re.findall('(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',line)
            comm.send(tweets, dest=2)
        else:
            comm.send("None",dest=2)
        

        
    elif rank == 2:
        tweets = comm.recv(source=1)
        dict_of_tweets = tweetsToDict(tweets, dict_of_tweets)
        if tweets == "break":
            dict_sorted =  sorted(dict_of_tweets.items(),key=lambda x: x[1])
            print(dict_sorted[-10:])
            break

    elif rank == 3:
        line = comm.recv(source=0)
        if line == "break":
            comm.send("break",dest=4)
            break

        if 'lang' in line:
            line_dict = json.loads(line.rstrip(",\n"))
            language = line_dict['doc']['lang']
            comm.send(language,dest=4)
        else:
            comm.send("None",dest=4)
    
    elif rank == 4:
        language = comm.recv(source=3)
        if language in dict_of_lang:
            dict_of_lang[language] += 1
        else:
            dict_of_lang[language] = 1
        if language == "break":
            lang_sorted = sorted(dict_of_lang.items(),key=lambda x: x[1])
            print(lang_sorted[-10:])
            break




    
