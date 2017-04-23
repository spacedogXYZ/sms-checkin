web: gunicorn sms_checkin.wsgi:application --log-file -
worker: celery -A sms_checkin.settings worker -l info