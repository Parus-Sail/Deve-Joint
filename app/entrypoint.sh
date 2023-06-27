#!/bin/sh
echo "Run entrypoint.sh"
python3 manage.py makemigrations MainPageApp
python3 manage.py migrate MainPageApp
exec "$@"