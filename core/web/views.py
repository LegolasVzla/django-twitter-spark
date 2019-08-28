#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (HttpResponse, HttpResponseForbidden, 
	HttpResponseRedirect)
#from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.views.generic import View, RedirectView
#from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import (User,Language,Dictionary,CustomDictionary,
	SocialNetwork,Search,Topic,WordRoot)
from api.serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	WordRootSerializer)
import json
import requests

# Create your views here.
class IndexView(View):
	'''Load index form'''
	def get(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Hello Social Analyzer!'

		return render(request, 'web/index.html',content)

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

class DictionaryView(APIView):
	"""docstring for DictionaryView"""

	def get(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Dictionary Get'

		return render(request, 'web/dictionary_get.html',content)

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

class RecentTwitterSearchView(APIView):
	"""docstring for RecentTwitterSearchView"""

	def get(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Recently Search Get'
		return render(request, 'web/recently_search_twitter.html',content)

	def post(self, request, *args, **kwargs):
		content = {}
		content['message'] = 'Recently Search Post'
		return render(request, 'web/twitter_timeline.html',content)

