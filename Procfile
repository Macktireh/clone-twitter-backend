release: python manage.py migrate && python manage.py collectstatic
web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2