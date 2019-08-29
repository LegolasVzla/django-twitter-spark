from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()

# Create your models here.
class Language(models.Model):
	name = models.CharField( max_length = 100)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(auto_now_add=True)

class Dictionary(models.Model):
	NEUTRAL = 'None'
	POSITIVE = 'P'
	NEGATIVE = 'N'
	POLARITY_CHOICES = [
	    (NEUTRAL, 'Neutral'),
	    (POSITIVE, 'Positive'),
	    (NEGATIVE, 'Negative'),
	]
	#__polarity_values=((1,_('Positive')),(2,_('Negative')),(3,_('Neutral')))
	word = models.CharField( max_length = 100)
	polarity = models.CharField(
	    max_length=4,
	    choices=POLARITY_CHOICES,
	    default=NEUTRAL,
	)
	#polarity = models.CharField(choices = __polarity_values)
	language = models.ForeignKey(Language,related_name='dictionary_language_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.word
	def __unicode__(self ):
		return self.word

class CustomDictionary(models.Model):
    NEUTRAL = 'None'
    POSITIVE = 'P'
    NEGATIVE = 'N'
    POLARITY_CHOICES = [
        (NEUTRAL, 'Neutral'),
        (POSITIVE, 'Positive'),
        (NEGATIVE, 'Negative'),
    ]
    user = models.ForeignKey(User,related_name='custom_dictionary_user_id',on_delete=models.CASCADE)
    word = models.CharField( max_length = 100)
    polarity = models.CharField(
		max_length=4,
		choices=POLARITY_CHOICES,
		default=NEUTRAL,
	)
    language = models.ForeignKey(Language,related_name='custom_dictionary_language_id',on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    updated_date=models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.word
    def __unicode__(self ):
    	return self.word

class SocialNetwork(models.Model):
	name = models.CharField( max_length = 100)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(auto_now_add=True)

class Topic(models.Model):
	name = models.CharField( max_length = 100)
	language = models.ForeignKey(Language,related_name='topic_language_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(auto_now_add=True)

class Search(models.Model):
	NEUTRAL = 'None'
	POSITIVE = 'P'
	NEGATIVE = 'N'
	POLARITY_CHOICES = [
		(NEUTRAL, 'Neutral'),
		(POSITIVE, 'Positive'),
		(NEGATIVE, 'Negative'),
	]
	user = models.ForeignKey(User,related_name='searched_user_id',on_delete=models.CASCADE)
	word = models.CharField( max_length = 100)
	social_network = models.ForeignKey(SocialNetwork,related_name='search_social_network_id',on_delete=models.CASCADE)
	polarity = models.CharField(
	    max_length=4,
	    choices=POLARITY_CHOICES,
	    default=NEUTRAL,
	)
	topic = models.ForeignKey(Topic,related_name='search_topic_id',on_delete=models.CASCADE)
	liked = models.IntegerField(default=0)	
	shared = models.IntegerField(default=0)	
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	searched_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.word
	def __unicode__(self ):
		return self.word
	
class WordRoot(models.Model):
	word_root = models.CharField( max_length = 100)
	topic = models.ForeignKey(Topic,related_name='word_root_topic_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(auto_now_add=True)

class SocialNetworkAccounts(models.Model):
	name = models.CharField( max_length = 100)
	social_network = models.ForeignKey(SocialNetwork,related_name='social_network_accounts_social_network_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(auto_now_add=True)