from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Languages(models.Model):
	name = models.CharField( max_length = 100)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(default=timezone.now)

class Dictionaries(models.Model):
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
	language_id = models.ForeignKey(Languages,related_name='dictionaries_language_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.word
 	def __unicode__(self ):
 		return self.word

class CustomDictionaries(models.Model):
    NEUTRAL = 'None'
    POSITIVE = 'P'
    NEGATIVE = 'N'
    POLARITY_CHOICES = [
        (NEUTRAL, 'Neutral'),
        (POSITIVE, 'Positive'),
        (NEGATIVE, 'Negative'),
    ]
	user_id = models.ForeignKey(User,related_name='custom_dictionaries_user_id',on_delete=models.CASCADE)
	word = models.CharField( max_length = 100)
    polarity = models.CharField(
        max_length=4,
        choices=POLARITY_CHOICES,
        default=NEUTRAL,
    )	
	language_id = models.ForeignKey(Languages,related_name='custom_dictionaries_language_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.word
 	def __unicode__(self ):
 		return self.word

class SocialNetwork(models.Model):
	name = models.CharField( max_length = 100)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(default=timezone.now)

class Searched(models.Model):
    NEUTRAL = 'None'
    POSITIVE = 'P'
    NEGATIVE = 'N'
    POLARITY_CHOICES = [
        (NEUTRAL, 'Neutral'),
        (POSITIVE, 'Positive'),
        (NEGATIVE, 'Negative'),
    ]
	user_id = models.ForeignKey(User,related_name='searched_user_id',on_delete=models.CASCADE)
	word = models.CharField( max_length = 100)
    polarity = models.CharField(
        max_length=4,
        choices=POLARITY_CHOICES,
        default=NEUTRAL,
    )	
	topic = models.CharField( max_length = 100, null = True)
	liked = models.IntegerField(default=0)	
	retweeted = models.IntegerField(default=0)	
	searched_date = models.DateTimeField(default=datetime.now)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.word
 	def __unicode__(self ):
 		return self.word

class Topics(models.Model):
	name = models.CharField( max_length = 100)
	language_id = models.ForeignKey(Languages,related_name='topics_language_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(default=timezone.now)

class WordRoots(models.Model):
	word_root = models.CharField( max_length = 100)
	topics_id = models.ForeignKey(Topics,related_name='word_roots_topics_id',on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	updated_date=models.DateTimeField(auto_now=True)
	created_date = models.DateTimeField(default=timezone.now)
