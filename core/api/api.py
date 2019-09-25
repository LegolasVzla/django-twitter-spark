from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
from rest_framework import viewsets, permissions
from .serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	RecentSearchSerializer,WordRootSerializer,SocialNetworkAccountsSerializer,
	CustomDictionaryKpiSerializer)
from django.db.models import Count
#import io
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser

from rest_framework import views
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action, detail_route
#from rest_framework.views import APIView
#from rest_framework.decorators  import list_route
#from rest_framework.viewsets import GenericViewSet
#from rest_framework import serializers, validators
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model

import json
import os
from os import path
from os.path import exists
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import imageio

from core.settings import BASE_DIR 
import logging
from functools import wraps
from rest_framework import exceptions

User = get_user_model()

def validate_field_name(f):
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
			"user_id": 1
		}
	}
	- Mandatory: comments
	- Optionals: user_id
	If user_id is given, it will generate a random word cloud with some 
	mask located in static/images/word_cloud_masks. In other case, wordcloud
	will be with square form		
	'''
	def __init__(self):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0
		self.error_message = ''

	def create(self, request, *args, **kwargs):
		user_id = ''
		try:
			user_id = kwargs['user']
		except Exception as e:
			user_id = request.data['data']['user_id']
		url = ''
		authenticated = False
		colors_array = ['viridis', 'inferno', 'plasma', 'magma','Blues', 'BuGn', 'BuPu','GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd','PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu','Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd','afmhot', 'autumn', 'bone', 'cool','copper', 'gist_heat', 'gray', 'hot','pink', 'spring', 'summer', 'winter','BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr','RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral','seismic','Accent', 'Dark2', 'Paired', 'Pastel1','Pastel2', 'Set1', 'Set2', 'Set3', 'Vega10','Vega20', 'Vega20b', 'Vega20c','gist_earth', 'terrain', 'ocean', 'gist_stern','brg', 'CMRmap', 'cubehelix','gnuplot', 'gnuplot2', 'gist_ncar','nipy_spectral', 'jet', 'rainbow','gist_rainbow', 'hsv', 'flag', 'prism']
		word_cloud_data = {"data": {"comments": ["Ea excepteur dolor velit sed qui non ad mollit minim incididunt laborum sunt laborum elit consequat eiusmod consequat ut deserunt est nostrud adipisicing officia cupidatat anim deserunt qui do eu veniam pariatur duis in non dolore incididunt cupidatat esse ut fugiat velit dolor consequat deserunt esse excepteur voluptate sit cillum in officia incididunt ad aute laboris in dolor mollit pariatur officia dolor do ad labore culpa sed sint duis esse labore sed adipisicing adipisicing ut laborum nostrud id do mollit anim qui ut irure cupidatat dolor magna occaecat in amet dolore sint aliquip ullamco eiusmod irure enim qui consequat sit nulla aliquip esse laboris incididunt dolore tempor aute velit deserunt eiusmod aliquip incididunt in pariatur labore dolor ut consequat velit elit mollit duis laboris ex amet dolore eu dolor proident tempor elit laboris quis laboris elit ut minim cupidatat reprehenderit nulla reprehenderit magna enim voluptate laborum ut occaecat esse sint consequat reprehenderit do deserunt ea enim deserunt officia officia minim dolor aliqua dolore esse veniam ut enim dolor incididunt elit dolor magna laborum ut anim exercitation esse dolore irure aute dolor elit officia velit ut reprehenderit minim nisi irure dolore fugiat dolore dolore cupidatat."], "user_id": user_id }}
		try:
			comments_list = word_cloud_data['data']['comments']
			text = ' '.join(comments_list)
			colors = random.randint(0, 74)
			print("Generating the wordcloud image...")
			# If user is authenticated
			if (word_cloud_data['data']['user_id']):
				authenticated = True
				user_id = word_cloud_data['data']['user_id']
				image = random.randint(0, 9)

				# Generating the custom random word cloud
				wordcloud = WordCloud(stopwords=STOPWORDS,background_color='white',width=1600,height=1200,colormap= colors_array[colors],mask=imageio.imread('./static/images/word_cloud_masks/cloud'+ str(image) +'.png')).generate(text)

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
			if not word_cloud_data['data']['comments']:
				self.error_message = 'Comments can"t be empty. '
			else:
				self.error_message = 'word_cloud_data format must be like: {"data": {"comments": ["twitter comments list"],"user_id": '' }} where user_id can be empty. '
			self.response_data['error'].append("[WordCloudViewSet] - Error: " + self.error_message + str(e))
			logging.getLogger('error_logger').exception("[WordCloudViewSet] - Error: " + self.error_message + str(e))
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
			logging.getLogger('error_logger').exception("[WordCloudViewSet] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return Response(self.response_data,status=self.code)

class StandardResultsSetPagination(PageNumberPagination):
	page_size = 10
	#page_size_query_param = 'page_size'
	#max_page_size = 1000

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

	@validate_field_name
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
			self.response_data['error'].append("[CustomDictionaryViewSet] - Error: " + str(e))			
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
		if self.action == 'recent_search':
			return RecentSearchSerializer
		return SearchSerializer

	@validate_field_name
	@action(methods=['post'], detail=False)
	def recent_search(self, request, *args, **kwargs):
		try:
			#import pdb;pdb.set_trace()

			# Get the recently search of the current user
			serializer = SearchSerializer(self.queryset, many=True)
			self.response_data['data']['recently_search'] = json.loads(json.dumps(serializer.data))

			# Get the total of search of the current user
			total_search = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user']
			).count()

			# Calculate the % of the positive and negative search done 
			# by the current user
			self.response_data['data']['weighted_group'] = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user']
			).values('polarity').annotate(
				weighted_group=Count('polarity')*100/total_search
			)

			# Get the top five positive most wanted words of the current user 
			self.response_data['data']['top_positive_search'] = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				polarity='P'
			).values('word').annotate(count=Count('word'))

			# Get the top negative positive most wanted words of the current user
			self.response_data['data']['top_negative_search'] = Search.objects.filter(
				is_active=True,
				is_deleted=False,
				social_network=kwargs['data']['social_network'],
				user_id=kwargs['data']['user'],
				polarity='N'
			).values('word').annotate(count=Count('word'))

			self.code = status.HTTP_200_OK
		except Exception as e:
			logging.getLogger('error_logger').exception("[RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[RecentSearchTwitterView] - Error: " + str(e))
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

