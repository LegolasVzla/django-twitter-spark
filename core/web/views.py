#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from api.models import (User,Language,Dictionary,CustomDictionary,
	SocialNetwork,Search,Topic,WordRoot)
from api.serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	WordRootSerializer,SocialNetworkAccounts)
from api.api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,SearchViewSet,WordRootViewSet,SocialNetworkAccountsViewSet,
	WordCloudViewSet,TwitterViewSet,BigDataViewSet)

from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (HttpResponse, HttpResponseForbidden, 
	HttpResponseRedirect)
from django.views.generic import View
from django.http import JsonResponse
from django.http import QueryDict

from rest_framework import status
import logging

class IndexView(View):
	'''Load index form'''
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		'''
		This action will call 2 endpoints, first will get tweets for 
		timeline, second one for wordcloud generation. In the future, 
		with a frontend framework, the first endpoint should be splitted
		to make async calls. It's possible to also use Celery to achieve 
		this behaviour. 
		'''
		try:
			word_cloud_tweets_data = ''
			self.response_data['data']['wordcloud'] = {}

			# Calling to Spark endpoint to get current tweets by text mining
			# process with nltk 
			_bigData = BigDataViewSet()
			_bigData.process_tweets(request,social_network=1)
			tweets_processed = _bigData.response_data['data']
			#tweets_processed= [{'account_name': 'CaraotaDigital', 'text': '#18Abr | El hampa no acata la cuarentena! varias escuelas han sido robadas por la ausencia de personal | Por:… https://t.co/IFj5n8Kc1C', 'clean_tweet': 'abr hampa acata cuarentena varias escuelas sido robadas ausencia personal ...', 'topic': 'Educación - Salud', 'created_at': 'Sat Apr 18 23:44:08 +0000 2020', 'formated_date': '18 Apr 2020 19:44:08'}, {'account_name': 'CaraotaDigital', 'text': 'Encuesta COVID-19: el 89,2% del territorio venezolano presenta fallas en el servicio eléctrico https://t.co/5b1apaMUae .*', 'clean_tweet': 'encuesta covid territorio venezolano presenta fallas servicio electrico', 'topic': 'Tecnología', 'created_at': 'Sat Apr 18 23:43:37 +0000 2020', 'formated_date': '18 Apr 2020 19:43:37'}]

			self.response_data['data']['tweets_processed'] = tweets_processed[0]['timeline']

			# Generating word cloud with current tweets
			_wordcloud = WordCloudViewSet()
			_wordcloud.create(request,user=1,comments=tweets_processed[0]['wordcloud'])
			self.response_data['data']['wordcloud'] = _wordcloud.response_data['data'][0]
			self.code = _wordcloud.code

		except Exception as e:
			logging.getLogger('error_logger').exception("[IndexView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[IndexView] - Error: " + str(e))
		return render(request,template_name='web/index.html',status=self.code,context=self.response_data)

class UserProfileView(View):
	"""docstring for UserProfile"""
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			print("------user profile get------")
			_user = UserViewSet()
			_user.user_details(request,user=1)
			self.response_data['data'] = _user.response_data['data'][0]
			self.code = _user.code
			self.response_data['data']['code'] = self.code

		except Exception as e:
			logging.getLogger('error_logger').exception("[UserProfileView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[UserProfileView] - Error: " + str(e))
		return render(request,'web/profile_get.html',self.response_data)

	def post(self, request, *args, **kwargs):
		print("------user profile post------")
		data = {}
		data['message'] = 'Profile Create'

		return render(request, 'web/profile_create.html',data)

	def put(self, request, *args, **kwargs):
		print("------user profile put------")
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
				self.response_data['data'] = _customdictionary.response_data['data'][0]
				self.code = _customdictionary.code
				self.response_data['data']['code'] = self.code
				return JsonResponse(self.response_data)

			# Display all the default data in "Ver Mi Diccionario" section
			else:
				_customdictionary = CustomDictionaryViewSet()
				_customdictionary.custom_dictionary_kpi(request,language=1,user=1)
				self.response_data['data'] = _customdictionary.response_data['data'][0]
				_customdictionary.user_custom_dictionary(request,language=1,user=1)
				self.response_data['data'] = _customdictionary.response_data['data'][0]
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
				self.response_data['data'] = _customdictionary.response_data['data'][0]
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
				_customdictionary.update(request,id=request.GET['word_id'],polarity=new_polarity)
				self.code = _customdictionary.code
				self.response_data['data'] = _customdictionary.response_data['data'][0]

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
				self.response_data['data'] = _customdictionary.response_data['data'][0]
				self.code = _customdictionary.code
				self.response_data['data']['code'] = self.code

		except Exception as e:
			logging.getLogger('error_logger').exception("[CustomDictionaryView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[CustomDictionaryView] - Error: " + str(e))
		return JsonResponse(self.response_data)

class TwitterSearchView(View):
	"""docstring for TwitterSearchView"""
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 200

	def get(self, request, *args, **kwargs):
		data = {}
		data['message'] = 'Twitter Search'

		return render(request, 'web/twitter_search.html',data)

	def post(self, request, *args, **kwargs):
		try:
			if request.method == 'POST' and request.is_ajax():
				_twitter_search = BigDataViewSet()
				#import pdb;pdb.set_trace()
				_twitter_search.twitter_search(request,text=request.POST['word'],user=1,language=1)
				self.response_data['data'] = _twitter_search.response_data['data'][0]
				self.code = _twitter_search.code
				self.response_data['data']['code'] = self.code

		except Exception as e:
			logging.getLogger('error_logger').exception("[TwitterSearchView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[TwitterSearchView] - Error: " + str(e))
		#return JsonResponse(self.response_data)
		#return render(self.request, 'web/twitter_search.html',data)
		return render(request,template_name='web/twitter_search.html',status=self.code,context=self.response_data)

class RecentSearchTwitterView(View):
	"""docstring for RecentSearchTwitterView"""
	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': {}}
		self.code = 0

	def get(self, request, *args, **kwargs):
		try:
			_recent_search = SearchViewSet()
			_recent_search.recent_search_kpi(request,social_network=1,user=1)
			self.response_data['data'] = _recent_search.response_data['data'][0]
			_recent_search.recent_search(request,social_network=1,user=1)
			self.response_data['data'] = _recent_search.response_data['data'][0]
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
			_recent_search.twitter_timeline_polarity(request,social_network=1,
				word=request.GET.get('word',None),user=1)
			self.response_data['data'] = _recent_search.response_data['data'][0]

			_recent_search.twitter_timeline_likes(request,social_network=1,
				word=request.GET.get('word',None),user=1)
			self.response_data['data'] = _recent_search.response_data['data'][0]

			_recent_search.twitter_timeline_shared(request,social_network=1,
				word=request.GET.get('word',None),user=1)
			self.response_data['data'] = _recent_search.response_data['data'][0]

			self.code = status.HTTP_200_OK
			self.response_data['data']['code'] = self.code
			#import pdb;pdb.set_trace()

		except Exception as e:
			logging.getLogger('error_logger').exception("[TimelineSearchTwitterView] - Error: " + str(e))
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[TimelineSearchTwitterView] - Error: " + str(e))
		#return render(request,'web/word_searched_details_twitter.html',self.response_data)
		return render(request,template_name='web/word_searched_details_twitter.html',status=self.code,context=self.response_data)
		#return JsonResponse(self.response_data)
		#return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		#return HttpResponseRedirect('web/word_searched_details_twitter.html',self.response_data)
		#return JsonResponse({'code':self.code,'url':'web/word_searched_details_twitter.html','data':self.response_data['data']})
		#return JsonResponse({'code':self.code,'url':reverse('timeline_search_twitter'),'data':self.response_data['data']})

