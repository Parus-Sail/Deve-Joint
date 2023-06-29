#!/bin/sh
echo "Run entrypoint.sh"
python3 manage.py makemigrations
python3 manage.py migrate
exec "$@"