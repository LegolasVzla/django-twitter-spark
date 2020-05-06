 #!/usr/bin/env python3

class TextMiningMethods():
	"""docstring for TextMiningMethods"""
	def clean_tweet(self,tweet):
		'''
		Method to clean tweets (with regex, translate, unidecode) 
		and remove stop words (with nltk)
		'''
		import re
		import unidecode

		from nltk.corpus import stopwords

		# Define some regex rules
		url_regex = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')
		numeric_regex = re.compile('(\\d+)')
		mentions_regex = re.compile("@[A-Za-z0-9]+")
		brackets_regex = re.compile("\[[^)]*\]")
		parenthesis_regex = re.compile   ("\([^)]*\)")
		punctuation_signs = re.compile(r'[^\w\s]')

		# Remove Hiperlinks
		tweet = url_regex.sub('', tweet)
		
		# Remove @mentions
		tweet = mentions_regex.sub('', tweet)

		# Remove text between brackets and parenthesis, like [Video] or [Photos]
		tweet = brackets_regex.sub('', tweet)
		tweet = parenthesis_regex.sub('', tweet)

		# Remove punctuations
		tweet = punctuation_signs.sub('', tweet)

		# Remove punctuations
		tweet = numeric_regex.sub('', tweet)
		
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

class MachineLearningMethods():
	'''
	Class for machine learning udf
	'''
	def most_common_words(self,tweet_list):
		'''
		Get the frequency distribution of tokens obtained from tweet_list, 
		getting 100 most common words
		'''
		import nltk
		from nltk.tokenize import word_tokenize

		tokens = word_tokenize(tweet_list)
		freq = nltk.FreqDist(tokens)
		response_data = []
		for i in freq.most_common(100):
		    response_data.append(i[0])
		return response_data

	def remove_uncommon_words(self,clean_tweets,most_common_words_list):
		'''
		Remove uncommon words from clean tweets
		'''
		response_data = ''
		for index,word in enumerate(clean_tweets.split(' ')):
			if word in most_common_words_list:
				response_data+= " " + word
		return response_data

	def tweet_topic_classification(self,word_roots_by_topic_list,clean_tweet):
		'''
		- Get topic of a tweet based on Topic Model
		'''
		from rest_framework import status

		from nltk.tokenize import word_tokenize
		import Stemmer
		from collections import Counter

		try:

			# Set word roots by topics
			entertainment = word_roots_by_topic_list[0]
			religion = word_roots_by_topic_list[1]
			sports = word_roots_by_topic_list[2]
			education = word_roots_by_topic_list[3]
			technology = word_roots_by_topic_list[4]
			economy = word_roots_by_topic_list[5]
			health = word_roots_by_topic_list[6]
			politica = word_roots_by_topic_list[7]
			social = word_roots_by_topic_list[8]

			# Tokenize tweets
			#tokens = word_tokenize(kwargs['data']['text'].lower())
			tokens = word_tokenize(clean_tweet)

			# Define Stemmer for Spanish Language
			stemmer = Stemmer.Stemmer('spanish')

			# To apply stemmer to a word
			# stemmer.stemWord('word')

			# Search for coincidences between tokens from the tweet 
			# and the word roots by topics
			entertainment_coincidences = map(lambda x : x in entertainment['word_roots'],stemmer.stemWords(tokens))
			religion_coincidences = map(lambda x : x in religion['word_roots'],stemmer.stemWords(tokens))
			sports_coincidences = map(lambda x : x in sports['word_roots'],stemmer.stemWords(tokens))
			education_coincidences = map(lambda x : x in education['word_roots'],stemmer.stemWords(tokens))
			technology_coincidences = map(lambda x : x in technology['word_roots'],stemmer.stemWords(tokens))
			economy_coincidences = map(lambda x : x in economy['word_roots'],stemmer.stemWords(tokens))
			health_coincidences = map(lambda x : x in health['word_roots'],stemmer.stemWords(tokens))
			politica_coincidences = map(lambda x : x in politica['word_roots'],stemmer.stemWords(tokens))
			social_coincidences = map(lambda x : x in social['word_roots'],stemmer.stemWords(tokens))

			# Count coincidences by topic
			obj_entertainment = MachineLearningMethods()
			obj_entertainment.value = Counter(entertainment_coincidences)[True]
			obj_entertainment.topic = entertainment['topic']
			obj_religion = MachineLearningMethods()
			obj_religion.value = Counter(religion_coincidences)[True]
			obj_religion.topic = religion['topic']
			obj_sports = MachineLearningMethods()
			obj_sports.value = Counter(sports_coincidences)[True]
			obj_sports.topic = sports['topic']
			obj_education = MachineLearningMethods()
			obj_education.value = Counter(education_coincidences)[True]
			obj_education.topic = education['topic']
			obj_techcnology = MachineLearningMethods()
			obj_techcnology.value = Counter(technology_coincidences)[True]
			obj_techcnology.topic = technology['topic']
			obj_economy = MachineLearningMethods()
			obj_economy.value = Counter(economy_coincidences)[True]
			obj_economy.topic = economy['topic']
			obj_health = MachineLearningMethods()
			obj_health.value = Counter(health_coincidences)[True]
			obj_health.topic = health['topic']
			obj_politica = MachineLearningMethods()
			obj_politica.value = Counter(politica_coincidences)[True]
			obj_politica.topic = politica['topic']
			obj_social = MachineLearningMethods()
			obj_social.value = Counter(social_coincidences)[True]
			obj_social.topic = social['topic']

			# List of all topic objects
			topic_list = [
				obj_entertainment,
				obj_religion,
				obj_sports,
				obj_education,
				obj_techcnology,
				obj_economy,
				obj_health,
				obj_politica,
				obj_social
			]

			# Sort the list by value of each topic in descending order
			topic_list.sort(key=lambda x: x.value, reverse=True)

			# Finally, determine the topic resulting with the most value
			if (topic_list[0].value==0):
				response_data = "Diverso"
			elif (topic_list[0].value > topic_list[1].value):
				response_data = topic_list[0].topic
			else:
				response_data = topic_list[0].topic+' - '+topic_list[1].topic

			#self.response_data['data'].append(self.data)

		except Exception as e:
			response_data = str(e)

		return response_data

	def udf_tweet_topic_classification(self,word_roots_by_topic_list):
		from pyspark.sql.functions import udf
		from pyspark.sql.types import StringType
		return udf(lambda x: MachineLearningMethods().tweet_topic_classification(word_roots_by_topic_list,x),StringType())