#!/bin/bash
# shellcheck disable=SC1091

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py makemigrations main
python manage.py migrate