release: python manage.py migrate && python manage.py collectstatic
web: daphne -b 0.0.0.0 -p $PORT config.asgi:application