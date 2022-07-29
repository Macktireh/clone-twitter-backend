import os

from .base import *


TYPE_DATABASE = os.environ.get('TYPE_DATABASE', 'sqlite3')

# Database
if TYPE_DATABASE != 'sqlite3':
    DATABASES = {
        f'{TYPE_DATABASE}': {
            'ENGINE': os.environ.get("ENGINE"),
            'NAME': os.environ.get("DB"),
            'USER': os.environ.get("USERNAME"),
            'PASSWORD': os.environ.get("PASSWORD"),
            'HOST': os.environ.get("HOST"),
            'PORT': os.environ.get("PORT"),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }