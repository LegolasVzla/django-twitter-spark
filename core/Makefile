VENV_NAME?=env
HOST=127.0.0.1
PORT=8000

help:
	@echo "make execute"
	@echo "	Run server."
	@echo "make setup"
	@echo "	Install packages and some default things needed in your system."
	@echo "make install"
	@echo " By setting previously a virtual env, generate db with default data and install python requirements."

execute:
	python manage.py runserver ${HOST}:${PORT}

start-spark:
	spark-class org.apache.spark.deploy.master.Master

setup:
	# Install PostgreSQL
	sudo apt-get update
	sudo apt install python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev
	# Generate log folder 
	mkdir logs
	# Generate config file for environment variables
	touch settings.ini
	# install pip
	sudo apt-get install python-pip python-dev build-essential -y
	sudo pip install --upgrade pip
	# Install java for Apache Spark, you can comment this line if you already have it
	sudo apt install openjdk-8-jdk
	# Install Zookeeper for high availability with Apache Spark
	apt-get install zookeeperd -y

install:
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate
	# load default system data
	python3 fixtures_load.py
	python3 nltk_install.py