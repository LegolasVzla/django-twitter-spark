from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
from rest_framework import viewsets, permissions
from .serializers import (UserSerializer,DictionarySerializer,
	CustomDictionarySerializer,TopicSerializer,SearchSerializer,
	WordRootSerializer,SocialNetworkAccountsSerializer,WordCloudSerializer)
from rest_framework import views
#from rest_framework.views import APIView
from rest_framework.decorators  import list_route
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, validators
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from core.settings import BASE_DIR 
import os
from os.path import exists
import logging

User = get_user_model()

class WordCloudViewSet(viewsets.ViewSet):
	os.chdir(BASE_DIR)

	def create(self, request, *args, **kwargs):
		word_cloud= [{"id": 10, "path": "location/word_cloud.png"}]
		results = WordCloudSerializer(word_cloud, many=True).data
		return Response(results)

	def list(self, request, *args, **kwargs):
		word_cloud= [{"id": 20, "path": "location/word_cloud.png"}]
		results = WordCloudSerializer(word_cloud, many=True).data
		return Response(results)

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

