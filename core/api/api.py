from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
from .serializers import (UserSerializer,UserDetailsAPISerializer,
	UserProfileUpdateAPISerializer,DictionarySerializer,
	DictionaryPolarityAPISerializer,CustomDictionarySerializer,
	TopicSerializer,WordCloudAPISerializer,SearchSerializer,
	RecentSearchAPISerializer,WordDetailsAPISerializer,
	WordRootSerializer,SocialNetworkAccountsSerializer,
	SocialNetworkAccountsAPISerializer,CustomDictionaryKpiAPISerializer,
	CustomDictionaryPolaritySerializer,CustomDictionaryWordAPISerializer,
	TweetTopicClassificationAPISerializer)
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions
from rest_framework import views
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import exceptions
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
#from rest_framework.views import APIView
#from rest_framework.decorators  import list_route
#from rest_framework.viewsets import GenericViewSet
#from rest_framework import serializers, validators

import json
import copy
import os
from os import path
from os.path import exists
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import imageio
#import io
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
import tzlocal

import re
import string
import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Stemmer
from collections import Counter
import pandas as pd

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import *
from pyspark.sql import SQLContext
from pyspark.sql.functions import udf
#from pyspark.sql.types import StringType, ArrayType
#from pyspark.sql import Row
from core.settings import SPARK_WORKERS,SPARK_UDF_FILE

from core.settings import BASE_DIR 
from api.social_networks_api_connections import *
import logging
from functools import wraps
from udf.pyspark_udf import (TextMiningMethods,MachineLearningMethods)

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
	page_size = 10
	#page_size_query_param = 'page'
	#max_page_size = 1000

def validate_type_of_request(f):
	'''
	Allows to validate the type of request for the endpoints
	'''
	@wraps(f)
	def decorator(*args, **kwargs):
		if(len(kwargs) > 0):
			# HTML template
			kwargs['data'] = kwargs
		# DRF raw data, HTML form input
		elif len(args[1].data) > 0:
			kwargs['data'] = args[1].data
		# Postman POST request made by params
		elif len(args[1].query_params.dict()) > 0:
			kwargs['data'] = args[1].query_params.dict()
		return f(*args,**kwargs)
	return decorator

class MachineLearningViewSet(viewsets.ViewSet):
	'''
	Class for machine learning endpoints: Topic classification of Tweet, Topic classification...
	'''
	serializer_class = TweetTopicClassificationAPISerializer

	def __init__(self):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0

	def __topic(self):
		self.value = 0
		self.topic = ""

	def __most_common_key(text):
		# Calculate the frequency distribution of tokens, getting most common word
		freq=nltk.FreqDist(tokens)
		return freq.most_common(1)[0][0]

	def __most_common_value(text):
		# Calculate the frequency distribution of tokens, getting most common word's value
		freq=nltk.FreqDist(tokens)
		return freq.most_common(1)[0][1]

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def tweet_topic_classification(self, request, *args, **kwargs):
		'''
		- POST method (tweet_topic_classification): get topic of a tweet based on Topic Model.
		- Mandatory: text
		'''
		try:
			serializer = TweetTopicClassificationAPISerializer(data=kwargs['data'])

			if serializer.is_valid():

				# Get twitter topics stored in Topic model
				_word_roots_by_topic_list = WordRootViewSet()
				response = requests.get("http://localhost:8000/api/word_root/word_roots_by_topic")

				if _word_roots_by_topic_list.code == 200:
	
					topic_list = _word_roots_by_topic_list.response_data['data']

					# Set word roots by topics
					entertainment = topic_list[0]
					religion = topic_list[1]
					sports = topic_list[2]
					education = topic_list[3]
					technology = topic_list[4]
					economy = topic_list[5]
					health = topic_list[6]
					politica = topic_list[7]
					social = topic_list[8]

					# Tokenize tweets
					tokens = word_tokenize(kwargs['data']['text'].lower())

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
					obj_entertainment = MachineLearningViewSet()
					obj_entertainment.value=Counter(entertainment_coincidences)[True]
					obj_entertainment.topic="Entretenimiento"
					obj_religion = MachineLearningViewSet()
					obj_religion.value=Counter(religion_coincidences)[True]
					obj_religion.topic="Religion"
					obj_sports = MachineLearningViewSet()
					obj_sports.value=Counter(sports_coincidences)[True]
					obj_sports.topic="Deporte"
					obj_education = MachineLearningViewSet()
					obj_education.value=Counter(education_coincidences)[True]
					obj_education.topic="Educacion"
					obj_techcnology = MachineLearningViewSet()
					obj_techcnology.value=Counter(technology_coincidences)[True]
					obj_techcnology.topic="Tecnologia"
					obj_economy = MachineLearningViewSet()
					obj_economy.value=Counter(economy_coincidences)[True]
					obj_economy.topic="Economia"
					obj_health = MachineLearningViewSet()
					obj_health.value=Counter(health_coincidences)[True]
					obj_health.topic="Salud"
					obj_politica = MachineLearningViewSet()
					obj_politica.value=Counter(politica_coincidences)[True]
					obj_politica.topic="Politica"
					obj_social = MachineLearningViewSet()
					obj_social.value=Counter(social_coincidences)[True]
					obj_social.topic="Social"

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
						self.data['topic'] = "Diverso"
					elif (topic_list[0].value > topic_list[1].value):
						self.data['topic'] = topic_list[0].topic
					else:
						self.data['topic'] = topic_list[0].topic+' - '+topic_list[1].topic

					self.response_data['data'].append(self.data)
					self.code = status.HTTP_200_OK
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - MachineLearningViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - MachineLearningViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

class BigDataViewSet(viewsets.ViewSet):
	'''
	Class for big data endpoints: Word cloud with cleaned tweets,
	sentiment analysis, topic classification of tweets (both of them)
	using apache spark
	'''
	serializer_class = SocialNetworkAccountsAPISerializer

	def __init__(self):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def process_tweets(self, request, *args, **kwargs):
		'''
		- POST method (process_tweets): get tweets from tweets_get endpoint
		for different goals: to clean all tweets with Text Mining Methods, 
		to determine Topic and to To Determinate Sentiment Analysis
		- Mandatory: social network account
		'''		
		try:

			serializer = SocialNetworkAccountsAPISerializer(data=kwargs['data'])

			if serializer.is_valid():

				# Get twitter topics stored in Topic model
				_tweets = TwitterViewSet()
				_tweets.tweets_get(request,social_network=kwargs['data']['social_network'])

				if _tweets.code == 200:

					tweets_list = _tweets.response_data['data']

					# Create SparkSession for word_cloud generation
					sc=SparkSession \
						.builder \
						.master("spark://"+SPARK_WORKERS) \
						.appName('word_cloud') \
						.config("spark.executor.memory", '2g') \
						.config('spark.executor.cores', '2') \
						.config('spark.cores.max', '2') \
						.config("spark.driver.memory",'2g') \
						.getOrCreate()
					# spark.sparkContext.getConf().getAll()

					# Or with SparkContext
					# conf = SparkConf(). \
					# 	.setAppName('word_cloud') \
					# 	.setMaster('spark://'+SPARK_WORKERS) \
					# sc = SparkContext(conf=conf)
					# SparkConf().getAll()

					sc.sparkContext.addPyFile(SPARK_UDF_FILE)

					'''
					# Generate rdd of tweets list
					tweets_rdd=spark.sparkContext.parallelize(tweets_list)

					# And then convert it to a pyspark dataframe of tweets list
					df = sqlContext.read.json(tweets_rdd)
					'''

					'''
					But tweet column in the df, needs to be split
					(Pdb) df.show()
					+---------------+---------------+--------------------+
					|_corrupt_record|   account_name|               tweet|
					+---------------+---------------+--------------------+
					|           null| CaraotaDigital|[[Wed Mar 18 05:2...|
					|           null|  ElNacionalWeb|[[Wed Mar 18 05:3...|
					|           null|    ElUniversal|[[Wed Mar 18 05:3...|
					|           null|NoticiasVenezue|                  []|
					+---------------+---------------+--------------------+
					'''

					# Tweet column is inside of [[]], so better, do the lines below

					# Define all columns name needed
					cols = [
						'account_name',
						'text',
						'favorite_count',
						'id',
						'retweet_count',
						'created_at',
						'formated_date',
						'clean_tweet',
						'topic'
					]
					rows = []

					# And iterate over all the tweet list
					for tweet_account_index, tweet_account_data in enumerate(tweets_list):

						# Extract tweets of the current tweet account into a new pandas dataframe
						tweet_data_aux_pandas_df = pd.Series(tweet_account_data['tweet']).dropna()
					
						# Iterate on each tweet of the current tweet account
						for tweet_index,tweet in enumerate(tweet_data_aux_pandas_df):

							timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
							d=datetime.fromtimestamp(timestamp)
							d.strftime('%d/%m/%Y')

							row = [
								tweet_account_data['account_name'],
								tweet['text'],
								tweet['favorite_count'],
								tweet['id'],
								tweet['retweet_count'],
								tweet['created_at'],
								d.strftime('%d %b %Y %X'),
								None,
								None
							]
							rows.append(row)
					
					# Create a Pandas Dataframe of tweets
					tweet_pandas_df = pd.DataFrame(rows, columns = cols)

					schema = StructType([
					    StructField("account_name", StringType(),True),
					    StructField("text", StringType(),True),
					    StructField("favorite_count", IntegerType(),True),
					    StructField("id", LongType(),True),
					    StructField("retweet_count", IntegerType(),True),
					    StructField("created_at", StringType(),True),
					    StructField("formated_date", StringType(),True),
					    StructField("clean_tweet", StringType(),True),
					    StructField("topic", StringType(),True)
					])

					# Create a Spark DataFrame from a pandas DataFrame
					# This data is not cleaned yet
					df = sc.createDataFrame(tweet_pandas_df,schema=schema)

					# Create a pyspark User Defined Function to clean tweets
					clean_tweet_udf = udf(TextMiningMethods().clean_tweet, StringType())

					# Applying udf functions to a new dataframe
					clean_tweet_df = df.withColumn("clean_tweet", clean_tweet_udf(df["text"]))

					# Create a pyspark udf of topic classification
					tweet_topic_classification_udf = udf(MachineLearningMethods().tweet_topic_classification, StringType())

					# Applying udf functions to a new dataframe
					topic_df = clean_tweet_df.withColumn("topic",tweet_topic_classification_udf(clean_tweet_df["clean_tweet"]))

					# Get columns and converts to a list
					tweets_processed = topic_df.select(
						'account_name',
						'text',
						'clean_tweet',
						'topic',
						'created_at',
						'formated_date',
					).toJSON().collect()

					''' To get and return only clean_tweet of clean_tweet_df
					This part was moved to frontend layer

					all_clean_tweet_ = ''

					for i in clean_tweet_list:					
						all_clean_tweet_ =  all_clean_tweet_ + i[0]

					self.response_data['data'] = ''.join(all_clean_tweet_)
					'''

					# Push and return the columns selected in json format 
					for tweet_elem in tweets_processed:					
						self.response_data['data'].append(json.loads(tweet_elem))

					sc.stop()
					self.code = status.HTTP_200_OK
					#print (self.response_data['data'])

				else:
					logging.getLogger('error_logger').exception("[API - BigDataViewSet] - Error: " + _tweets.response_data['error'][0])
					self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
					self.response_data['error'].append("[API - BigDataViewSet] - Error: " + _tweets.response_data['error'][0])

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - BigDataViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - BigDataViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class WordCloudViewSet(viewsets.ViewSet):
	'''
	Class for word cloud generation. It allows to generate a word cloud with 
	trending tweets
	'''
	serializer_class = WordCloudAPISerializer

	def __init__(self):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0

	@validate_type_of_request
	def create(self, request, *args, **kwargs):
		'''
		- POST method (create): generate a Twitter word cloud image from users 
		comments.
		- Mandatory: comments
		- Optionals: user
		If user_id is given, it will generate a random word cloud with some 
		mask located in static/images/word_cloud_masks. In other case, 
		wordcloud will be with square form
		'''
		user_id = ''
		url = ''
		authenticated = False
		colors_array = ['viridis', 'inferno', 'plasma', 'magma','Blues', 'BuGn', 'BuPu','GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd','PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu','Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd','afmhot', 'autumn', 'bone', 'cool','copper', 'gist_heat', 'gray', 'hot','pink', 'spring', 'summer', 'winter','BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr','RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral','seismic','Accent', 'Dark2', 'Paired', 'Pastel1','Pastel2', 'Set1', 'Set2', 'Set3', 'Vega20', 'Vega20b', 'Vega20c','gist_earth', 'terrain', 'ocean', 'gist_stern','brg', 'CMRmap', 'cubehelix','gnuplot', 'gnuplot2', 'gist_ncar','nipy_spectral', 'jet', 'rainbow','gist_rainbow', 'hsv', 'flag', 'prism']
		try:
			serializer = WordCloudAPISerializer(data=kwargs['data'])
			if serializer.is_valid():

				print("Generating the wordcloud image...")
				user_id = kwargs['data']['user']
				colors = random.randint(0, 74)

				# If user is authenticated
				if (user_id):
					authenticated = True
					image = random.randint(0, 9)

					# Generating the custom random word cloud
					wordcloud = WordCloud(stopwords=STOPWORDS,background_color='white',width=1600,height=1200,colormap=colors_array[colors],mask=imageio.imread(BASE_DIR + '/static/images/word_cloud_masks/cloud'+ str(image) +'.png')).generate(kwargs['data']['comments'])
				else:
					# Generating the word cloud				
					wordcloud = WordCloud(background_color='white',width=1600,height=1200).generate(kwargs['data']['comments'])
				
				plt.imshow(wordcloud, interpolation='bilinear')
				plt.axis("off")

				# Set the path folder to generate the word cloud
				if (os.path.exists(BASE_DIR + "/static/images/word_clouds")):
					os.chdir(BASE_DIR + "/static/images/word_clouds")
				else:
					os.mkdir(BASE_DIR + "/static/images/word_clouds")
					os.chdir(BASE_DIR + "/static/images/word_clouds")

				# If user is authenticated
				if user_id:
					if (os.path.exists(BASE_DIR + "/static/images/word_clouds/" + str(user_id))):
						os.chdir(BASE_DIR + "/static/images/word_clouds/" + str(user_id))
					else:
						os.mkdir(BASE_DIR + "/static/images/word_clouds/" + str(user_id))
						os.chdir(BASE_DIR + "/static/images/word_clouds/" + str(user_id))

				plt.savefig('./wordcloud.png', dpi=800,transparent = True, bbox_inches='tight', pad_inches=0)

				# Getting the url of the word cloud image generated
				if authenticated:
					url = 'images/word_clouds/' + str(user_id) + '/' + os.listdir(os.getcwd())[0]
				else:
					url = 'images/word_clouds/' + os.listdir(os.getcwd())[0]

				os.chdir(BASE_DIR)
				self.code = status.HTTP_200_OK
				self.data['url'] = url
				self.data['authenticated'] = authenticated
				self.response_data['data'].append(self.data)

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			self.data['url'] = '/images/word_cloud_masks/cloud500.png'			
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			logging.getLogger('error_logger').exception("[API - WordCloudViewSet] - Error: " + str(e))
			self.response_data['error'].append("[API - WordCloudViewSet] - Error: " + str(e))

		return Response(self.response_data,status=self.code)

	def list(self, request, *args, **kwargs):
		'''
		- GET method (list): list word clouds user folders generated
		'''		
		authenticated_word_clouds_list = []
		unauthenticated_word_cloud = ''
		aux_user_word_cloud_list = {}
		try:
			# If at least one word_cloud has been generated
			if (exists(BASE_DIR + '/static/images/word_clouds')):
				os.chdir(BASE_DIR + "/static/images/word_clouds/")

				if exists("wordcloud.png"):
					unauthenticated_word_cloud = os.listdir(os.getcwd())[0]

				# Exist at least one word_cloud custom image generated
				if(len(os.listdir(os.getcwd())) > 1):

					# Get all the custom word_cloud folders name
					for word_cloud_folder in os.listdir(os.getcwd()):
						if word_cloud_folder != "wordcloud.png":
							aux_user_word_cloud_list['user_id'] = word_cloud_folder
							authenticated_word_clouds_list.append(aux_user_word_cloud_list)
							aux_user_word_cloud_list = {}
					os.chdir(BASE_DIR)

			self.code = status.HTTP_200_OK
			self.data['authenticated_word_clouds_url_list'] = authenticated_word_clouds_list
			self.data['unathenticated_word_clouds_url'] = unauthenticated_word_cloud
			self.response_data['data'].append(self.data)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - WordCloudViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - WordCloudViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class TwitterViewSet(viewsets.ViewSet):
	'''
	Class to get a list with trending tweets
	'''
	serializer_class = SocialNetworkAccountsAPISerializer

	def __init__(self):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def tweets_get(self, request, *args, **kwargs):
		'''
		- POST method (tweets_get): get twitter data from 
		SocialNetworkAccounts Model using Tweepy
		- Mandatory: social_network
		'''
		twitter_accounts_data = {}
		try:
			serializer = SocialNetworkAccountsSerializer(
				data=kwargs['data'],
				fields=['social_network'])

			if serializer.is_valid():

				# Get twtter accounts stored in SocialNetworkAccounts model 
				_socialnetworkaccounts = SocialNetworkAccountsViewSet()
				_socialnetworkaccounts.accounts_by_social_network(
					social_network=kwargs['data']['social_network'])

				# If request is success, connect with Tweepy
				if _socialnetworkaccounts.code == 200:
					twitter_accounts_data = _socialnetworkaccounts.response_data['data'][0]['accounts_by_social_network']
					
					_socialnetworksapiconnections = SocialNetworksApiConnections(self)
					tweepy_api_client =_socialnetworksapiconnections.tweepy_connection()

					# Iterate on each twitter accounts
					for twitter_account_index, twitter_account_data in enumerate(twitter_accounts_data):

						# Make the request to get tweets of the current twitter account
						all_twitter_timeline_data = tweepy_api_client.user_timeline(
							screen_name = twitter_account_data['name'],
							count=twitter_account_data['quantity_by_request']
						)

						# Get twitter account name from the current twitter account
						self.data['account_name'] = twitter_account_data['name']
						self.data['tweet'] = []

						# Iterate on each tweet data, extracted from the current twitter account
						for tweet_data_index,tweet_data in enumerate(all_twitter_timeline_data):
							tweet_element_data = {}
							tweet_element_data['id'] = tweet_data['id']
							tweet_element_data['text'] = tweet_data['text']
							tweet_element_data['retweet_count'] = tweet_data['retweet_count']
							tweet_element_data['favorite_count'] = tweet_data['favorite_count']
							tweet_element_data['created_at'] = tweet_data['created_at']
							self.data['tweet'].append(copy.deepcopy(tweet_element_data))
						self.response_data['data'].append(copy.deepcopy(self.data))

					self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - TwitterViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - TwitterViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class UserViewSet(viewsets.ModelViewSet):
	'''
	Class related with the User Model.
	'''
	queryset = User.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0		

	def get_serializer_class(self):
		if self.action in ['user_details']:
			return UserDetailsAPISerializer
		if self.action in ['profile_update']:
			return UserProfileUpdateAPISerializer
		return UserSerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def user_details(self, request, *args, **kwargs):
		'''
		- POST method (user_details): get specific fields of the user
		(id,first_name,last_name,email)
		- Mandatory: user
		'''
		try:
			serializer = UserDetailsAPISerializer(data=kwargs['data'])
			if serializer.is_valid():

				queryset = get_object_or_404(
					User.objects.filter(
						id=kwargs['data']['user'],
						is_active=True,
						is_deleted=False
					).values('id','first_name','last_name','email'))
				self.data = queryset
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - UserView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - UserView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['put'], detail=False)	
	def profile_update(self, request, *args, **kwargs):
		'''
		- PUT method (profile_update): updated user from email input
		comments.
		- Mandatory: email
		- Optionals: first_name, last_name
		'''
		try:
			serializer = UserProfileUpdateAPISerializer(data=kwargs['data'])
			if serializer.is_valid():

				# Get the instance of the user requested to edit
				instance = User.objects.get(email=kwargs['data']['email'])

				if not kwargs['data']['first_name'] and not kwargs['data']['last_name']:
					serializer = UserSerializer(instance,
						data=kwargs['data'],
						partial=True,
						fields=('email','first_name','last_name'),
						required_fields=['email'],
						excluded_fields=['first_name','last_name']
					)

				elif not kwargs['data']['first_name']:
					serializer = UserSerializer(instance,
						data=kwargs['data'],
						partial=True,
						fields=('email','first_name','last_name'),
						required_fields=['email'],
						excluded_fields=['first_name'])

				elif not kwargs['data']['last_name']:
					serializer = UserSerializer(instance,
						data=kwargs['data'],
						partial=True,
						fields=('email','first_name','last_name'),
						required_fields=['email'],
						excluded_fields=['last_name'])
				else:
					serializer = UserSerializer(instance,
						data=kwargs['data'],
						partial=True,
						fields=('email','first_name','last_name'),
						required_fields=['email'])

				if serializer.is_valid():
					serializer.save()
					self.data['id'] = instance.id
					self.data['first_name'] = instance.first_name
					self.data['last_name'] = instance.last_name
					self.response_data['data'].append(self.data)
					self.code = status.HTTP_200_OK
				else:
					self.response_data['error'].append("[API - UserView] - Error: " + serializer.errors)
					self.code = status.HTTP_400_BAD_REQUEST

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - UserView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - UserView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class DictionaryViewSet(viewsets.ModelViewSet):
	'''
	Class related with the Dictionary Model, that is a set of word that 
	contains positive and negative words.
	'''
	queryset = Dictionary.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0		

	def get_serializer_class(self):
		if self.action in ['dictionary_by_polarity']:
			return DictionaryPolarityAPISerializer
		return DictionarySerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def dictionary_by_polarity(self, *args, **kwargs):
		'''
		- POST method (post): get dictionary by polarity filtering (positive 
		or negative words list)
		- Mandatory: polarity, language_id
		'''
		try:
			serializer = DictionarySerializer(
				data=kwargs['data'],
				fields=['polarity','language'])

			if serializer.is_valid():

				queryset = Dictionary.objects.filter(
					is_active=True,
					is_deleted=False,
					polarity=kwargs['data']['polarity'],
					language_id=kwargs['data']['language']
				).order_by('id')
				page = self.paginate_queryset(queryset)

				if page is not None:

					serializer = DictionarySerializer(page,many=True,required_fields=['polarity'],fields=('id','word','polarity'))
					self.data['words']=json.loads(json.dumps(serializer.data))
					self.response_data['data'].append(self.data)
					self.code = status.HTTP_200_OK
					return self.get_paginated_response(serializer.data)

				serializer = DictionarySerializer(queryset,many=True,required_fields=['polarity'],fields=('id','word','polarity'))
				self.data['words']=json.loads(json.dumps(serializer.data))
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK              
				return Response(serializer.data)

			else:

				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - DictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - DictionaryViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

class CustomDictionaryViewSet(viewsets.ModelViewSet):
	'''
	Class related with the CustomDictionary Model, that is a customizable 
	set of words per user, with positive and negative words
	'''	
	queryset = CustomDictionary.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0		

	def get_serializer_class(self):
		if self.action in ['custom_dictionary_kpi','user_custom_dictionary']:
			return CustomDictionaryKpiAPISerializer
		if self.action in ['custom_dictionary_polarity_get']:
			return CustomDictionaryWordAPISerializer
		return CustomDictionarySerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def custom_dictionary_kpi(self, *args, **kwargs):
		'''
		- POST method (custom_dictionary_kpi): get user custom dictionary
		kpi's (total of words, total positive words, total negative words)
		from email input
		- Mandatory: user, language
		'''
		try:
			serializer = CustomDictionarySerializer(
				data=kwargs['data'],
				fields=('language','user'),
				required_fields=['language','user'])

			if serializer.is_valid():

				self.data['total_words'] = CustomDictionary.objects.filter(
					is_active=True,
					is_deleted=False,
					language_id=kwargs['data']['language'],
					user_id=kwargs['data']['user']
				).count()			
				self.data['total_positive_words'] = CustomDictionary.objects.filter(
					is_active=True,
					is_deleted=False,
					language_id=kwargs['data']['language'],
					user_id=kwargs['data']['user'],
					polarity='P'
				).count()
				self.data['total_negative_words'] = CustomDictionary.objects.filter(
					is_active=True,
					is_deleted=False,
					language_id=kwargs['data']['language'],
					user_id=kwargs['data']['user'],
					polarity='N'
				).count()
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def user_custom_dictionary(self, *args, **kwargs):
		'''
		- POST method (user_custom_dictionary): get user custom dictionary
		- Mandatory: user, language
		'''
		try:

			serializer = CustomDictionarySerializer(
				data=kwargs['data'],
				fields=('language','user'),
				required_fields=['language','user'])

			if serializer.is_valid():

				self.data['custom_dictionary'] = CustomDictionary.objects.filter(
					is_active=True,
					is_deleted=False,
					language_id=kwargs['data']['language'],
					user_id=kwargs['data']['user']
				).order_by('id').values(
					'id','word','polarity','created_date','updated_date')
				#content = JSONRenderer().render(serializer.data)
				#stream = io.BytesIO(content)
				#self.response_data['data']['custom_dictionary'] = JSONParser().parse(stream)
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def custom_dictionary_polarity_get(self, *args, **kwargs):
		'''
		- POST method (user_custom_dictionary): get the polarity of a word
		- Mandatory: user, word
		'''
		try:

			# The request comes from the web app
			queryset = CustomDictionary.objects.filter(
				id=kwargs['data']['word'],
				is_active=True,
				is_deleted=False
			).values('id','polarity','word')
			self.data = queryset[0]
			self.response_data['data'].append(self.data)
			self.code = status.HTTP_200_OK

		except Exception as e:

			try:

				# The request comes from DRF API View, Swagger, Postman...
				serializer = CustomDictionarySerializer(
					data=kwargs['data'],
					fields=('word','user'),
					required_fields=['word','user'])

				if serializer.is_valid():

					# Get the instance of the requested word to edit
					queryset = get_object_or_404(
						CustomDictionary.objects.filter(
							word=kwargs['data']['word'],
							user_id=kwargs['data']['user'],
							is_active=True,
							is_deleted=False
						).values('id','polarity','word'),
						word=kwargs['data']['word'])
					self.data['custom_dictionary']=queryset
					self.response_data['data'].append(self.data)
					self.code = status.HTTP_200_OK

				else:
					return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

			except Exception as e:
				logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
				self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
				self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	def create(self, request, *args, **kwargs):
		'''
		- POST method (create): create a new word for a custom dictionary
		- Mandatory: word, polarity, is_active, is_deleted, user, language
		'''
		try:
			serializer = CustomDictionarySerializer(data=kwargs['data'])
			if serializer.is_valid():

				serializer.save()
				self.data['word'] = kwargs['data']['word']
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	def update(self, request, *args, **kwargs):
		'''
		- PUT method (update): update the polarity of a word
		- Mandatory: word_id, polarity
		'''
		try:
			data = None
			custom_dictionary_id = None

			# The request comes from DRF API View          
			if kwargs.keys().__contains__('pk'):
				data = request.data
				custom_dictionary_id = kwargs['pk']
			else:
				# The request comes from Web App, Swagger, Postman
				data = kwargs['data']
				custom_dictionary_id = kwargs['data']['id']

			serializer = CustomDictionarySerializer(data=data,
				fields=('id','polarity'),
				required_fields=['id','polarity'])

			if serializer.is_valid():

				# Get the instance of the requested word to edit
				instance = CustomDictionary.objects.get(id=custom_dictionary_id)
				serializer = CustomDictionaryPolaritySerializer(instance,
					data=data,partial=True)

				if serializer.is_valid():
					serializer.save()
					self.data['id'] = instance.id
					self.data['word'] = instance.word
					self.response_data['data'].append(self.data)
					self.code = status.HTTP_200_OK
				else:
					return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	def destroy(self, request, *args, **kwargs):
		'''
		- DELETE method (destroy): delete a word of an user custom dictionary
		- Mandatory: word_id
		'''
		try:
			# Get the instance of the requested word to destroy
			instance = CustomDictionary.objects.get(id=kwargs['data']['word'])
			instance.is_active = False
			instance.is_deleted = True
			instance.save()

			self.data['id'] = instance.id
			self.data['word'] = instance.word
			self.response_data['data'].append(self.data)
			self.code = status.HTTP_200_OK

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class TopicViewSet(viewsets.ModelViewSet):
	'''
	Class related with the Topic Model, what is about people are talking 
	in a specific moment in a social network.
	'''
	queryset = Topic.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = TopicSerializer
	pagination_class = StandardResultsSetPagination

class SearchViewSet(viewsets.ModelViewSet):
	'''
	Class related with the Search Model, that is a tracking model where you
	could find recently search by user.
	'''	
	queryset = Search.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': []}
		self.data = {}		
		self.code = 0		

	def get_serializer_class(self):
		if self.action in ['recent_search_kpi','recent_search']:
			return RecentSearchAPISerializer
		if self.action in ['twitter_timeline_polarity',
			'twitter_timeline_likes','twitter_timeline_shared']:
			return WordDetailsAPISerializer
		return SearchSerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def recent_search_kpi(self, request, *args, **kwargs):
		'''
		- POST method (recent_search_kpi): get user custom recent search 
		kpi's (total of positive and negative search by group, top positive 
		search, top negative search
		- Mandatory: user, social_network_id
		'''
		try:
			serializer = SearchSerializer(
				data=kwargs['data'],
				fields=['social_network','user'])

			if serializer.is_valid():
			
				# 1. Get the total of search of the current user
				total_search = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user']
				).count()

				# Then, calculate the % of the positive and negative search done 
				# by the current user
				self.data['weighted_group'] = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user']
				).values('polarity').annotate(
					weighted_group=Count('polarity')*100/total_search)

				# 2. Get the total of the positive search
				total_positive_search = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user'],
					polarity='P'
				).count()

				# Then, get the top five positive most wanted words of the 
				# current user 
				self.data['top_positive_search'] = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user'],
					polarity='P'
				).values('word').order_by('-count').annotate(count=Count('word')*100/total_positive_search)[:5]

				# 3. Get the total of the negative search
				total_negative_search = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user'],
					polarity='N'
				).count()

				# Then, get the top negative positive most wanted words of the 
				# current user
				self.data['top_negative_search'] = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user'],
					polarity='N'
				).values('word').order_by('-count').annotate(count=Count('word')*100/total_negative_search)[:5]
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def recent_search(self, request, *args, **kwargs):
		'''
		- POST method (recent_search): get user recent search
		- Mandatory: user, social_network_id
		'''
		try:
			serializer = SearchSerializer(
				data=kwargs['data'],
				fields=['social_network','user'])

			if serializer.is_valid():

				queryset = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user']).order_by('id').reverse()
				'''
				page = self.paginate_queryset(queryset)

				if page is not None:

				# Get the recently search of the current user
				serializer = SearchSerializer(page, many=True, fields=(
					'id','word','polarity','liked','shared','searched_date'))
				self.data['recently_search'] = json.loads(json.dumps(serializer.data))
				self.code = status.HTTP_200_OK
				self.response_data['data'].append(self.data)
				return self.get_paginated_response(serializer.data)
				'''

				# Get the recently search of the current user
				serializer = SearchSerializer(queryset, many=True, fields=(
					'id','word','polarity','liked','shared','searched_date'))
				self.data['recently_search'] = json.loads(json.dumps(serializer.data))
				self.code = status.HTTP_200_OK
				self.response_data['data'].append(self.data)

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def twitter_timeline_polarity(self, request, *args, **kwargs):
		'''
		- POST method (word_details): get an user timeline of a word 
		searched (twitter_timeline_shared,twitter_timeline_likes,
		twitter_timeline_polarity)
		- Mandatory: social_network_id, word, user_id
		'''
		try:
			serializer = SearchSerializer(
				data=kwargs['data'],
				fields=['social_network','user','word'])

			if serializer.is_valid():

				#self.data['word'] = kwargs['data']['word']

				# Get the information related with the timeline of the word 
				# on Twitter in function of polarity
				queryset = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user'],
					word=kwargs['data']['word']
				).values('sentiment_analysis_percentage','searched_date').order_by('id')

				serializer = SearchSerializer(queryset,many=True,
					fields=('sentiment_analysis_percentage','searched_date'))
				self.data['twitter_timeline_polarity'] = json.loads(json.dumps(serializer.data))
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def twitter_timeline_likes(self, request, *args, **kwargs):
		'''
		- POST method (word_details): get an user timeline of a word 
		searched (twitter_timeline_shared,twitter_timeline_likes,
		twitter_timeline_polarity)
		- Mandatory: social_network_id, word, user_id
		'''
		try:
			serializer = SearchSerializer(
				data=kwargs['data'],
				fields=['social_network','user','word'])

			if serializer.is_valid():

				#self.data['word'] = kwargs['data']['word']

				# Get the information related with the timeline of the word
				# on Twitter in function of likes
				queryset = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user'],
					word=kwargs['data']['word']
				).values('liked','searched_date').order_by('id')

				serializer = SearchSerializer(queryset, many=True, fields=('liked','searched_date'))
				self.data['twitter_timeline_likes'] = json.loads(json.dumps(serializer.data))
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def twitter_timeline_shared(self, request, *args, **kwargs):
		'''
		- POST method (word_details): get an user timeline of a word 
		searched (twitter_timeline_shared,twitter_timeline_likes,
		twitter_timeline_polarity)
		- Mandatory: social_network_id, word, user_id
		'''
		try:
			serializer = SearchSerializer(
				data=kwargs['data'],
				fields=['social_network','user','word'])

			if serializer.is_valid():

				#self.data['word'] = kwargs['data']['word']

				# Get the information related with the timeline of the word
				# on Twitter in function of retweets
				queryset = Search.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network=kwargs['data']['social_network'],
					user_id=kwargs['data']['user'],
					word=kwargs['data']['word']
				).values('shared','searched_date').order_by('id')

				serializer = SearchSerializer(queryset, many=True, fields=('shared','searched_date'))
				self.data['twitter_timeline_shared'] = json.loads(json.dumps(serializer.data))
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class WordRootViewSet(viewsets.ModelViewSet):
	'''
	Class related with the WordRoot Model, that is a word or word part that
	can form the basis of new words through the addition of prefixes and 
	suffixes.
	'''
	queryset = WordRoot.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = WordRootSerializer
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0

	@validate_type_of_request
	@action(methods=['get'], detail=False)
	def word_roots_by_topic(self, request, *args, **kwargs):
		'''
		- POST method (word_roots_by_topic): get word roots group by topics
		- Mandatory: None
		'''
		try:
			topics_list = Topic.objects.filter(
				is_active=True,
				is_deleted=False).values('id','name')

			# Iterate on each topic
			for topic in topics_list:	

				self.data['topic'] = topic['name']
				word_roots_by_topic = WordRoot.objects.filter(
					is_active=True,
					is_deleted=False,
					topic_id=topic['id']).values('word_root')
				self.data['quantity'] = word_roots_by_topic.count()
				self.data['word_roots'] = []

				# Iterate on each word root group of the current topic
				for word_root_index,word_root in enumerate(word_roots_by_topic):
					self.data['word_roots'].append(word_root['word_root'])
				self.response_data['data'].append(copy.deepcopy(self.data))

			self.code = status.HTTP_200_OK

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - WordRootViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - WordRootViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

class SocialNetworkAccountsViewSet(viewsets.ModelViewSet):
	'''
	Class related with the SocialNetworksAccounts Model, that is a set of
	social networks accounts used to sentiment analysis
	'''	
	queryset = SocialNetworkAccounts.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = 0		

	def get_serializer_class(self):
		if self.action in ['accounts_by_social_network']:
			return SocialNetworkAccountsAPISerializer
		return SocialNetworkAccountsSerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def accounts_by_social_network(self, *args, **kwargs):
		'''
		- POST method (post): get the social networks accounts list of an
		specific social network
		- Mandatory: social network account
		'''
		try:
			serializer = SocialNetworkAccountsSerializer(
				data=kwargs['data'],
				fields=['social_network'])

			if serializer.is_valid():

				queryset = SocialNetworkAccounts.objects.filter(
					is_active=True,
					is_deleted=False,
					social_network_id=kwargs['data']['social_network']).order_by('id')
				serializer = SocialNetworkAccountsSerializer(queryset,many=True,
					required_fields=['social_network'],
					fields=('id','name','social_network','quantity_by_request'))
				self.data['accounts_by_social_network']=json.loads(json.dumps(serializer.data))
				self.response_data['data'].append(self.data)
				self.code = status.HTTP_200_OK

			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - SocialNetworkAccountsViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - SocialNetworkAccountsViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)
