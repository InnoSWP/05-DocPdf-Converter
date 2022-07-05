=======================
Quick start instuctions
=======================

**To set up the project, set your virtual env using the commands in this order (Bash):**
----------------------------------------------------------------------------------------
1. `source venv/Scripts/activate`
2. `python manage.py makemigrations`
3. `python manage.py makemigrations main`
4. `python manage.py migrate`
5. `python manage.py runserver`

**To set up the project, set your virtual env using the commands in this order (Ubuntu):**
------------------------------------------------------------------------------------------
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
---------------------
**`sudo apt install python3 && sudo apt install python3-venv && sudo -S apt -y update && sudo -S apt -y install libreoffice && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 manage.py makemigrations && python3 manage.py makemigrations main && python3 manage.py migrate && python3 manage.py runserver`**

You also can add server runner to your configs, to do that follow this steps (PyCharm):
---------------------------------------------------------------------------------------
1. Open configurations editor
2. Add new configuration
3. Python
4. Name it as you want
5. Set script path (Path to manage.py)
6. Set parameters: "runserver"
7. Make sure that here is configured your environment