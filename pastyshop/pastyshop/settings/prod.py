import os
from .base import *

DEBUG = False

ADMINS = [
    ("Ihor V", "ihorvoitiukk@gmail.com"),
]

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost"
]

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': "5432",
    }
}

REDIS_URL = 'redis://redis:6379'
