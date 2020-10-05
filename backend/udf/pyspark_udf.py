 #!/usr/bin/env python3
'''Run the following command from django-twitter-core/core path, 
if this file needs to be updated:
zip -r udf.zip udf'''

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

class VoteClassifier():
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        from statistics import mode

        votes = []
        for current_classifier in self._classifiers:
            v = current_classifier.classify(dict([token, True] for token in features))
            votes.append(v)
            return mode(votes)

    def confidence(self, features):
        from statistics import mode

        votes = []
        for current_classifier in self._classifiers:
            v = current_classifier.classify(dict([token, True] for token in features))
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

    def get_tweets_for_model(self, features):
        yield dict([token, True] for token in features)

    def voted_classifier_prob_classify(self, features):
        from statistics import mode

        positive_dist = 0
        negative_dist = 0
        for current_classifier in self._classifiers:
        	dist = current_classifier.prob_classify(list(VoteClassifier().get_tweets_for_model(features))[0])
        	positive_dist+= dist.prob('Positive')
        	negative_dist+= dist.prob('Negative')
        positive_prob_classify = positive_dist/len(self._classifiers)
        negative_prob_classify = negative_dist/len(self._classifiers)
        return positive_prob_classify,negative_prob_classify

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

	def twitter_sentiment_analysis(self,custom_user_dictionary_dict,clean_tweet):
		'''
		- Determinate sentiment analysis (polarity) of tweet
		Note: this simple model, isn't trained to handle sarcasm or ironic 
		sentences yet, i.e:

		"Hoy es un maravilloso e impresionante día de mierda"

		This is a typically ironic tweet but this model will categorize it 
		as "Positive" by majority of positive words. However, some words that
		aren't in positive_dictionary.json or negative_dictionary.json
		could be added by the user and selected as "Positive" or "Negative",
		so in consequence, a sarcasm tweet could be categorized correctly,
		but only by mayority of positive and negative words.
		'''
		import json
		from nltk.tokenize import word_tokenize

		import Stemmer
		from collections import Counter

		try:
			response_data = {}
			tokens = word_tokenize(clean_tweet)

			# Define Stemmer for Spanish Language
			stemmer = Stemmer.Stemmer('spanish')

			# Compare received tweet with the positive and negative 
			# custom user dictionary
			positive = map(lambda x : x in custom_user_dictionary_dict['positive'], stemmer.stemWords(tokens))
			negative = map(lambda x : x in custom_user_dictionary_dict['negative'], stemmer.stemWords(tokens))
			pos = Counter(positive)[True]
			neg = Counter(negative)[True]
			total = pos + neg

			if total > 0:
				if pos == neg:
					response_data["polarity"] = "NU" # Neutral
				else:
					if pos > neg:
						response_data["polarity"] = "P"
						# response_data["sentiment"] = (pos*100)/total
					else:
						response_data["polarity"] = "N"
						# response_data["sentiment"] = (neg*100)/total

				response_data["positive_sentiment_score"] = pos/len(tokens)
				response_data["negative_sentiment_score"] = neg/len(tokens)
				response_data["neutral_sentiment_score"] = (len(tokens)-(pos+neg))/len(tokens)

			else:
				# None token match with any positive or negative word, 
				# so it's weak to determine a sentiment score
				response_data["polarity"] = "NU"
				# Note: sentiment score could be 1, if all the words
				# are neutral, it means that it's necessary also a
				# neutral dictionary
				response_data["positive_sentiment_score"] = 0
				response_data["negative_sentiment_score"] = 0
				response_data["neutral_sentiment_score"] = 1

			# We still don't have a way to determine confidence level
			# with a sentiment analysis model from a dictionary with 
			# positive and negative words
			response_data["confidence"] = "Undefined"

		except Exception as e:
			response_data = { 
				"polarity": None,
				"positive_sentiment_score": None,
				"negative_sentiment_score": None,
				"neutral_sentiment_score": None,
				"confidence": "Undefined"
			}

		return json.dumps(response_data)

	def udf_twitter_sentiment_analysis(self,custom_user_dictionary_dict):
		from pyspark.sql.functions import udf
		from pyspark.sql.types import StringType
		return udf(lambda x: MachineLearningMethods().twitter_sentiment_analysis(custom_user_dictionary_dict,x),StringType())

	def twitter_sentiment_analysis_voted_classifier(self,tweet):
		import json
		import pickle
		import os

		from nltk.tokenize import word_tokenize

		try:
			response_data = {}

			# Import project path: "<your_full_path>/django-twitter-spark/core/udf"
			project_path = os.path.join(os.path.dirname(__file__)) 

			# Load the bayesian classifier sentiment model
			f = open(project_path+'/../sentiment_classifiers/original_naives_bayes_classifier.pickle', 'rb')
			#return os.getcwd() + " " + project_path+'/../sentiment_classifiers/'
			original_bayesian_classifier = pickle.load(f)
			f.close()

			# Load the SVC_classifier sentiment model
			# f = open(project_path+'/../sentiment_classifiers/SVC_sentiment_classifier.pickle', 'rb')
			# SVC_classifier = pickle.load(f)
			# f.close()

			# Load the LinearSVC_classifier sentiment model
			# f = open(project_path+'/../sentiment_classifiers/LinearSVC_sentiment_classifier.pickle', 'rb')
			# LinearSVC_classifier = pickle.load(f)
			# f.close()

			# Load the NuSVC_classifier sentiment model
			f = open(project_path+'/../sentiment_classifiers/NuSVC_sentiment_classifier.pickle', 'rb')
			NuSVC_classifier = pickle.load(f)
			f.close()

			# Load the SGDClassifier_classifier sentiment model
			# f = open(project_path+'/../sentiment_classifiers/SGDClassifier_sentiment_classifier.pickle', 'rb')
			# SGDClassifier_classifier = pickle.load(f)
			# f.close()

			# Load the MNB_classifier sentiment model
			f = open(project_path+'/../sentiment_classifiers/MNB_sentiment_classifier.pickle', 'rb')
			MNB_classifier = pickle.load(f)
			f.close()

			# Load the BernoulliNB_classifier sentiment model
			f = open(project_path+'/../sentiment_classifiers/BernoulliNB_sentiment_classifier.pickle', 'rb')
			BernoulliNB_classifier = pickle.load(f)
			f.close()

			# Load the LogisticRegression_classifier sentiment model
			f = open(project_path+'/../sentiment_classifiers/LogisticRegression_sentiment_classifier.pickle', 'rb')
			LogisticRegression_classifier = pickle.load(f)
			f.close()

			voted_classifier = VoteClassifier(original_bayesian_classifier,
			                                  #SVC_classifier,
			                                  #LinearSVC_classifier,
			                                  NuSVC_classifier,
			                                  #SGDClassifier_classifier,
			                                  MNB_classifier,
			                                  BernoulliNB_classifier,
			                                  LogisticRegression_classifier)

			tweet_tokenized = word_tokenize(TextMiningMethods().clean_tweet(tweet))

			# Get sentiment analysis of the tweet
			polarity = voted_classifier.classify(tweet_tokenized)

			if polarity == 'Positive':
				response_data["polarity"] = "P"
			elif polarity == 'Negative':
				response_data["polarity"] = "N"
			# elif polarity == 'Neutral':
			# 	response_data["polarity"] = "NU"

			# Get confidence level of the analysis
			response_data["confidence"] = voted_classifier.confidence(tweet_tokenized)

			# dist = classifier.prob_classify(features)
			# for label in dist.samples():
			#     print("%s: %f" % (label, dist.prob(label)))

			# response_data["positive_sentiment_score"] = dist.prob('Positive')
			# response_data["neutral_sentiment_score"] = float("{:f}".format(1-(dist.prob('Positive')+dist.prob('Negative'))))

			response_data["positive_sentiment_score"],response_data["negative_sentiment_score"] = voted_classifier.voted_classifier_prob_classify(tweet_tokenized)

		except Exception as e:
			response_data = { 
				"polarity": None,
				"positive_sentiment_score": None,
				"negative_sentiment_score": None,
				"neutral_sentiment_score": None,
				"confidence": "Undefined"
			}

		return json.dumps(response_data)
