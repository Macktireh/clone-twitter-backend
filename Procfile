release: python manage.py migrate && python manage.py collectstatic
web: gunicorn config.wsgi --log-file -