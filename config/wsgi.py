"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from config.settings.base import BASE_DIR
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
load = load_dotenv(os.path.join(BASE_DIR, '.env'))

# Variable environment local or production
ENV = os.environ.get('ENV', 'development')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod' if ENV == 'production' else 'config.settings.dev')

application = get_wsgi_application()
