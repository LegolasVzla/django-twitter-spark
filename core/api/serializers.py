from .models import (User,Dictionary,CustomDictionary,Topic,WordRoot)
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('__all__')

class DictionarySerializer(serializers.ModelSerializer):
	class Meta:
		model = Dictionary
		fields = ('id','word','polarity','language','is_active','is_deleted')

class CustomDictionarySerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomDictionary
		fields = ('id','user','word','polarity','language','is_active','is_deleted')

class TopicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Topic
		fields = ('id','name','language','is_active','is_deleted')

class WordRootSerializer(serializers.ModelSerializer):
	class Meta:
		model = WordRoot
		fields = ('id','word_root','topic','is_active','is_deleted')
