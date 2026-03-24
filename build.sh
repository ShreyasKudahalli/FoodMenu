#!/usr/bin/env bash

rm -rf staticfiles
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate