# 05-DocPdf-Converter

To set up project set your virtual env use commands in this order (Bash):
1. source venv/Scripts/activate
2. python manage.py migrate
3. python manage.py makemigrations
4. python manage.py runserver

You also can add server runner to your configs,
to do that follow this steps (PyCharm):
1. Open configurations editor
2. Add new configuration
3. Python
4. Name it as you want
5. Set script path (Path to manage.py)
6. Set parameters: "runserver"
7. Make sure that here is configured your environment