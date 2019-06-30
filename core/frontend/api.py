from .models import (User,Dictionaries,CustomDictionaries,Topics,WordRoots)
from rest_framework import viewsets, permissions
from .serializers import (UserSerializer,DictionariesSerializer,
	CustomDictionariesSerializer,TopicsSerializer,WordRootsSerializer)
from rest_framework import serializers, validators
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = UserSerializer
	pagination_class = StandardResultsSetPagination

class DictionariesViewSet(viewsets.ModelViewSet):
	queryset = Dictionaries.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DictionariesSerializer
	pagination_class = StandardResultsSetPagination

class CustomDictionariesViewSet(viewsets.ModelViewSet):
	queryset = CustomDictionaries.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CustomDictionariesSerializer
	pagination_class = StandardResultsSetPagination

class TopicsViewSet(viewsets.ModelViewSet):
	queryset = Topics.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = TopicsSerializer
	pagination_class = StandardResultsSetPagination

class WordRootsViewSet(viewsets.ModelViewSet):
	queryset = WordRoots.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = WordRootsSerializer
	pagination_class = StandardResultsSetPagination

