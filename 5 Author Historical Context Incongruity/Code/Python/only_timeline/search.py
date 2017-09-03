#print search data retrived
from TwitterSearch import *
import sys
import codecs
import nltk
import re
import time
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")


#Files
users_file = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/only_timeline/users','r',encoding='utf-8')
error404 = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/only_timeline/timelines/error404.txt','a',encoding='utf-8')
error401 = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/only_timeline/timelines/error401.txt','a',encoding='utf-8')
#TUO
ts = TwitterSearch(
                    consumer_key = 'RwfT7lMfFeVVlEUyyl4rhxd1f',
                    consumer_secret = 'BISoeO85xYQ4zmfNtbk8TFlxf459k1Zf3WOaD51rYTzmfr4B5y',
                    access_token = '122074593-d79A7JyAo5Zxm8J6sUlvlEyOjyv1zPSSRUHjNmCu',
                    access_token_secret = 'Dbl6JQmvxwXq1pMDbb9KnsysfFzUTELclLrbyRYSojjFo'
                    )
user = []
j =0
for test_tweet in users_file:
    words = test_tweet.split()  # list of words emoji and links
    user.append(words[0])
    saveFile = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/only_timeline/timelines/tweets'+str(j)+'.txt','w',encoding='utf-8')
    flag=1
    while flag==1:
            try:
                tuo = TwitterUserOrder(user[j])
                for tweet in ts.search_tweets_iterable(tuo):
                    if tweet['lang'] == 'en':
                        saveFile.write(tweet['text'])
                        saveFile.write('\n')
                flag = 0
            except TwitterSearchException as e: # take care of all those ugly errors if there are some 
                if str(e) == "Error 404: ('Not Found: The URI requested is invalid or', 'the resource requested does not exists')" :
                    flag =0 
                    error404.write(str(j))
                    error404.write('\n')
                elif str(e) == "Error 401: ('Unauthorized: Authentication credentials ', ' were missing or incorrect')":
                    flag = 0
                    error401.write(str(j))
                    error401.write('\n')
                else:
                    print(e)
                    time.sleep(100)  
    j+=1
saveFile.close()