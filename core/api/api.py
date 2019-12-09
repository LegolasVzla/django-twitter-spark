from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
from .serializers import (UserSerializer,UserDetailsSerializer,
	UserProfileUpdateSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,
	SearchSerializer,SentimentAnalysisSerializer,LikesSerializer,
	SharedSerializer,RecentSearchSerializer,WordRootSerializer,
	SocialNetworkAccountsSerializer,CustomDictionaryKpiSerializer,
	CustomDictionaryPolaritySerializer)
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
import os
from os import path
from os.path import exists
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import imageio
#import io

from core.settings import BASE_DIR 
import logging
from functools import wraps

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
	page_size = 10
	#page_size_query_param = 'page_size'
	#max_page_size = 1000

def validate_type_of_request(f):
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

class WordCloudViewSet(viewsets.ViewSet):
	'''
	Endpoint to list and generate Twitter word cloud images
	- POST method (create): generate a Twitter word cloud image from users 
	comments.
	Input must be as below:
	{
		"data": {
			"comments": ["twitter comments list"],
			"user": 1
		}
	}
	- Mandatory: comments
	- Optionals: user
	If user_id is given, it will generate a random word cloud with some 
	mask located in static/images/word_cloud_masks. In other case, wordcloud
	will be with square form		
	'''
	def __init__(self):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0
		self.error_message = ''

	@validate_type_of_request
	def create(self, request, *args, **kwargs):
		user_id = ''
		url = ''
		authenticated = False
		colors_array = ['viridis', 'inferno', 'plasma', 'magma','Blues', 'BuGn', 'BuPu','GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd','PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu','Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd','afmhot', 'autumn', 'bone', 'cool','copper', 'gist_heat', 'gray', 'hot','pink', 'spring', 'summer', 'winter','BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr','RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral','seismic','Accent', 'Dark2', 'Paired', 'Pastel1','Pastel2', 'Set1', 'Set2', 'Set3', 'Vega20', 'Vega20b', 'Vega20c','gist_earth', 'terrain', 'ocean', 'gist_stern','brg', 'CMRmap', 'cubehelix','gnuplot', 'gnuplot2', 'gist_ncar','nipy_spectral', 'jet', 'rainbow','gist_rainbow', 'hsv', 'flag', 'prism']
		try:
			user_id = kwargs['data']['data']['user']
			comments_list = kwargs['data']['data']['comments']
			text = ' '.join(comments_list)
			colors = random.randint(0, 74)
			
			print("Generating the wordcloud image...")

			# If user is authenticated
			if (kwargs['data']['data']['user']):
				authenticated = True
				user_id = kwargs['data']['data']['user']
				image = random.randint(0, 9)

				# Generating the custom random word cloud
				wordcloud = WordCloud(stopwords=STOPWORDS,background_color='white',width=1600,height=1200,colormap=colors_array[colors],mask=imageio.imread('./static/images/word_cloud_masks/cloud'+ str(image) +'.png')).generate(text)
			else:
				# Generating the word cloud				
				wordcloud = WordCloud(background_color='white',width=1600,height=1200).generate(text)
			
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
			self.response_data['data']['url'] = url
			self.response_data['data']['authenticated'] = authenticated

		except Exception as e:
			if not kwargs['data']['data']['comments']:
				self.error_message = 'Comments can"t be empty. '
			else:
				self.error_message = 'word_cloud_data format must be like: {"data": {"comments": ["twitter comments list"],"user": '' }} where user can be empty. '
			self.response_data['error'].append("[API - WordCloudViewSet] - Error: " + self.error_message + str(e))
			logging.getLogger('error_logger').exception("[API - WordCloudViewSet] - Error: " + self.error_message + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR

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
			self.response_data['data']['authenticated_word_clouds_url_list'] = authenticated_word_clouds_list
			self.response_data['data']['unathenticated_word_clouds_url'] = unauthenticated_word_cloud

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - WordCloudViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return Response(self.response_data,status=self.code)

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = UserSerializer
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get_serializer_class(self):
		if self.action in ['user_details']:
			return UserDetailsSerializer
		if self.action in ['profile_update']:
			return UserProfileUpdateSerializer
		return UserSerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def user_details(self, request, *args, **kwargs):
		try:
			queryset = get_object_or_404(
				User.objects.filter(
					id=kwargs['data']['user'],
					is_active=True,
					is_deleted=False
				).values('id','first_name','last_name','email'))
			self.response_data['data'] = queryset
			self.code = status.HTTP_200_OK
		except Exception as e:
			logging.getLogger('error_logger').exception("[API - UserView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - UserView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['put'], detail=False)	
	def profile_update(self, request, *args, **kwargs):
		try:
			# Get the instance of the user requested to edit
			instance = User.objects.get(email=kwargs['data']['email'])

			if not kwargs['data']['first_name']:
				serializer = UserSerializer(instance, data=kwargs['data'], partial=True, fields=('email','first_name','last_name'), required_fields=['email'],excluded_fields=['first_name'])
			elif not kwargs['data']['last_name']:
				serializer = UserSerializer(instance, data=kwargs['data'], partial=True, fields=('email','first_name','last_name'), required_fields=['email'],excluded_fields=['last_name'])
			else:
				serializer = UserSerializer(instance, data=kwargs['data'], partial=True, fields=('email','first_name','last_name'), required_fields=['email'])

			if serializer.is_valid():
				serializer.save()
				self.response_data['data']['id'] = instance.id
				self.response_data['data']['first_name'] = instance.first_name
				self.response_data['data']['last_name'] = instance.last_name
				self.code = status.HTTP_200_OK
			else:
				self.response_data['error'].append("[API - UserView] - Error: " + serializer.errors)
				self.code = status.HTTP_400_BAD_REQUEST
		except Exception as e:
			logging.getLogger('error_logger').exception("[API - UserView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - UserView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class DictionaryViewSet(viewsets.ModelViewSet):
	queryset = Dictionary.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DictionarySerializer
	pagination_class = StandardResultsSetPagination

class CustomDictionaryViewSet(viewsets.ModelViewSet):
	queryset = CustomDictionary.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CustomDictionarySerializer
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get_serializer_class(self):
		if self.action == 'custom_dictionary_kpi':
			return CustomDictionaryKpiSerializer
		return CustomDictionarySerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def custom_dictionary_kpi(self, *args, **kwargs):
		try:
			queryset = CustomDictionary.objects.filter(
				is_active=True,
				is_deleted=False,
				language_id=kwargs['data']['language'],
				user_id=kwargs['data']['user']
			).order_by('id')
			#language_id=request.data['language'],
			serializer = CustomDictionarySerializer(queryset, many=True)
			#content = JSONRenderer().render(serializer.data)
			#stream = io.BytesIO(content)
			#self.response_data['data']['custom_dictionary'] = JSONParser().parse(stream)
			self.response_data['data']['custom_dictionary']=json.loads(json.dumps(serializer.data))
			self.response_data['data']['total_words'] = CustomDictionary.objects.filter(
				is_active=True,
				is_deleted=False,
				language_id=kwargs['data']['language'],
				user_id=kwargs['data']['user']
			).count()
			self.response_data['data']['total_positive_words'] = CustomDictionary.objects.filter(
				is_active=True,
				is_deleted=False,
				language_id=kwargs['data']['language'],
				user_id=kwargs['data']['user'],
				polarity='P'
			).count()
			self.response_data['data']['total_negative_words'] = CustomDictionary.objects.filter(
				is_active=True,
				is_deleted=False,
				language_id=kwargs['data']['language'],
				user_id=kwargs['data']['user'],
				polarity='N'
			).count()					
			self.code = status.HTTP_200_OK
		except Exception as e:
			'''This kind of format data validation, will be improvement
			coming soon
			if not self.response_data['data']['user']:
				self.response_data['data']['error'].append('User can"t be empty')
			elif not self.response_data['data']['language']:
				self.response_data['data']['error'].append('Language can"t be empty')
			else:
				self.response_data['data']['error'].append('Data format must be like: {"data": {"user": <user_id>, "language": <language_id> }}')
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + self.response_data['error'] + str(e))
			'''
			logging.getLogger('error_logger').exception("[CustomDictionaryViewSet] - Error: " + str(e))			
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def custom_dictionary_polarity_get(self, *args, **kwargs):
		try:
			# The request comes from the web app
			queryset = CustomDictionary.objects.filter(
				id=kwargs['data']['word'],
				is_active=True,
				is_deleted=False
			).values('id','polarity','word')
			self.response_data['data'] = queryset[0]
			self.code = status.HTTP_200_OK
		except Exception as e:
			try:
				# The request comes from DRF Api View
				if kwargs['data'].dict():
					# Get the instance of the requested word to edit
					queryset = get_object_or_404(
						CustomDictionary.objects.filter(
							word=kwargs['data']['word'],
							is_active=True,
							is_deleted=False
						).values('id','polarity','word'),
						word=kwargs['data']['word'])
					self.response_data['data']['custom_dictionary']=queryset
					self.code = status.HTTP_200_OK
			except Exception as e:
				logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
				self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
				self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))			
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	def create(self, request, *args, **kwargs):
		try:
			serializer = CustomDictionarySerializer(data=kwargs)

			if serializer.is_valid():
				serializer.save()
				self.response_data['data']['word'] = kwargs['word']
				self.code = status.HTTP_200_OK
			else:
				self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + serializer.errors)
				self.code = status.HTTP_400_BAD_REQUEST
		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	def update(self, request, *args, **kwargs):
		try:
			# Get the instance of the requested word to edit
			instance = CustomDictionary.objects.get(id=kwargs['data']['word'])

			serializer = CustomDictionaryPolaritySerializer(instance, 
				data=kwargs['data'], partial=True)

			if serializer.is_valid():
				serializer.save()
				self.response_data['data']['id'] = instance.id
				self.response_data['data']['word'] = instance.word
				self.code = status.HTTP_200_OK
			else:
				self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + serializer.errors)
				self.code = status.HTTP_400_BAD_REQUEST
		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	def destroy(self, request, *args, **kwargs):
		try:
			# Get the instance of the requested word to destroy
			instance = CustomDictionary.objects.get(id=kwargs['data']['word'])
			instance.is_active = False
			instance.is_deleted = True
			instance.save()

			self.response_data['data']['id'] = instance.id
			self.response_data['data']['word'] = instance.word
			self.code = status.HTTP_200_OK

		except Exception as e:
			logging.getLogger('error_logger').exception("[API - CustomDictionaryViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - CustomDictionaryViewSet] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class TopicViewSet(viewsets.ModelViewSet):
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
	queryset = Search.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = SearchSerializer
	pagination_class = StandardResultsSetPagination

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get_serializer_class(self):
		if self.action in ['recent_search','word_details']:
			return RecentSearchSerializer
		return SearchSerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def recent_search(self, request, *args, **kwargs):
		try:
			print("-------recent_search-----------")
			# 1. Get the recently search of the current user
			serializer = SearchSerializer(self.queryset, many=True)
			self.response_data['data']['recently_search'] = json.loads(json.dumps(serializer.data))

			# 2. Get the total of search of the current user
			total_search = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user']
			).count()

			# Then, calculate the % of the positive and negative search done 
			# by the current user
			self.response_data['data']['weighted_group'] = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user']
			).values('polarity').annotate(
				weighted_group=Count('polarity')*100/total_search)

			# 3. Get the total of the positive search
			total_positive_search = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				polarity='P'
			).count()

			# Then, get the top five positive most wanted words of the 
			# current user 
			self.response_data['data']['top_positive_search'] = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				polarity='P'
			).values('word').order_by('-count').annotate(count=Count('word')*100/total_positive_search)[:5]

			# 4. Get the total of the negative search
			total_negative_search = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				polarity='N'
			).count()

			# Then, get the top negative positive most wanted words of the 
			# current user
			self.response_data['data']['top_negative_search'] = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				polarity='N'
			).values('word').order_by('-count').annotate(count=Count('word')*100/total_negative_search)[:5]

			self.code = status.HTTP_200_OK
		except Exception as e:
			logging.getLogger('error_logger').exception("[RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)
	def word_details(self, request, *args, **kwargs):
		try:
			print("-------word_details-----------")
			self.response_data['data']['word'] = kwargs['data']['word']
			# 1. Get the information related with the timeline of the word 
			# on Twitter in function of polarity
			queryset = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				word=kwargs['data']['word']
			).values('polarity','sentiment_analysis_percentage','searched_date').order_by('id')

			serializer = SearchSerializer(queryset, many=True)
			self.response_data['data']['timeline_word_twitter_polarity'] = json.loads(json.dumps(serializer.data))

			# 2. Get the information related with the timeline of the word
			# on Twitter in function of likes
			queryset = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				word=kwargs['data']['word']
			).values('liked','searched_date').order_by('id')

			serializer = LikesSerializer(queryset, many=True)
			self.response_data['data']['timeline_word_twitter_likes'] = json.loads(json.dumps(serializer.data))

			# 3. Get the information related with the timeline of the word
			# on Twitter in function of retweets
			queryset = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				word=kwargs['data']['word']
			).values('shared','searched_date').order_by('id')

			serializer = SharedSerializer(queryset, many=True)
			self.response_data['data']['timeline_word_twitter_shared'] = json.loads(json.dumps(serializer.data))

			self.code = status.HTTP_200_OK
		except Exception as e:
			logging.getLogger('error_logger').exception("[RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

class WordRootViewSet(viewsets.ModelViewSet):
	queryset = WordRoot.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = WordRootSerializer
	pagination_class = StandardResultsSetPagination

class SocialNetworkAccountsViewSet(viewsets.ModelViewSet):
	queryset = SocialNetworkAccounts.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = SocialNetworkAccountsSerializer
	pagination_class = StandardResultsSetPagination

