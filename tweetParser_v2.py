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


"""method updates the dictionary kept locally keeping the count of the respective tweets"""

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

    #If the software is running with a single process, the size is 1 and hence the block below is called

    if size == 1:
        line = filehandle.readline()
        if not line:
            dict_sorted =  sorted(dict_of_tweets.items(),key=lambda x: x[1])
            print(dict_sorted[-10:])
            lang_sorted = sorted(dict_of_lang.items(),key=lambda x: x[1])
            print(lang_sorted[-10:])
            break
        tweets = []
        if "text" in line:
            tweets = re.findall('(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',line)
            dict_of_tweets = tweetsToDict(tweets, dict_of_tweets)

        if 'lang' in line:
            line_dict = json.loads(line.rstrip(",\n"))
            language = line_dict['doc']['lang']
            if language in dict_of_lang:
                dict_of_lang[language] += 1
            else:
                dict_of_lang[language] = 1


    #If the software is run on multiple processes the following block is called 

    else:

        """The first process reads a line and send the line to the second process and fourth processes"""

        if rank == 0:
            line = filehandle.readline()
            if line:
                comm.send(line, dest=1)
                comm.send(line, dest=3)
            if not line: #if no line is left to read, a break command is sent to processes 2 and 4
                comm.send("break", dest=1) #check for tweets
                comm.send("break", dest=3) #check for language handle
                break

        
        
        elif rank == 1:
            line = comm.recv(source=0)
            if line == "break":
                comm.send("break",dest=2)
                break

            """ check the line for the presence of the text, then uses regex to find the tweets"""

            if "text" in line:
                tweets = re.findall('(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',line)
                comm.send(tweets, dest=2)
            else:
                comm.send("None",dest=2)
            

        """ collect tweets and language, updates local dictionary and the prints the output once the file has been completely read """
            
        elif rank == 2:
            tweets = comm.recv(source=1)
            dict_of_tweets = tweetsToDict(tweets, dict_of_tweets)
            if tweets == "break":
                dict_sorted =  sorted(dict_of_tweets.items(),key=lambda x: x[1])
                print(dict_sorted[-10:])

            language = comm.recv(source=3)
            if language in dict_of_lang:
                dict_of_lang[language] += 1
            else:
                dict_of_lang[language] = 1
            if language == "break":
                lang_sorted = sorted(dict_of_lang.items(),key=lambda x: x[1])
                print(lang_sorted[-10:])
                break


        """ checks the language and sends it to the third process  """

        elif rank == 3:
            line = comm.recv(source=0)
            if line == "break":
                comm.send("break",dest=2)
                break

            if 'lang' in line:
                line_dict = json.loads(line.rstrip(",\n"))
                language = line_dict['doc']['lang']
                comm.send(language,dest=2)
            else:
                comm.send("None",dest=2)
    
        



    
