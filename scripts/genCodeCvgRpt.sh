#!/bin/bash
# Author: Noah Gold
foreman run worker &
foreman run coverage run --source='.' --omit=venv/*,*test*,*migrations*,*__init__*,*settings*,manage*,pageitforward/urls*,pageitforward/wsgi*,*admin* manage.py test --pattern="tests*.py"
coverage html -d codeCoverage
pkill -INT -P $!
kill -9 $!
