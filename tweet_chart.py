import json
import re
import operator
from collections import Counter
import string

# Words/Punctuation to be excluded from frequency check
punctuation = list(string.punctuation)
stop = punctuation + ['RT', 'via', 'the', '…', 'of', 'in', 'to', 
'and', 'is', 'for', 'a', 'I', 'at', 'you', 'today', 'are', 'be', 'this', 'the', 'This', 'The', 'women', 'all', 'my', 'that',
'so', 'it', 'on', 'with', 'from', 'not', 'was', 'de', 'amp', 'our', 'we', 'We', '@womensmarch', 'I\'m', 'who', '#womensmarch', '#WomensMarch', 'have',
'what', 'they', 'as', 'up', 'her', '\'', 'day', 'about', 'march', '่', 'by', 'your', 'just', '️', 'ี', 'but', 'que', 'https', 'These', 'la', 'me', 'don\'t',
'said', 'do', 'A', 'out', '’', 'im', '#SundayMorning', 'I\'M'
]

hashtags = '#WomensMarch', 'womensmarch'

# Tokenizing (pre-processing)
emoticons_str = r"""
    (?:
        [:=;] # eyes
        [oO\-]? # nose
        [D\)\]\(\]/\\OpP] #mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
	return tokens_re.findall(s)

def preprocess(s, lowercase=False):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens

# import pdb; pdb.set_trace()
tweets_data_path = 'political_tweets.json'

with open(tweets_data_path, 'r') as f:
	count_all = Counter()
	count_hash_tag = Counter()

	# creates geoJSON structure
	geo_data = {
		"type": "FeatureCollection",
		"features": []
	}
	for line in f:
		try:
			tweet = json.loads(line)

			# Uses pre-set words to check against tweet text & updates counters
			terms_all = [term for term in preprocess(tweet['text']) if term not in stop]
			terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#') and term not in hashtags]
			count_all.update(terms_all)
			count_hash_tag.update(terms_hash)

			# Converts tweets to geoJSON
			if tweet['coordinates']:
				geo_json_feature = {
					"type": "Feature",
					"geometry": tweet['coordinates'],
					"properties": {
						"text": tweet['text'],
						"created_at": tweet['created_at']
					}
				}
			if geo_json_feature['properties']['text'] not in geo_data['features']:
				geo_data['features'].append(geo_json_feature)
		except:
			continue

most_common_words = count_all.most_common(10)
most_common_hashtags = count_hash_tag.most_common(4)
print("Top ten most common words: " + str(most_common_words))
print("Top 4 related hashtags" + str(most_common_hashtags))

# Save geo data
with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))






















