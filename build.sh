#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations chatbot --no-input
python manage.py migrate --no-input
python manage.py seed_data
