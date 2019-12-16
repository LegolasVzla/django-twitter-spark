# django-twitter-spark
Thesis project: topic categorization and sentiment analysis on twitter

Summary
---------------
The presently work was an academic thesis, about how to make topic categorization and sentiment analysis of tweets in Python, using algorithms of Text Mining and Natural Language Processing (NLP) with Apache Spark. Adittionally a web application in Django was developt to display a several of graphics indicators like: a wordcloud and other interesting graphics.

* Status: orienting all to APIs and adding improvements.

Authors:
---------------
- Manuel Araujo

- Manuel Carrero

## Technologies
- [Django REST framework](https://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

- [Apache Spark](https://spark.apache.org/) is a unified analytics engine for large-scale data processing.

- [PostgreSQL](https://www.postgresql.org/) is the World's Most Advanced Open Source Relational Database.

- [Tweepy](https://www.tweepy.org/) is an easy-to-use Python library for accessing the Twitter API.

- [NLTK (Natural Language Toolkit)](https://www.nltk.org/) is a leading platform for building Python programs to work with human language data.

What would happen if we integrate this technologies?...Let's check it!

## Requirements
- Ubuntu 18
- Install PostgreSQL:
```
  sudo apt-get update
  sudo apt install python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev
```
## Installation

Create your virtualenv (see Troubleshooting section) and install the requirements:

	virtualenv env --python=python3
	source env/bin/activate

	pip install -r requirements.txt

In "django-twitter-spark/core/" path, create logs folder:

	mkdir logs

In "django-twitter-spark/core/" path, create a **settings.ini** file, with the structure as below:

	[postgresdbConf]
	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=dbname
	DB_USER=user
	DB_PASS=password
	DB_HOST=host
	DB_PORT=port

	[tweepyConf]
	CONSUMER_KEY = <consumer_key>
	CONSUMER_SECRET = <consumer_secret>
	ACCESS_TOKEN = <access_token>
	ACCESS_TOKEN_SECRET = <access_token_secret>

- postgresdbConf section: fill in with your own PostgreSQL credentials. By default, DB_HOST and DB_PORT in PostgreSQL are localhost/5432.

Default credentials for admin superuser are: admin@admin.com / admin. Then run the migrations:

	python manage.py makemigrations

	python manage.py migrate

- tweepyConf section: register a [Tweepy account](https://developer.twitter.com/en/apply-for-access) and fill in with your own credentials.

Generate default data with the fixtures:

	python3 fixtures_load.py

Run the server:

	python manage.py runserver

You could see the home page in:

	http://127.0.0.1:8000/socialanalyzer/

## Models

- Topic: is about people are talking in a specific moment in a social network.
- Word root: is a word or word part that can form the basis of new words through the addition of prefixes and suffixes.
- Dictionary: is a set of word that contains positive and negative words.
- CustomDictionary: is a customizable set of words per user, with positive and negative words
- Search: is a tracking table where you could find you recently search.
- SocialNetworkAccounts: is a set of social networks accounts used to sentiment analysis.

## Swagger Documentation

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a tool for API documentation. "Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption."

## Endpoints Structure

In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods (GET, POST, PUT, DELETE), making all posssible CRUD (create, retrieve, update, delete) operations.

You can see the endpoints structure in the Swagger UI documentation:
	
	http://127.0.0.1:8000/swagger/

Basically the structure is as below for all the main instances (User, Dictionaries, Custom Dictionaries, Topics and Word roots)

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`api/<instance>` | GET | READ | Get all the <instance> records
`api/<instance>/:id` | GET | READ | Get a single <instance>
`api/<instance>`| POST | CREATE | Create a new <instance> record
`api/<instance>/:id` | PUT | UPDATE | Update a <instance> record
`api/<instance>/:id` | DELETE | DELETE | Delete a <instance> record

## Endpoints without Models

* Wordcloud: endpoint to list and generate Twitter word cloud images

Methods:

- POST (create): consist in a Twitter's comments word cloud image generation. It has the folow structure:

Input: a JSON format as below:

	{
		"data": {
			"comments": ["twitter comments list"],
			"user": '1'
		}
	}

Parameters:
- Mandatory: data, comments
- Optionals: user_id

If user_id is given (authenticated=True), it will generate a random word cloud with one of the mask located in:

	static/images/word_cloud_masks

In other case, word cloud will be with square form. The image will be generated in the follow path:

	/static/images/word_clouds/<user>

Output:

Success: return the url where is stored the image and an authenticated boolean

	{
	    "status": 200,
	    "data": {
	        "url": "",
	        "authenticated": 
	    }
	}

Fail: return a message with the error response

	{
	    "status": 500,
	    "data": {},
	    "error:" [message]
	}

## Contributions
------------------------

All work to improve performance is good

Enjoy it!
