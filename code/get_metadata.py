#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   /$$$$$$  /$$      /$$ /$$      /$$ /$$$$$$$$
#  /$$__  $$| $$$    /$$$| $$$    /$$$|__  $$__/
# | $$  \__/| $$$$  /$$$$| $$$$  /$$$$   | $$   
# |  $$$$$$ | $$ $$/$$ $$| $$ $$/$$ $$   | $$   
#  \____  $$| $$  $$$| $$| $$  $$$| $$   | $$   
#  /$$  \ $$| $$\  $ | $$| $$\  $ | $$   | $$   
# |  $$$$$$/| $$ \/  | $$| $$ \/  | $$   | $$   
#  \______/ |__/     |__/|__/     |__/   |__/  
#
#
# Developed during Biomedical Hackathon 6 - http://blah6.linkedannotation.org/
# Authors: Ramya Tekumalla, Javad Asl, Juan M. Banda
# Contributors: Kevin B. Cohen, Joanthan Lucero

import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
import argparse
import os
import os.path as osp
import pandas as pd
from tweepy import TweepError
from time import sleep


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outputfile", help="Output file name with extension")
    parser.add_argument("-i", "--inputfile", help="Input file name with extension")
    parser.add_argument("-k", "--keyfile", help="Json api key file name")
    parser.add_argument("-c", "--idcolumn", help="tweet id column in the input file, string name")
    parser.add_argument("-m", "--mode", help="Enter e for extended mode ; else the program would consider default compatible mode")
    parser.add_argument("-ll", "--lowerlimit", help="Lower limit of the tweets")
    parser.add_argument("-ul", "--upperlimit", help="Upper limit of the tweets")
    

    args = parser.parse_args()
    if args.inputfile is None or args.outputfile is None:
        parser.error("please add necessary arguments")
        
    if args.keyfile is None:
        parser.error("please add a keyfile argument")

    with open(args.keyfile) as f:
        keys = json.load(f)

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, retry_delay=60*3, retry_count=5,retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit_notify=True)
    
    if api.verify_credentials() == False: 
        print("Your twitter api credentials are invalid") 
        sys.exit()
    else: 
        print("Your twitter api credentials are valid.") 
    
    
    output_file = args.outputfile
    hydration_mode = args.mode

    output_file_noformat = output_file.split(".",maxsplit=1)[0]
    print(output_file)
    output_file = '{}'.format(output_file)
    output_file_short = '{}_short.json'.format(output_file_noformat)
    compression = zipfile.ZIP_DEFLATED    
    ids = []
    
    if '.tsv' in args.inputfile:
        inputfile_data = pd.read_csv(args.inputfile, sep='\t')
        print('tab seperated file, using \\t delimiter')
    elif '.csv' in args.inputfile:
        inputfile_data = pd.read_csv(args.inputfile)
    elif '.txt' in args.inputfile:
        inputfile_data = pd.read_csv(args.inputfile, sep='\n', header=None, names= ['tweet_id'] )
        print(inputfile_data)
    
    if not isinstance(args.idcolumn, type(None)):
        inputfile_data = inputfile_data.set_index(args.idcolumn)
    else:
        inputfile_data = inputfile_data.set_index('tweet_id')
    
    ids = list(inputfile_data.index)
    print('total ids: {}'.format(len(ids)))

    start = 0
    end = 100
    limit = len(ids)
    i = int(math.ceil(float(limit) / 100))
    lowlim = 0
    uplim = int(math.ceil(float(limit-start)))
    if(args.upperlimit is not None):
      uplim = int(args.upperlimit)
    if(args.lowerlimit is not None):
      lowlim = int(args.lowerlimit)
    last_tweet = None
    if osp.isfile(args.outputfile) and osp.getsize(args.outputfile) > 0:
        with open(output_file, 'rb') as f:
            #may be a large file, seeking without iterating
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
        last_tweet = json.loads(last_line)
        start = ids.index(last_tweet['id'])
        end = start+100

    print('metadata collection complete')
    print('creating master json file between the tweets {} and {}'.format(lowlim,uplim))
    print(uplim)
    print(lowlim)
    try:
        start += lowlim
        end = start+100
        forrange = int((uplim - lowlim)/100)
        with open(output_file, 'a') as outfile:
            for go in range(forrange):
                print('currently getting {} - {}'.format(start, end))
                # sleep(1)  # needed to prevent hitting API rate limit
                id_batch = ids[start:end]
                start += 100
                end += 100       
                backOffCounter = 1
                while True:
                    try:
                        if hydration_mode == "e":
                            tweets = api.statuses_lookup(id_batch,tweet_mode = "extended")
                        else:
                            tweets = api.statuses_lookup(id_batch)
                        break
                    except tweepy.TweepError as ex:
                        print('Caught the TweepError exception:\n %s' % ex)
                        sleep(30*backOffCounter)  # sleep a bit to see if connection Error is resolved before retrying
                        backOffCounter += 1  # increase backoff
                        continue
                for tweet in tweets:
                    json.dump(tweet._json, outfile)
                    outfile.write('\n')
    except:
        print('exception: continuing to zip the file')

    print('creating ziped master json file')
    zf = zipfile.ZipFile('{}.zip'.format(output_file_noformat), mode='w')
    zf.write(output_file, compress_type=compression)
    zf.close()


    def is_retweet(entry):
        return 'retweeted_status' in entry.keys()

    def get_source(entry):
        if '<' in entry["source"]:
            return entry["source"].split('>')[1].split('<')[0]
        else:
            return entry["source"]
    
    
    print('creating minimized json master file')
    with open(output_file_short, 'w') as outfile:
        with open(output_file) as json_data:
            for tweet in json_data:
                data = json.loads(tweet) 
                if hydration_mode == "e":
                    text = data["full_text"]
                else:
                    text = data["text"]
                          
                # When adding or removing fields, there are 3 places to make changes
                # First, make a change in the below dict t
                t = {
                    "user.id_str": data["user"]["id_str"],
                    # "retweeted_status.user.id_str": data["retweeted_status"]["user"]["id_str"],
                    "text": text,
                    "retweet_count": data["retweet_count"],
                    "favorite_count": data["favorite_count"],
                    "id_str": data["id_str"],
                    "is_retweet": is_retweet(data),
                    "user.followers_count": data["user"]["followers_count"],
                    "user.friends_count": data["user"]["friends_count"],
                    "user.favourites_count": data["user"]["favourites_count"],
                    "user.verified": data["user"]["verified"],
                    "user.name": data["user"]["name"],
                    # "entities.user_mentions": data["entities"]["user_mentions"]["id_str"]
                }
                # If the tweet is not a retweet, retweeted_user_id is assigned to -1
                if is_retweet(data):
                  t["retweeted_status.user.id_str"] = data["retweeted_status"]["user"]["id_str"]
                else:
                  t["retweeted_status.user.id_str"] = -1
                json.dump(t, outfile)
                outfile.write('\n')
        
    f = csv.writer(open('{}.csv'.format(output_file_noformat), 'w'))
    print('creating CSV version of minimized json master file') 
    # Secondly, make a change in the below fields list
    fields = ["user_id","retweeted_user_id","user_verified","user_followers_count","favorite_count","user_favourites_count","user_friends_count", "text", "is_retweet", "retweet_count","id_str" ] # ,"entities_user_mentions"              
    f.writerow(fields)       
    with open(output_file_short) as master_file:
        for tweet in master_file:
          data = json.loads(tweet)
          # Thirdly, make a change in the below writerow statement
          f.writerow([data["user.id_str"], data["retweeted_status.user.id_str"],data["user.verified"],data["user.favourites_count"],data["user.followers_count"],data["user.friends_count"],data["favorite_count"], data["text"].encode('utf-8'), data["is_retweet"], data["retweet_count"], data["id_str"]])
  
# main invoked here    
main()
