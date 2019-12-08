from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A Serializer that takes an additional `fields` argument that
    controls which fields should be used.
    """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        excluded_fields = kwargs.pop("excluded_fields", None)
        required_fields = kwargs.pop("required_fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

            if isinstance(fields, dict):
                for field, config in fields.items():
                    set_attrs(self.fields[field], config)

        if excluded_fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in excluded_fields:
                self.fields.pop(field_name)

        if required_fields is not None:
            for field_name in required_fields:
                self.fields[field_name].required = True

class UserSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	first_name = serializers.CharField(allow_blank=False, max_length=100)
	last_name = serializers.CharField(allow_blank=False, max_length=100)
	class Meta:
		model = User
		fields = ('__all__')

class UserDetailsSerializer(serializers.ModelSerializer):
	user = serializers.Field()
	class Meta:
		model = User
		fields = ('user',)

class UserProfileUpdateSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email','first_name','last_name')

	def update(self, instance, data):
		instance.first_name = data.get("first_name")
		instance.last_name = data.get("last_name")
		instance.save()
		return instance

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
		fields = ('user','language')

class CustomDictionaryPolaritySerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomDictionary
		fields = ('polarity',)

	def update(self, instance, data):
		instance.polarity = data.get("polarity")
		instance.save()
		return instance
	
class TopicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Topic
		fields = ('__all__')

class SearchSerializer(serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = Search
		fields = ('__all__')

	def __init__(self, instance=None, data=None, **kwargs):
		super(SearchSerializer, self).__init__(instance, data, **kwargs)
		if instance is not None and instance._fields is not None:     
			allowed = set(instance._fields)
			existing = set(self.fields.keys())
			for fn in existing - allowed:
				self.fields.pop(fn)

class RecentSearchSerializer(serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	#user = serializers.IntegerField(source='user_id')
	class Meta:
		model = Search
		fields = ('user','social_network','word','searched_date')

class SentimentAnalysisSerializer(serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = Search
		fields = ('polarity','searched_date','sentiment_analysis_percentage')

class LikesSerializer(serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = Search
		fields = ('liked','searched_date')

class SharedSerializer(serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = Search
		fields = ('shared','searched_date')

class WordRootSerializer(serializers.ModelSerializer):
	class Meta:
		model = WordRoot
		fields = ('__all__')

class SocialNetworkAccountsSerializer(serializers.ModelSerializer):
	class Meta:
		model = SocialNetworkAccounts
		fields = ('__all__')
