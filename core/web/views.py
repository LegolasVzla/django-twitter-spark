#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from api.models import (User,Language,Dictionary,CustomDictionary,
	SocialNetwork,Search,Topic,WordRoot)
from api.serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	WordRootSerializer,SocialNetworkAccounts)
from api.api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,SearchViewSet,WordRootViewSet,SocialNetworkAccountsViewSet,
	WordCloudViewSet)

from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (HttpResponse, HttpResponseForbidden, 
	HttpResponseRedirect)
from django.views.generic import View
from django.http import JsonResponse
from django.http import QueryDict

from rest_framework import status
from rest_framework.response import Response
#from rest_framework import views
#from rest_framework.decorators import api_view
#from rest_framework import generics
#from django.core.exceptions import ObjectDoesNotExist
#from rest_framework.permissions import IsAuthenticated

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
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			_user = UserViewSet()
			_user.user_details(request,user=1)
			self.response_data['data'] = _user.response_data['data']
			self.code = _user.code
			self.response_data['data']['code'] = self.code

		except Exception as e:
			logging.getLogger('error_logger').exception("[UserProfileView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[UserProfileView] - Error: " + str(e))
		return render(request,'web/profile_get.html',self.response_data)

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
			# In the modal of "Ver Mi Diccionario" section,
			# when edit the polarity of a word, show the polarity
			if request.is_ajax():
				_customdictionary = CustomDictionaryViewSet()
				_customdictionary.custom_dictionary_polarity_get(
					request,word=request.GET['word_id'])
				self.response_data['data'] = _customdictionary.response_data['data']
				self.code = _customdictionary.code
				self.response_data['data']['code'] = self.code
				return JsonResponse(self.response_data)

			# Display all the default data in "Ver Mi Diccionario" section
			else:
				_customdictionary = CustomDictionaryViewSet()
				_customdictionary.custom_dictionary_kpi(request,language=1,user=1)
				self.response_data['data'] = _customdictionary.response_data['data']
				self.code = _customdictionary.code
				return render(request,template_name='web/dictionary_get.html',status=self.code,context=self.response_data)

		except Exception as e:
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[CustomDictionaryView] - Error: " + str(e))
			return JsonResponse(self.response_data)

	def post(self, request, *args, **kwargs):
		try:
			if request.method == 'POST' and request.is_ajax():
				if request.POST['polarity'] == 'true':
					new_polarity = 'P'
				elif request.POST['polarity'] == 'false':
					new_polarity = 'N'
				else:
					new_polarity = 'None'

				# In the modal of "Ver Mi Diccionario" section,
				# when add a new word to your custom dictionary
				_customdictionary = CustomDictionaryViewSet()
				_customdictionary.create(request,word=request.POST['word'],
					polarity=new_polarity,language=1,user=1)
				self.response_data['data'] = _customdictionary.response_data['data']
				self.code = _customdictionary.code
				self.response_data['data']['code'] = self.code

		except Exception as e:
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[CustomDictionaryView] - Error: " + str(e))
		return JsonResponse(self.response_data)

	def put(self, request, *args, **kwargs):
		try:
			if request.method == 'PUT' and request.is_ajax():
				# Check the new polarity value for the word
				if request.GET['polarity'] == 'true':
					new_polarity = 'P'
				elif request.GET['polarity'] == 'false':
					new_polarity = 'N'
				else:
					new_polarity = 'None'

				# In the modal of "Ver Mi Diccionario" section,
				# when edit the polarity of a word, save the changes
				_customdictionary = CustomDictionaryViewSet()
				_customdictionary.update(request,word=request.GET['word_id'],
					polarity=new_polarity)
				self.code = _customdictionary.code
				self.response_data['data'] = _customdictionary.response_data['data']

		except Exception as e:
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[CustomDictionaryView] - Error: " + str(e))
		return JsonResponse(self.response_data)

	def delete(self, request, *args, **kwargs):
		try:
			if request.method == 'DELETE' and request.is_ajax():
				# In the modal of "Ver Mi Diccionario" section,
				# when delete a word selected
				_customdictionary = CustomDictionaryViewSet()
				delete = QueryDict(request.body)
				word_id = delete.get('word_id')
				_customdictionary.destroy(request,word=word_id)
				self.response_data['data'] = _customdictionary.response_data['data']
				self.code = _customdictionary.code
				self.response_data['data']['code'] = self.code

		except Exception as e:
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[CustomDictionaryView] - Error: " + str(e))
		return JsonResponse(self.response_data)

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
		#return render(request,'web/word_searched_details_twitter.html',self.response_data)
		return JsonResponse(self.response_data)
		#return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		#return HttpResponseRedirect('web/word_searched_details_twitter.html',self.response_data)
		#return JsonResponse({'code':self.code,'url':'web/word_searched_details_twitter.html','data':self.response_data['data']})
		#return JsonResponse({'code':self.code,'url':reverse('timeline_search_twitter'),'data':self.response_data['data']})

