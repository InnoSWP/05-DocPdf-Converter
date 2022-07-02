#!/bin/bash
sudo apt-get update
sudo apt-get -y install libreoffice python3 python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py makemigrations main
python3 manage.py migrate