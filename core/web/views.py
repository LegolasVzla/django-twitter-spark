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
#from django.core.exceptions import ObjectDoesNotExist
#from rest_framework.permissions import IsAuthenticated
from api.models import (User,Language,Dictionary,CustomDictionary,
	SocialNetwork,Search,Topic,WordRoot)
from api.serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	WordRootSerializer,SocialNetworkAccounts)

import json
import requests
import logging

class IndexView(View):
	'''Load index form'''
	def get(self, request, *args, **kwargs):
		word_cloud_url = ''
		try:
			word_cloud_url = "http://127.0.0.1:8000/api/wordcloud/"
			response = requests.post(word_cloud_url)
			response = response.content.decode('utf-8')
			word_cloud_json = json.loads(response)
			word_cloud_url = word_cloud_json['data']['url']
			data = { 
				"status": status.HTTP_200_OK,
				"data": { 
					"word_cloud_url": word_cloud_url 
				} 
			}	
		except Exception as e:
			logging.getLogger('error_logger').exception("[IndexView] - Error: " + str(e))
			word_cloud_url = '/images/word_cloud_masks/cloud500.png'
			data = { 
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"data": { 
					"word_cloud_url": word_cloud_url 
				} 
			}
		return render(request, 'web/index.html',data)

class UserProfileView(View):
	"""docstring for UserProfile"""
	def get(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Profile Get'

		return render(request, 'web/profile_get.html',content)

	def post(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Profile Create'

		return render(request, 'web/profile_create.html',content)

	def put(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Profile Upload'

		return render(request, 'web/profile_update.html',content)

	def remove(self, request, *args, **kwargs):
		pass

class CustomDictionaryView(View):
	"""docstring for CustomDictionaryView"""

	#@api_view(['GET', 'POST'])
	def get(self, request, *args, **kwargs):
		#data = {}
		#data['message'] = 'CustomDictionary Get'
		custom_dictionary = CustomDictionary.objects.all()
		serializer = CustomDictionarySerializer(custom_dictionary, many=True)
		#data=(JsonResponse(serializer.data, safe=False))
		return Response(serializer.data,status=200,template_name='web/dictionary_get.html')

	def post(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Dictionary Post'

		return render(request, 'web/dictionary_create.html',content)

	def put(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Dictionary Put'

		return render(request, 'web/dictionary_get.html',content)

	def remove(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Dictionary Remove'

		return render(request, 'web/dictionary_get.html',content)

class TwitterSearchView(View):
	"""docstring for TwitterSearchView"""
	def get(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Twitter Search'

		return render(request, 'web/twitter_search.html',content)

	def post(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Twitter Results '

		return render(request, 'web/twitter_results.html',content)

class RecentSearchTwitterView(View):
	"""docstring for RecentSearchTwitterView"""

	def get(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Recently Search Get'
#		return render(request, 'web/recent_search_twitter.html',content)
		return render(request, 'web/timeline_search_twitter.html',content)

	def post(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Recently Search Post'
		return render(request, 'web/timeline_search_twitter.html',content)

