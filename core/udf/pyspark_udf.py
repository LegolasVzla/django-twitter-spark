#!/usr/bin/env python3

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
		brackets_regex = re.compile("\[[^)]*\]")
		parenthesis_regex = re.compile   ("\([^)]*\)")
		consecutive_dots = re.compile(r'\.{3,}')

		# Remove Hiperlinks
		tweet = url_regex.sub(' ', tweet)
		
		# Remove @mentions
		tweet = mentions_regex.sub(' ', tweet)

		# Remove text between brackets and parenthesis, like [Video] or [Photos]
		tweet = brackets_regex.sub('', tweet)
		tweet = parenthesis_regex.sub('', tweet)

		# Remove consecutive dots
		tweet = consecutive_dots.sub('', tweet)
		
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

	def tweet_topic_classification(self, clean_tweet):
		'''
		- Get topic of a tweet based on Topic Model
		'''
		import json
		#import logging
		from rest_framework import status

		from nltk.tokenize import word_tokenize
		import Stemmer
		from collections import Counter
		import requests

		try:

			# Get twitter topics stored in Topic model
			#_word_roots_by_topic_list = WordRootViewSet()
			#_word_roots_by_topic_list.word_roots_by_topic(request)
			response = requests.get("http://localhost:8000/api/word_root/word_roots_by_topic")

			#if _word_roots_by_topic_list.code == 200:
			if response.status_code == 200:

				#topic_list = _word_roots_by_topic_list.response_data['data']
				response = response.content.decode('utf-8')
				json_response = json.loads(response)

				# Set word roots by topics
				'''
				entertainment = topic_list[0]
				religion = topic_list[1]
				sports = topic_list[2]
				education = topic_list[3]
				technology = topic_list[4]
				economy = topic_list[5]
				health = topic_list[6]
				politica = topic_list[7]
				social = topic_list[8]
				'''

				entertainment = json_response['data'][0]
				religion = json_response['data'][1]
				sports = json_response['data'][2]
				education = json_response['data'][3]
				technology = json_response['data'][4]
				economy = json_response['data'][5]
				health = json_response['data'][6]
				politica = json_response['data'][7]
				social = json_response['data'][8]

				# Tokenize tweets
				#tokens = word_tokenize(kwargs['data']['text'].lower())
				tokens = word_tokenize(clean_tweet)

				# Define Stemmer for Spanish Language
				stemmer = Stemmer.Stemmer('spanish')

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
			#logging.getLogger('error_logger').exception("[UDF - MachineLearningMethods] - Error: " + str(e))
			#self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			#self.response_data['error'].append("[UDF - MachineLearningMethods] - Error: " + str(e))
			response_data = str(e)

		return response_data
