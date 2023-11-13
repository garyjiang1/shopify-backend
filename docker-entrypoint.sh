#!/bin/sh

flask db init
flask db migrate
flask db upgrade

cd /usr/src/app
python wsgi.py