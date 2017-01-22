import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml

# open file with Twitter auth keys
with open("consumerkeys.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Variables with user credentials to access the Twitter API
CONSUMER_KEY = cfg["mysql"]["consumer_key"]
CONSUMER_SECRET = cfg["mysql"]["consumer_secret"]
ACCESS_TOKEN = cfg["mysql"]["access_token"]
ACCESS_SECRET = cfg["mysql"]["access_token_secret"]

class StdOutListener(StreamListener):
	def on_data(self, data):
		print (data)
		return True

	def on_error(self, status):
		# import pdb; pdb.set_trace()
		print (status)
		return True

if __name__ == '__main__':
	#This handles Twitter authetification and the connection to Twitter Streaming API
	# import pdb; pdb.set_trace()

	l = StdOutListener()
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	stream = Stream(auth, l)

	#This line filter Twitter Streams to capture data by the keywords:
	response = stream.filter(track=['WomensMarch'])

	# , 'ParachinarAttack', 'RigopianoHotel', 'Inaguration', 'Plascobuilding', 'ElChapo', 'GlobalWarming'], languages=['en']
















