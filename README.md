socialjusticebingo
==================

[![Build Status](https://circleci.com/gh/jessamynsmith/socialjusticebingo.svg?style=shield)](https://circleci.com/gh/jessamynsmith/socialjusticebingo)
[![Coverage Status](https://coveralls.io/repos/jessamynsmith/socialjusticebingo/badge.svg?branch=master)](https://coveralls.io/r/jessamynsmith/socialjusticebingo?branch=master)

The vision for this is a server of the bingo cards available on the internet for dealing with
common social justice situations.

So far, it's a clone of my underquoted app, which is:
Simple site that serves a page with a random quotation and allows searching of quotations.
Also provides a quotation API. Check out the live app:
https://socialjusticebingo.herokuapp.com/
You can inspect the API at:
https://socialjusticebingo.herokuapp.com/api/v1/

Development
-----------

Fork the project on github and git clone your fork, e.g.:

    git clone https://github.com/<username>/socialjusticebingo.git

Create a virtualenv using Python 3 and install dependencies. NOTE! You must change 'path/to/python3'
to be the actual path to python3 on your system.

    mkvirtualenv socialjusticebingo --python=/path/to/python3
    pip install -r requirements/development.txt

Use development settings:

    export DJANGO_SETTINGS_MODULE=socialjusticebingo.settings.development

Set up db:
    
    In psql:
    CREATE EXTENSION unaccent;
    ALTER FUNCTION unaccent(text) IMMUTABLE;

    python manage.py syncdb
    python manage.py migrate

Run tests and view coverage:

     coverage run manage.py test
     coverage report

Check code style:

    flake8

Run server:

    python manage.py runserver
