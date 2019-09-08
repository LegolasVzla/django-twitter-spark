from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
from rest_framework import viewsets, permissions
from .serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	WordRootSerializer,SocialNetworkAccountsSerializer)
from rest_framework import views
from rest_framework import status
#from rest_framework.views import APIView
#from rest_framework.decorators  import list_route
#from rest_framework.viewsets import GenericViewSet
#from rest_framework import serializers, validators
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from os import path
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import imageio

from core.settings import BASE_DIR 
import os
from os.path import exists
import logging

User = get_user_model()

class WordCloudViewSet(viewsets.ViewSet):

	def create(self, request, *args, **kwargs):
		url = ''
		try:
			comments_list = request.data['data']['comments']
			user_id = request.data['data']['user_id']
			text = ' '.join(comments_list)
			colors_array = ['viridis', 'inferno', 'plasma', 'magma','Blues', 'BuGn', 'BuPu','GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd','PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu','Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd','afmhot', 'autumn', 'bone', 'cool','copper', 'gist_heat', 'gray', 'hot','pink', 'spring', 'summer', 'winter','BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr','RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral','seismic','Accent', 'Dark2', 'Paired', 'Pastel1','Pastel2', 'Set1', 'Set2', 'Set3', 'Vega10','Vega20', 'Vega20b', 'Vega20c','gist_earth', 'terrain', 'ocean', 'gist_stern','brg', 'CMRmap', 'cubehelix','gnuplot', 'gnuplot2', 'gist_ncar','nipy_spectral', 'jet', 'rainbow','gist_rainbow', 'hsv', 'flag', 'prism']
			colors = random.randint(0, 74)

			# Generating the word cloud
			wordcloud = WordCloud(stopwords=STOPWORDS,background_color='white',width=1800,height=1400,colormap= colors_array[colors],mask=imageio.imread('./static/images/cloud2.png')).generate(text)
			#wordcloud = WordCloud(background_color='white',width=1800,height=1400).generate(text)
			plt.imshow(wordcloud, interpolation='bilinear')
			plt.axis("off")

			if (os.path.exists(BASE_DIR + "/word_clouds")):
				os.chdir(BASE_DIR + "/word_clouds")
			else:
				os.mkdir(BASE_DIR + "/word_clouds")
				os.chdir(BASE_DIR + "/word_clouds")
			plt.savefig('./my_twitter_wordcloud.png', dpi=800,transparent = True, bbox_inches='tight', pad_inches=0)

			# Getting the url of the word cloud image generated
			url = os.getcwd() + '/' + os.listdir(os.getcwd())[0]

			os.chdir(BASE_DIR)
			data = { "status": status.HTTP_200_OK, "data": { "url": url } }

			return Response(data)
			
		except Exception as e:
			data = { "status": status.HTTP_500_INTERNAL_SERVER_ERROR, "data": { "url": url } }
			return Response(data)

	def list(self, request, *args, **kwargs):

		word_cloud= [{"id": 20, "path": "location/word_cloud.png"}]
		data = { "code": 204 }
		return Response(data,status=status.HTTP_200_OK)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    #page_size_query_param = 'page_size'
    #max_page_size = 1000


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = UserSerializer
	pagination_class = StandardResultsSetPagination

class DictionaryViewSet(viewsets.ModelViewSet):
	queryset = Dictionary.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DictionarySerializer
	pagination_class = StandardResultsSetPagination

class CustomDictionaryViewSet(viewsets.ModelViewSet):
	queryset = CustomDictionary.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CustomDictionarySerializer
	pagination_class = StandardResultsSetPagination

class TopicViewSet(viewsets.ModelViewSet):
	queryset = Topic.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = TopicSerializer
	pagination_class = StandardResultsSetPagination

class SearchViewSet(viewsets.ModelViewSet):
	queryset = Search.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = SearchSerializer
	pagination_class = StandardResultsSetPagination

class WordRootViewSet(viewsets.ModelViewSet):
	queryset = WordRoot.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = WordRootSerializer
	pagination_class = StandardResultsSetPagination

class SocialNetworkAccountsViewSet(viewsets.ModelViewSet):
	queryset = SocialNetworkAccounts.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = SocialNetworkAccountsSerializer
	pagination_class = StandardResultsSetPagination

