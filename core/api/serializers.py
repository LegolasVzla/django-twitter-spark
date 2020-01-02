from .models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)
#from rest_framework.serializers import ValidationError
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

class WordCloudAPISerializer(serializers.ModelSerializer):
	comments = serializers.CharField(required=True)
	user = serializers.IntegerField(source='id',required=False)
	class Meta:
		model = User
		fields = ('comments','user')

	def to_internal_value(self, data):
		required = []
		optionals = []
		for k in ['comments']:
			'''
			- Case 1: Is the k field in the data and it's empty?
			- Case 2: Is not the k field in the data?
			'''
			if (data.keys().__contains__(k) and data[k] == '') or (not data.keys().__contains__(k)):
				required.append(k)

		for k in ['user']:
			# Is not the k field in the data?
			if not data.keys().__contains__(k):
				optionals.append(k)

		if len(required) > 0 and len(optionals) > 0:
			raise ValueError("The following fields are required: %s" % ','.join(required) + " and the following fields are needed but can be empty: %s" % ','.join(optionals))

		elif len(required) > 0 and len(optionals) == 0:
			raise ValueError("The following fields are required: %s" % ','.join(required))

		elif len(required) == 0 and len(optionals) > 0:
			raise ValueError("The following fields are needed but can be empty: %s" % ','.join(optionals))

		return data

class UserSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	first_name = serializers.CharField(allow_blank=False, max_length=100)
	last_name = serializers.CharField(allow_blank=False, max_length=100)
	class Meta:
		model = User
		fields = ('__all__')

class UserDetailsAPISerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	user = serializers.IntegerField()
	class Meta:
		model = User
		fields = ('user',)

	def to_internal_value(self, data):
		required = []
		for k in ['user']:
			'''
			- Case 1: Is the k field in the data and it's empty?
			- Case 2: Is not the k field in the data?
			'''
			if (data.keys().__contains__(k) and data[k] == '') or (not data.keys().__contains__(k)):
				required.append(k)

		if len(required):
			raise ValueError("The following fields are required: %s" % ','.join(required))

		return data

class UserProfileUpdateAPISerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email','first_name','last_name')

	def update(self, instance, data):
		instance.first_name = data.get("first_name")
		instance.last_name = data.get("last_name")
		instance.save()
		return instance

	def to_internal_value(self, data):
		required = []
		optionals = []
		for k in ['email']:
			'''
			- Case 1: Is the k field in the data and it's empty?
			- Case 2: Is not the k field in the data?
			'''
			if (data.keys().__contains__(k) and data[k] == '') or (not data.keys().__contains__(k)):
				required.append(k)

		for k in ['first_name','last_name']:
			# Is not the k field in the data?
			if not data.keys().__contains__(k):
				optionals.append(k)

		if len(required) > 0 and len(optionals) > 0:
			raise ValueError("The following fields are required: %s" % ','.join(required) + " and the following fields are needed but can be empty: %s" % ','.join(optionals))

		elif len(required) > 0 and len(optionals) == 0:
			raise ValueError("The following fields are required: %s" % ','.join(required))

		elif len(required) == 0 and len(optionals) > 0:
			raise ValueError("The following fields are needed but can be empty: %s" % ','.join(optionals))

		return data

class DictionarySerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	class Meta:
		model = Dictionary
		fields = ('__all__')

class DictionaryPolarityAPISerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	class Meta:
		model = Dictionary
		fields = ('polarity','language')

class CustomDictionarySerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	class Meta:
		model = CustomDictionary
		fields = ('__all__')

class CustomDictionaryKpiAPISerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomDictionary
		fields = ('user','language')

class CustomDictionaryWordAPISerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomDictionary
		fields = ('user','word')

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

class SearchSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = Search
		fields = ('__all__')

class RecentSearchAPISerializer(serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = Search
		fields = ('user','social_network','searched_date')

class WordDetailsAPISerializer(serializers.ModelSerializer):
	searched_date = serializers.DateTimeField(format="%d-%m-%Y")
	#user = serializers.IntegerField(source='user_id')
	class Meta:
		model = Search
		fields = ('user','social_network','word','searched_date')

class WordRootSerializer(serializers.ModelSerializer):
	class Meta:
		model = WordRoot
		fields = ('__all__')

class SocialNetworkAccountsSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
	class Meta:
		model = SocialNetworkAccounts
		fields = ('__all__')

	def to_internal_value(self, data):
		required = []
		for k in ['social_network']:
			'''
			- Case 1: Is the k field in the data and it's empty?
			- Case 2: Is not the k field in the data?
			'''
			if (data.keys().__contains__(k) and data[k] == '') or (not data.keys().__contains__(k)):
				required.append(k)

		if len(required):
			raise ValueError("The following fields are required: %s" % ','.join(required))

		return data

class SocialNetworkAccountsAPISerializer(serializers.ModelSerializer):
	class Meta:
		model = SocialNetworkAccounts
		fields = ('social_network',)

	def to_internal_value(self, data):
		required = []
		for k in ['social_network']:
			'''
			- Case 1: Is the k field in the data and it's empty?
			- Case 2: Is not the k field in the data?
			'''
			if (data.keys().__contains__(k) and data[k] == '') or (not data.keys().__contains__(k)):
				required.append(k)

		if len(required):
			raise ValueError("The following fields are required: %s" % ','.join(required))

		return data