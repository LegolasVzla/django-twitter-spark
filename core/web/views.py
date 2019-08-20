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
	SocialNetwork,Searched,Topic,WordRoot)

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

	def post():
		pass

	def put():
		content = {}
		content['message'] = 'Profile Upload'

		return render(request, 'web/profile_update.html',content)

	def remove():
		pass

class DiccionaryView(APIView):
	"""docstring for DiccionaryView"""

	def get():
		pass

	def post():
		pass

	def put():
		pass

	def remove():
		pass

class TwitterSearchView(APIView):
	"""docstring for TwitterSearchView"""

	def get():
		pass

	def post():
		pass

	def put():
		pass

	def remove():
		pass

class RecentTwitterSearchView(APIView):
	"""docstring for RecentTwitterSearchView"""

	def get():
		pass

	def post():
		pass

	def put():
		pass

	def remove():
		pass
