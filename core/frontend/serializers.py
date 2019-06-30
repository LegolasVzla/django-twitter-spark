from .models import (User,Dictionaries,CustomDictionaries,Topics,WordRoots)
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('__all__')

class DictionariesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Dictionaries
		fields = ('id','word','polarity','language','is_active','is_deleted')

class CustomDictionariesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomDictionaries
		fields = ('id','user','word','polarity','language','is_active','is_deleted')

class TopicsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Topics
		fields = ('id','name','language','is_active','is_deleted')

class WordRootsSerializer(serializers.ModelSerializer):
	class Meta:
		model = WordRoots
		fields = ('id','word_root','topics','is_active','is_deleted')
