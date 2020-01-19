SHELL := /bin/bash
VENV_NAME?=env


help:
	@echo "make execute"
	@echo "	Run server."
	@echo "make run"
	@echo "	Install packages in your system."

prepare-env:
	virtualenv env --python=python3
	source env/bin/activate

venv:
       source .${VENV_BIN}/bin/activate; \

execute:
	python manage.py runserver

install:
	sudo apt-get update
	sudo apt install python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev
	python manage.py makemigrations
	python manage.py migrate
	python3 fixtures_load.py