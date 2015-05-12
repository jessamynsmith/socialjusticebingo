#!/bin/bash

# This script will quit on the first error that is encountered.
set -e

CIRCLE=$1

DEPLOY_DATE=`date "+%FT%T%z"`
SECRET=$(openssl rand -base64 58 | tr '\n' '_')

heroku config:set --app=socialjusticebingo \
NEW_RELIC_APP_NAME='socialjusticebingo' \
ADMIN_EMAIL="socialjusticebingo@gmail.com" \
ADMIN_NAME="socialjusticebingo" \
DJANGO_SETTINGS_MODULE=socialjusticebingo.settings.production \
DJANGO_SECRET_KEY="$SECRET" \
DEPLOY_DATE="$DEPLOY_DATE" \
> /dev/null

if [ $CIRCLE ]
then
    git fetch origin --unshallow
    git push git@heroku.com:socialjusticebingo.git $CIRCLE_SHA1:refs/heads/master
else
    git push heroku master
fi

heroku run python manage.py syncdb --noinput --app=socialjusticebingo
heroku run python manage.py migrate --noinput --app=socialjusticebingo
