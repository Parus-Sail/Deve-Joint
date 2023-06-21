#!/bin/sh
echo "Run entrypoint.sh" >&2
python3 manage.py migrate
exec "$@"