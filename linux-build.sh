#!/bin/bash
sudo apt install python3
sudo apt install python3-venv
sudo -S apt -y update
sudo -S apt -y install libreoffice
python3 -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py makemigrations main
python3 manage.py migrate