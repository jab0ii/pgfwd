web: gunicorn pageitforward.wsgi --log-file - --access-logfile -
worker: celery worker -A events.eventProcessor
