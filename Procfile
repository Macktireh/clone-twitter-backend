release: python manage.py migrate && python manage.py collectstatic --no-input
web: daphne -b 0.0.0.0 -p $PORT config.asgi:application