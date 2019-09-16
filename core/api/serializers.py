from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
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
		fields = ('__all__')

class CustomDictionarySerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomDictionary
		fields = ('__all__')

class CustomDictionaryKpiSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomDictionary
		fields = ('user_id','language_id')
	
class TopicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Topic
		fields = ('__all__')

class SearchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Search
		fields = ('__all__')

class WordRootSerializer(serializers.ModelSerializer):
	class Meta:
		model = WordRoot
		fields = ('__all__')

class SocialNetworkAccountsSerializer(serializers.ModelSerializer):
	class Meta:
		model = SocialNetworkAccounts
		fields = ('__all__')
