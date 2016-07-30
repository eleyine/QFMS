#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:`pwd`"
echo "Python path: ${PYTHONPATH}"
export DJANGO_SETTINGS_MODULE=smf_website.settings
echo "Django settings module: ${DJANGO_SETTINGS_MODULE}"
echo $PATH

echo "Make messages in root dir `pwd`"
pwd
django-admin makemessages -x js -l fr --settings=smf_website.settings
cd registration
mkdir -p locale

echo "Make messages in registration dir `pwd`"
django-admin makemessages -x js -l fr --settings=smf_website.settings

cd ../static/javascripts
echo "Make messages in dir `pwd`"
django-admin makemessages -d djangojs -l fr --settings=smf_website.settings

cd ../..
echo "Compile messages in dir `pwd`"
django-admin compilemessages --settings=smf_website.settings
python manage.py runserver