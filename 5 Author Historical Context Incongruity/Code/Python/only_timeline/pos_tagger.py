#print search data retrived
from TwitterSearch import *
import sys
import codecs
import nltk
import re
import time
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")

class Emoticons:
    POSITIVE = ["*O","*-*","*O*","*o*","* *",
                ":P",":D",":d",":p",
                ";P",";D",";d",";p",
                ":-)",";-)",":=)",";=)",
                ":<)",":>)",";>)",";=)",
                "=}",":)","(:;)",
                "(;",":}","{:",";}",
                "{;:]",
                "[;",":')",";')",":-3",
                "{;",":]",
                ";-3",":-x",";-x",":-X",
                ";-X",":-}",";-=}",":-]",
                ";-]",":-.)",
                "^_^","^-^"]

    NEGATIVE = [":(",";(",":'(",
                "=(","={","):",");",
                ")':",")';",")=","}=",
                ";-{{",";-{",":-{{",":-{",
                ":-(",";-(",
                ":,)",":'{",
                "[:",";]"
                ]

class ParseTweet:
    # compile once on import
    regexp = {"RT": "^RT", "MT": r"^MT", "ALNUM": r"(@[a-zA-Z0-9_]+)",
              "HASHTAG": r"(#[\w\d]+)", "URL": r"([https://|http://]?[a-zA-Z\d\/]+[\.]+[a-zA-Z\d\/\.]+)",
              "SPACES":r"\s+"}
    regexp = dict((key, re.compile(value)) for key, value in regexp.items())

    def __init__(self, timeline_owner, tweet):
        """ timeline_owner : twitter handle of user account. tweet - 140 chars from feed; object does all computation on construction
            properties:
            RT, MT - boolean
            URLs - list of URL
            Hashtags - list of tags
        """
        self.Owner = timeline_owner
        self.tweet = tweet
        self.UserHandles = ParseTweet.getUserHandles(tweet)
        self.Hashtags = ParseTweet.getHashtags(tweet)
        self.URLs = ParseTweet.getURLs(tweet)
        self.RT = ParseTweet.getAttributeRT(tweet)
        self.MT = ParseTweet.getAttributeMT(tweet)
        self.Emoticon = ParseTweet.getAttributeEmoticon(tweet)
        
        # additional intelligence
        if ( self.RT and len(self.UserHandles) > 0 ):  # change the owner of tweet?
            self.Owner = self.UserHandles[0]
        return

    def __str__(self):
        """ for display method """
        return "owner %s, urls: %d, hashtags %d, user_handles %d, len_tweet %d, RT = %s, MT = %s" % (
        self.Owner, len(self.URLs), len(self.Hashtags), len(self.UserHandles), len(self.tweet), self.RT, self.MT)

    @staticmethod
    def getAttributeEmoticon(tweet):
        """ see if tweet is contains any emoticons, +ve, -ve or neutral """
        emoji = list()
        for tok in re.split(ParseTweet.regexp["SPACES"],tweet.strip()):
            if tok in Emoticons.POSITIVE:
                emoji.append( tok )
                continue
            if tok in Emoticons.NEGATIVE:
                emoji.append( tok )
        return emoji
    
    @staticmethod
    def getAttributeRT(tweet):
        """ see if tweet is a RT """
        return re.search(ParseTweet.regexp["RT"], tweet.strip()) != None

    @staticmethod
    def getAttributeMT(tweet):
        """ see if tweet is a MT """
        return re.search(ParseTweet.regexp["MT"], tweet.strip()) != None

    @staticmethod
    def getUserHandles(tweet):
        """ given a tweet we try and extract all user handles in order of occurrence"""
        return re.findall(ParseTweet.regexp["ALNUM"], tweet)

    @staticmethod
    def getHashtags(tweet):
        """ return all hashtags"""
        return re.findall(ParseTweet.regexp["HASHTAG"], tweet)

    @staticmethod
    def getURLs(tweet):
        """ URL : [http://]?[\w\.?/]+"""
        return re.findall(ParseTweet.regexp["URL"], tweet)

def rm(word):
    words=[]
    for wd1 in word:
        #print wd[:3]
        #if wd not in cachedStopWords:
            if wd1 in (',','.',"'",'"',';','?'):
                continue
            if wd1[-1] in (',','.',"'",'"',';','?'):
                wd = wd1[:len(wd1)-1]
            else :
                wd =wd1
            if wd.lower() == '#sarcasm':
                continue
            if wd[:4]=='http':
                continue
            emoji = ParseTweet.getAttributeEmoticon(wd)
            if len(emoji)>0:
                continue
            rt = ParseTweet.getAttributeRT(wd)
            if rt:
                continue
            #usr = ParseTweet.getUserHandles(wd)
            if wd[0]=='@':
                continue
            if wd[:2]=='\u': ## takes in account the unicode characters that havent been converted to ascii
                continue
            words.append(wd)
    return words

#Files
users_file = codecs.open('/Users/slfrawesome/Desktop/CD/Data/users','r',encoding='utf-8')
pos_file = codecs.open('/Users/slfrawesome/Desktop/CD/Data/positivetext','r',encoding='utf-8')
neg_file = codecs.open('/Users/slfrawesome/Desktop/CD/Data/negativetext','r',encoding='utf-8')
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
for users in users_file:
    words = test_tweet.split()  # list of words emoji and links
    user.append(words[0])

j =0
for test_tweet in pos_file:
    words = test_tweet.split()  # list of words emoji and links
    ln=rm(words)  # removing everything other then words
    line = ""
    for wd in ln:
        line = line +wd+" "
    text=nltk.word_tokenize(line)
    tagged_sent = nltk.pos_tag(text)
    nnp = []
    nnp = [word for word,pos in tagged_sent if pos == 'NNP']
    saveFile = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/only_timeline/_only_NNP/tweets'+str(j)+'.txt','w',encoding='utf-8')
    flag=1
    while flag==1:
            try:
                tuo = TwitterUserOrder(user[j])
                for tweet in ts.search_tweets_iterable(tuo):
                    if tweet['lang'] == 'en':
                        for nnpp in nnp:
                            if tweet['text'].lower().count(nnpp):
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
for test_tweet in neg_file:
    words = test_tweet.split()  # list of words emoji and links
    ln=rm(words)  # removing everything other then words
    line = ""
    for wd in ln:
        line = line +wd+" "
    text=nltk.word_tokenize(line)
    tagged_sent = nltk.pos_tag(text)
    nnp = []
    nnp = [word for word,pos in tagged_sent if pos == 'NNP']
    saveFile = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/tweets'+str(j)+'.txt','w',encoding='utf-8')
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