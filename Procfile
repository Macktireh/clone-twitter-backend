release: python manage.py migrate && python manage.py collectstatic
web: daphne config.asgi:application