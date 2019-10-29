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
from django.http import JsonResponse
#from rest_framework.decorators import api_view
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
			_wordcloud.create(request,user=1)
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

class CustomDictionaryView(View):
	"""docstring for CustomDictionaryView"""
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			_customdictionary = CustomDictionaryViewSet()
			_customdictionary.custom_dictionary_kpi(request,language=1,user=1)
			self.response_data['data'] = _customdictionary.response_data['data']
			self.code = _customdictionary.code
			
		except Exception as e:
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[CustomDictionaryView] - Error: " + str(e))
		return render(request,template_name='web/dictionary_get.html',status=self.code,context=self.response_data)

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

class RecentSearchTwitterView(View):
	"""docstring for RecentSearchTwitterView"""
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			_recent_search = SearchViewSet()
			_recent_search.recent_search(request,social_network=1,user=1)
			self.response_data['data'] = _recent_search.response_data['data']
			self.code = _recent_search.code
			
		except Exception as e:
			logging.getLogger('error_logger').exception("[RecentSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[RecentSearchTwitterView] - Error: " + str(e))
		return render(request,template_name='web/recent_search_twitter.html',status=self.code,context=self.response_data)

class TimelineSearchTwitterView(View):
	"""docstring for RecentSearchTwitterView"""
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			_recent_search = SearchViewSet()
			_recent_search.word_details(request,social_network=1,
				word=request.GET.get('word',None),user=1)
			self.response_data['data'] = _recent_search.response_data['data']
			self.code = _recent_search.code
			self.response_data['data']['code'] = self.code
			#import pdb;pdb.set_trace()

		except Exception as e:
			logging.getLogger('error_logger').exception("[TimelineSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[TimelineSearchTwitterView] - Error: " + str(e))
		return render(request,template_name='web/word_searched_details_twitter.html',status=self.code,context=self.response_data)
		#return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		#return HttpResponseRedirect('web/word_searched_details_twitter.html',self.response_data)
		#return JsonResponse({'code':200,'url':'web/word_searched_details_twitter.html','data':'timeline'})

