# django-twitter-spark
Thesis project: topic categorization and sentiment analysis on twitter

Summary
---------------
The presently work was an academic thesis, about how to make topic categorization and sentiment analysis of tweets in Python, using algorithms of Text Mining and Natural Language Processing (NLP) with Apache Spark. Adittionally a web application in Django was developt to display a several of graphics indicators like: a wordcloud and other interesting graphics.

Authors:
---------------
- Manuel Araujo
- Manuel Carrero

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

Fill in with your own PostgreSQL credentials. By default, DB_HOST and DB_PORT in PostgreSQL are localhost/5432.

Generate default data with the fixtures:

	python3 fixtures_load.py

Default credentials for admin superuser are: admin@admin.com / admin. Then run the migrations:

	python manage.py makemigrations

	python manage.py migrate

Run the server:

	python manage.py runserver

You could see the home page in:

	http://127.0.0.1:8000/

## Swagger Documentation

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a tool for API documentation. "Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption."

## Contributions
------------------------

All work to improve performance is good

Enjoy it!
