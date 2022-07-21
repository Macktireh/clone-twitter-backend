import os
import dj_database_url
import django_heroku

from .base import *


# Database
# DATABASES = {
#     'PostgreSQL': {
#         'ENGINE': os.environ.get("ENGINE"),
#         'NAME': os.environ.get("POSTGRES_DB"),
#         'USER': os.environ.get("POSTGRES_USER"),
#         'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
#         'HOST': os.environ.get("POSTGRES_HOST"),
#         'PORT': os.environ.get("POSTGRES_PORT"),
#     },
# }

DATABASES = {
    'default': dj_database_url.config()
}

# Configure Django App for Heroku.
django_heroku.settings(locals(), test_runner=False)