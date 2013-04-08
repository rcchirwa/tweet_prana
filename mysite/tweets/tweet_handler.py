from django.conf import settings

import tweepy
import json
import urllib2
import time
from collections import namedtuple
import re
import logging

#my keys pulled from a file which is git ignored
twitter_keys = settings.TWITTER_KEYS

access_token = twitter_keys['access_token'] 
access_token_secret =  twitter_keys['access_token_secret']

consumer_key = twitter_keys["consumer_key"]
consumer_secret = twitter_keys["consumer_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

'''
The function below is used to post a tweet to the timeline as well as 
collect information from twitter that we would like to house in our datastore
'''

def postTweet(tweet):

	tweet_text = tweet.tweet
	
	tester = api.update_status(tweet.tweet)

	date_time = '%s-%s-%s %s'  % (tester.created_at.year,tester.created_at.month,tester.created_at.day,tester.created_at.time())

	pattern = '%Y-%m-%d %H:%M:%S'

	#compute the related epoch
	epoch = int(time.mktime(time.strptime(date_time, pattern)))


	tweet = tweet_text
	id_str = tester.id_str 
	created_at_time_txt = date_time
	created_at = tester.created_at
	created_at_epoch = epoch
	retweet_count = tester.retweet_count

	tweetCallURL = "https://api.twitter.com/1/statuses/oembed.json?id=%s"%id_str

	p =  urllib2.urlopen(tweetCallURL)
	tweetObject = p.read()

	tweet = json.loads(tweetObject)

	#this is the raw html string produced  twitter is you want to repost the tweets
	html = tweet['html']

	#create a regular expression to strip the tweet 
	regex = re.compile("<blockquote class=\"twitter-tweet\">(.*)</blockquote>")
	stripped_html = regex.findall(html)[0]\

	#define tuple to return	
	TweetDetails = namedtuple('TweetDetails','id_str created_at_time_txt created_at created_at_epoch retweet_count html stripped_html')

	#assign values to namedtuple
	tweetDetails = TweetDetails(id_str,created_at_time_txt,created_at, created_at_epoch, retweet_count, html, stripped_html)
	
	#return named tuple
	return tweetDetails


