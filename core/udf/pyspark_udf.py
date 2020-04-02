class TextMiningMethods():
	"""docstring for TextMiningMethods"""
	def clean_tweet(self,tweet):
		'''
		Method to clean tweets (with regex, translate, unidecode) 
		and remove stop words (with nltk)
		'''
		import re
		import string
		import unidecode
		from nltk.corpus import stopwords

		# Define some regex rules
		url_regex = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')
		numeric_regex = re.compile('(\\d+)')
		mentions_regex = re.compile("@[A-Za-z0-9]+")

		# Remove Hiperlinks
		tweet = url_regex.sub(' ', tweet)
		
		# Remove @mentions
		tweet = mentions_regex.sub(' ', tweet)
		
		# Remove punctuations
		tweet = tweet.translate(str.maketrans(string.punctuation,32*' '))	# len(string.punctuation) = 32
		
		# Remove numerics
		tweet = numeric_regex.sub(' ', tweet)
		
		# Remove white spaces
		tweet = " ".join(tweet.split())
		
		# Remove accents
		tweet = unidecode.unidecode(tweet)
		
		# Convert to lowercase
		tweet = tweet.lower()

		# Remove stop words
		list_position = 0
		tweet_cleaned = ''

		for word in tweet.split():
			if word not in set(stopwords.words("spanish")):
				if list_position == 0:
					tweet_cleaned = word
				else:
					tweet_cleaned = tweet_cleaned + ' ' + word
				list_position += 1

		return tweet_cleaned

	def clean_tweet_list(self,tweets_list):
		'''
		Method to clean tweets list with clean_tweet()
		'''
		# Iterate on each tweet account	
		for tweet_account_index,tweet_account_elem in enumerate(tweets_list):

			# Iterate on each tweet of the current account
			for tweet_data_index,tweet_data in enumerate(tweet_account_elem['tweet']):

				tweet = ''

				# Clean the current tweet
				tweet = self.clean_tweet(tweet_data['text'])

				# Update the current original tweet to the new cleaned tweet
				tweets_list[tweet_account_index]['tweet'][tweet_data_index]['text'] = tweet

		return tweets_list
