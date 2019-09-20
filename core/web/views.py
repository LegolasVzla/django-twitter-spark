#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (HttpResponse, HttpResponseForbidden, 
	HttpResponseRedirect)
from django.views.generic import View
from rest_framework import status
#from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics
#from django.core.exceptions import ObjectDoesNotExist
#from rest_framework.permissions import IsAuthenticated
from api.models import (User,Language,Dictionary,CustomDictionary,
	SocialNetwork,Search,Topic,WordRoot)
from api.serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	WordRootSerializer,SocialNetworkAccounts)
from api.api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,SearchViewSet,WordRootViewSet,SocialNetworkAccountsViewSet,
	WordCloudViewSet)

import json
import requests
import logging

class IndexView(View):
	'''Load index form'''
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			_wordcloud = WordCloudViewSet()
			_wordcloud.create(request)
			self.response_data['data'] = _wordcloud.response_data['data']
			self.code = _wordcloud.code
			
		except Exception as e:
			logging.getLogger('error_logger').exception("[IndexView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[IndexView] - Error: " + str(e))
			self.response_data['data']['url'] = '/images/word_cloud_masks/cloud500.png'

		return render(request,template_name='web/index.html',status=self.code,context=self.response_data)

class UserProfileView(View):
	"""docstring for UserProfile"""
	def get(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Profile Get'

		return render(request, 'web/profile_get.html',data)

	def post(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Profile Create'

		return render(request, 'web/profile_create.html',data)

	def put(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Profile Upload'

		return render(request, 'web/profile_update.html',data)

	def remove(self, request, *args, **kwargs):
		pass

class CustomDictionaryView(generics.RetrieveAPIView):
	"""docstring for CustomDictionaryView"""
	get_queryset = CustomDictionary.objects.filter(
		is_active=True,
		is_deleted=False,
		language_id=1
	).order_by('id')
	renderer_classes = [TemplateHTMLRenderer]

	def __init__(self):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			#serializer = CustomDictionarySerializer(self.get_queryset, many=True)
			#data['data']=json.loads(json.dumps(serializer.data))
			self.response_data['data']['custom_dictionary'] = self.get_queryset 
			self.response_data['data']['total_words'] = CustomDictionary.objects.filter(
						is_active=True,
						is_deleted=False,
						language_id=1
					).count()
			self.response_data['data']['total_positive_words'] = CustomDictionary.objects.filter(
						is_active=True,
						is_deleted=False,
						language_id=1,
						polarity='P'						
					).count()
			self.response_data['data']['total_negative_words'] = CustomDictionary.objects.filter(
						is_active=True,
						is_deleted=False,
						language_id=1,
						polarity='N'						
					).count()					
			self.code = status.HTTP_200_OK
		except Exception as e:
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[CustomDictionaryView] - Error: " + str(e))
		return Response(self.response_data,status=self.code,template_name='web/dictionary_get.html')

	def post(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Dictionary Post'

		return render(request, 'web/dictionary_create.html',data)

	def put(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Dictionary Put'

		return render(request, 'web/dictionary_get.html',data)

	def remove(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Dictionary Remove'

		return render(request, 'web/dictionary_get.html',data)

class TwitterSearchView(View):
	"""docstring for TwitterSearchView"""
	def get(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Twitter Search'

		return render(request, 'web/twitter_search.html',data)

	def post(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Twitter Results '

		return render(request, 'web/twitter_results.html',data)

class RecentSearchTwitterView(generics.RetrieveAPIView):
	"""docstring for RecentSearchTwitterView"""
	get_queryset = Search.objects.filter(
		is_active=True,
		is_deleted=False,
		social_network_id=1
	).order_by('id')
	renderer_classes = [TemplateHTMLRenderer]

	def __init__(self):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			self.response_data['data']['total_words'] = self.get_queryset			
			self.response_data['data']['total_words']['total_positive_search'] = Search.objects.filter(
						is_active=True,
						is_deleted=False,
						polarity='P',
						social_network_id=1
					).count()
			self.response_data['data']['total_words']['total_positive_search'] = Search.objects.filter(
						is_active=True,
						is_deleted=False,
						polarity='N',
						social_network_id=1
					).count()
			self.response_data['data']['total_words']['total_positive_search'] = Search.objects.filter(
						is_active=True,
						is_deleted=False,
						polarity='None',
						social_network_id=1
					).count()
			self.response_data['data']['top_positive_search'] = Search.objects.filter(
						is_active=True,
						is_deleted=False,
						polarity='P',
						social_network_id=1
					).count()
			self.response_data['data']['top_negative_search'] = Search.objects.filter(
						is_active=True,
						is_deleted=False,
						polarity='N',
						social_network_id=1
					).count()					
			self.code = status.HTTP_200_OK
		except Exception as e:
			logging.getLogger('error_logger').exception("[RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[RecentSearchTwitterView] - Error: " + str(e))
		return Response(self.response_data,status=self.code,template_name='web/recent_search_twitter.html')
		#return Response(self.response_data,status=self.code,template_name='web/timeline_search_twitter.html')

	def word_searched_detail(self, request, id):
		pass

	def post(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Recently Search Post'
		return render(request, 'web/timeline_search_twitter.html',data)

