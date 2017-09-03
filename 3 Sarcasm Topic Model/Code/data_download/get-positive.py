#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
 
from __future__ import print_function
import sys
import csv,codecs
 
from tweepy import StreamListener
 
import json, time, sys
#from __future__ import print_function
counter2 =0
class SListener(StreamListener):
 
    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
        self.output  = codecs.open(fprefix + '.'
                            + time.strftime('%Y%m%d-%H%M%S') + '.txt', 'w',encoding='UTF-8')
        self.delout  = open('delete.txt', 'a')
 
    def on_data(self, data):
 
 
 
        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print(warning['message'])
            return False
 
    def on_status(self, status):
 
 
        #if('"in_reply_to_status_id":null' not in status):
 	tweet=json.loads(status)
	
 	tlis=tweet['text'].split('\n') 
        
	self.output.write(' '.join(tlis) + "\n")
 
        self.counter += 1
        if(self.counter==10):
            print('\nstarted...')
        if(self.counter%100==0):
            print("")
            print (self.counter,end=',')
        elif (self.counter%10==0) :
            print(self.counter,end=',')
 
        return
 
    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return
 
    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return
 
    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False
 
    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return
 
 
 
 
#http://www.tweepy.org/
import tweepy
 
#Get your Twitter API credentials and enter them here
consumer_key = 'ilHNHwUrGChKQjoyeJwD1HDjz'
consumer_secret = 'kFicqTjlsmndG6bYnGjNEMYsQE5tHPaJLp1a1XjtTFzbtsKsIU'
 
access_key = '2928488004-lmPbmrtvPNUq2qu4rQ82Pu5dqxETrFqc0NkBuXP'
 
access_secret = 'dLoe1yxcuiSXHrtdMKNFgFVBAWbKcInoATYzbMGfvwfMc'
#method to get a user's last 100 tweets
def get_tweets():
 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
 
 
 
    
    while True : 
    	try:
		listen = SListener(api, 'Positive-tweets')
    		stream = tweepy.Stream(auth, listen)
    		print ("Streaming started...")
        	stream.filter(track = ['#happy','#excited'],languages=["en"])
    	except Exception,e:
 
        	print (str(e))
        	print("error")
        	stream.disconnect()
 		continue
 		
if __name__ == '__main__':
 
    get_tweets()
