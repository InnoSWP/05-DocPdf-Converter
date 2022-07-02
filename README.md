# Doc to PDF converter
## [Full documentation link](https://innoswp.github.io/05-DocPdf-Converter/)

# Badges
### Linter
[![Build](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/build.yml/badge.svg)](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/build.yml)
### Unit tests Django
[![Django CI](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/django.yml/badge.svg)](https://github.com/InnoSWP/05-DocPdf-Converter/actions/workflows/django.yml)
### Sonar cloud
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=coverage)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=bugs)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_05-DocPdf-Converter&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=InnoSWP_05-DocPdf-Converter)

## Project Description
### This is the project with user-friendly and simple interface that perform converting files with .doc/.docx extention to PDF on local Windows/Linux server
* Each of the algorithms (both for Windows and Linux) uses the built-in functions of programs-viewers (such as [**Microsoft Word**](https://en.wikipedia.org/wiki/Microsoft_Word) for Windows and [**LibreOffice Writer**](https://en.wikipedia.org/wiki/LibreOffice_Writer) for Linux) to convert files with .doc/.docx extension to PDFs with minimum errors of conversion.
* All files after the conversion are returned in archive with PDFs (if there are more than one file) or as a single PDF file otherwise.
* In case if the user will choose file(-s) with ".pdf" extension, then the program will send them back **=)**.

## Project Installation

### Easiest universal way is to run:
**`./runserver.sh`**

### To set up the project, set your virtual env using the commands in this order (Ubuntu)
1. `sudo apt install python3`
2. `sudo apt install python3-venv`
3. `sudo -S apt -y update && sudo -S apt -y install libreoffice`
4. `python3 -m venv venv`
5. `source venv/bin/activate`
6. `pip install -r requirements.txt`
7. `python3 manage.py migrate`
8. `python3 manage.py makemigrations`
9. `python3 manage.py makemigrations main`
10. `python3 manage.py migrate`

*One command format:*
**`sudo apt install python3 && sudo apt install python3-venv && sudo -S apt -y update && sudo -S apt -y install libreoffice && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 manage.py migrate && python3 manage.py makemigrations && python3 manage.py makemigrations main && python3 manage.py runserver`**

### To set up the project, set your virtual env using the commands in this order (Bash)
1. `source venv/Scripts/activate`
2. `python manage.py migrate`
3. `python manage.py makemigrations`
4. `python manage.py makemigrations main`
5. `python manage.py migrate`
6. `python manage.py runserver`

### You can also add server runner to your configs. To that, follow this steps (PyCharm)
1. Open configurations editor
2. Add new configuration
3. Python
4. Name it as you want
5. Set script path (Path to manage.py)
6. Set parameters: "runserver"
7. Make sure that here is configured your environment

### After running the local server
1. Go on the generated [**link**](http://127.0.0.1:8000/convert).
2. The main page will be opened. There you will see two buttons: "Choose files" and "Convert".
3. You can choose files on your machine and after that convert them by clicking the same-called buttons.
4. Depending on the amount of choosed files, you will receive a single-converted file (if you choosed one file) or an archive of converted files otherwise.

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
