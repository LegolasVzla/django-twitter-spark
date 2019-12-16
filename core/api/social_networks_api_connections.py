from core.settings import (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,
	ACCESS_TOKEN_SECRET)
import tweepy
from tweepy.parsers import JSONParser
from tweepy.error import TweepError

class SocialNetworksApiConnections(object):
	"""docstring for SocialNetworksApiConnections"""
	def __init__(self, arg):
		super(SocialNetworksApiConnections, self).__init__()
		self.arg = arg

	def tweepy_connection(self):
		try:
			auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
			auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
			tweepy_api_client = tweepy.API(auth,parser=tweepy.parsers.JSONParser())
		except tweepy.TweepError as e:
			print ("[ ERROR ] Fail tweepy connection. Error: " + str(e))
		return tweepy_api_client
