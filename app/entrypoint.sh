#!/bin/sh
echo "Run entrypoint.sh"
python3 manage.py migrate
exec "$@"