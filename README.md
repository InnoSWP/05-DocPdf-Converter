# Doc to PDF converter
## [Full documentation link](https://innoswp.github.io/05-DocPdf-Converter/)

## Badges
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

## Project Demo
### Main processes
https://user-images.githubusercontent.com/48485773/177003285-8a2783fe-2881-46db-98c6-2d3354836e11.mp4

### Errors
1. Attempt to convert nothing
2. Attempt to convert file(-s) with unsupported extensions

https://user-images.githubusercontent.com/48485773/177003334-a7ef6312-442d-4043-9d92-1bd7f6389713.mp4

## Project Installation
1. Clone the project
2. Open project directory in console
3. Make the scripts' executables:

**`chmod +x runserver.sh build.sh first-run.sh`**

### To run project first time with bash script (with installing dependencies)
**`source ./first-run.sh`**

### To install dependencies with bash script
**`source ./build.sh`**

### To run server without installing dependencies
**`source ./runserver.sh`**


### To set up the project, set your virtual env using the commands in this order (Ubuntu)
1. `sudo apt install python3`
2. `sudo apt install python3-venv`
3. `sudo -S apt -y update && sudo -S apt -y install libreoffice`
4. `python3 -m venv venv`
5. `source venv/bin/activate`
6. `pip install -r requirements.txt`
7. `python3 manage.py makemigrations`
8. `python3 manage.py makemigrations main`
9. `python3 manage.py migrate`
10. `python3 manage.py migrate`
*One command format:*
**`sudo apt install python3 && sudo apt install python3-venv && sudo -S apt -y update && sudo -S apt -y install libreoffice && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 manage.py makemigrations && python3 manage.py makemigrations main && python3 manage.py migrate && python3 manage.py runserver`**

### To set up the project, set your virtual env using the commands in this order (Bash)
1. `source venv/Scripts/activate`
2. `python manage.py makemigrations`
3. `python manage.py makemigrations main`
4. `python manage.py migrate`
5. `python manage.py runserver`

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
4. Depending on the amount of chosen files, you will receive a single-converted file (if you chose one file) or an archive of converted files otherwise.

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

## Description of requests
Please, pay attention to the fact the under `correct file(s)` in `Body param name` we assume all the files with the correct extension:
- .doc
- .docx
- .xls
- .xlsx
- .PDF

To see example requests on Postman, you should firstly accept the [invitation](https://app.getpostman.com/join-team?invite_code=e055fc0195cb7f0bd9fa89b71e7cfc4d&target_code=3e27288b270844aa4aa3c6570f31750b)

| URL                                                            | Request type | Body param name | Param value                              | Response code | Response content                                                               | Example                                                                                                                                                                             |
| :------------------------------------------------------------: | :----------: | :-------------: | :--------------------------------------: | :-----------: | :----------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| http://127.0.0.1:8000/convert                                  | POST         | `files`         | single correct file                      | 200           | single `.pdf` file                                                             | [Postman](https://lunar-crescent-398747.postman.co/workspace/DocToPdf-Team5-Workspace~f3018eb9-558e-49ae-8204-433ad59feae4/example/17330906-3252e40e-d287-48c5-be4d-82e9e79d7551)   |
| http://127.0.0.1:8000/convert                                  | POST         | `files`         | multiple correct files                   | 200           | multiple `.pdf` file                                                           | [Postman](https://lunar-crescent-398747.postman.co/workspace/DocToPdf-Team5-Workspace~f3018eb9-558e-49ae-8204-433ad59feae4/example/17330906-470e8e45-d14d-4982-a20c-69f4ff5d700d)   |
| http://127.0.0.1:8000/convert                                  | POST         | `files`         | null                                     | 400           | { "error": "invalid_files", "error_description": "Files field is empty."}      | [Postman](https://lunar-crescent-398747.postman.co/workspace/DocToPdf-Team5-Workspace~f3018eb9-558e-49ae-8204-433ad59feae4/example/17330906-16d2e64e-2255-4820-8f31-1b05e0d650e8)   |
| http://127.0.0.1:8000/convert                                  | POST         | `files`         | empty file                               | 400           | { "error": "empty_file", "error_description": "Empty file in your request."}   | [Postman](https://lunar-crescent-398747.postman.co/workspace/DocToPdf-Team5-Workspace~f3018eb9-558e-49ae-8204-433ad59feae4/example/17330906-836487d6-8e23-4f86-9f6d-9b2ea33d593c)   |
