import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml
import requests
import re

# open file with Twitter auth keys
with open("consumerkeys.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Variables with user credentials to access the Twitter API
CONSUMER_KEY = cfg["mysql"]["consumer_key"]
CONSUMER_SECRET = cfg["mysql"]["consumer_secret"]
ACCESS_TOKEN = cfg["mysql"]["access_token"]
ACCESS_SECRET = cfg["mysql"]["access_secret"]

class StdOutListener(StreamListener):
	def on_data(self, data):
		with open('political_tweets.json', 'a') as twitter_feed:
			twitter_feed.write(data)
		return True

	def on_error(self, status):
		print (status)
		return True

if __name__ == '__main__':
	# This handles Twitter authentication and the connection to Twitter REST & Streaming API
	# import pdb; pdb.set_trace()

	l = StdOutListener()

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

	api = tweepy.API(auth)
	stream = Stream(auth, l)

	top_trends = api.trends_place(23424775) # Canada

	# Parsing JSON & collecting hashtags for future tracking
	data = top_trends[0]
	trends = data['trends']
	names = [trend['name'] for trend in trends]
	trendsName = ' '.join(names)
	find_trend_hashtags = re.findall(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", trendsName)
	collect_trends = ' '.join(find_trend_hashtags).replace('#', '').split()
	
	response = stream.filter(track=collect_trends)
	















