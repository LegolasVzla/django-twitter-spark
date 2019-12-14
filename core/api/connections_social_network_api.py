from core.settings import (DATABASES,CONSUMER_SECRET,ACCESS_TOKEN,
	ACCESS_TOKEN_SECRET)

def tweepy_connection():
	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
	except Exception as e:
		print ("[ ERROR ] Fail tweepy connection. Error: " + str(e))
	return client