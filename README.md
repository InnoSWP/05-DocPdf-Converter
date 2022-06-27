# Doc to PDF converter
## [Full documentation link](https://innoswp.github.io/05-DocPdf-Converter/)

## Badges
[![Build](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/build.yml/badge.svg)](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/build.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)

## Project Installation
### To set up the project, set your virtual env using the commands in this order (Ubuntu)
1. sudo apt install python3
2. sudo apt install python3-venv
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. python3 manage.py migrate
7. python manage.py makemigrations
8. python manage.py makemigrations main
9. python3 manage.py migrate
  
### To set up the project, set your virtual env using the commands in this order (Bash)
1. source venv/Scripts/activate
2. python manage.py migrate
3. python manage.py makemigrations
4. python manage.py makemigrations main
5. python3 manage.py migrate
6. python manage.py runserver

### You can also add server runner to your configs. To that, follow this steps (PyCharm)
1. Open configurations editor
2. Add new configuration
3. Python
4. Name it as you want
5. Set script path (Path to manage.py)
6. Set parameters: "runserver"
7. Make sure that here is configured your environment

* After running the local server, go on 127.0.0.1 and click on the link right next the "converter" in the opened window.
* The main page will be opened. There you will see two buttons: "Choose files" and "Convert".
* You can choose files on your machine, and after that convert them by clicking the same-called button.
* Depending on the amount of chosen files, you will receive a single-converted file (if you have chosen one file) or an archive of files otherwise.

## Framework and technology
### Frontend
- HTML
- CSS
- JavaScript
- JQuery

### Backend
- Python
  - Django
  - Django Rest Framework
  - Sphinx
  - docx2pdf

## Features
### Cross-platform
DocPdf converter has two different modules that allow efficient conversion on both Linux and Windows-based servers. 
The system identifies the platform it runs on, and, depending on the result, executes corresponding module.
