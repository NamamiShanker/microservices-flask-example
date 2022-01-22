#!/bin/sh
set -o errexit
set -o nounset

poetry shell
export FLASK_APP=manage.py
export $(grep -v '^#' .flaskenv-Docker | xargs)
sleep 5s
python3 -m flask db upgrade
python3 -m celery --app manage.celery worker --loglevel INFO --detach
gunicorn -b 0.0.0.0:5000 manage:app --workers 1 --timeout 60
