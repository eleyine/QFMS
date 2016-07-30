#!/bin/bash

echo Present working directory: `pwd` 
rm -rf */migrations/*
rm */dev-db.sqlite3
python manage.py makemigrations
python manage.py makemigrations event registration
python manage.py migrate
# python manage.py dummydata --reset
./scripts/createsuperuser.sh
