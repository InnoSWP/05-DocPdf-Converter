# Doc to PDF converter
## [Full documentation link](https://innoswp.github.io/05-DocPdf-Converter/)

## Badges
[![Build](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/build.yml/badge.svg)](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/build.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)

## Project Installation
### To set up project set your virtual env use commands in this order (Bash)
1. source venv/Scripts/activate
2. python manage.py migrate
3. python manage.py makemigrations
4. python manage.py runserver

### You also can add server runner to your configs, to do that follow this steps (PyCharm)
1. Open configurations editor
2. Add new configuration
3. Python
4. Name it as you want
5. Set script path (Path to manage.py)
6. Set parameters: "runserver"
7. Make sure that here is configured your environment

* After running the local server go on 127.0.0.1 and click on link right next "converter" in the opened window.
* The main page will be opened. There you will see two buttons: "Choose files" and "Convert".
* You can choose files on your machine and after that convert them by clicking same-called buttons.
* Depends on the amount of choosed files you will receive single-converted file(if you choosed one file) or arcive of files otherwise.

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
### Crossplatform
DocPdf converter has two different modules that allow efficient convertation on both Linux- and Windows-based servers. The system identifies the platform it runs on, and, depending on the result, executes corresponding module...
