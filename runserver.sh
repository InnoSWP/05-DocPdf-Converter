#!/bin/bash
case "$OSTYPE" in
  linux*) sudo apt install python3 && sudo apt install python3-venv && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 manage.py migrate && python3 manage.py makemigrations && python3 manage.py makemigrations main && python3 manage.py runserver;;
  msys*) sh ./windows.sh;;
  cygwin*) sh ./windows.sh;;
  *)        echo "unknown: $OSTYPE" ;;
esac