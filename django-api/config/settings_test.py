from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django_react_libro",
        "USER": "postgres",
        "PASSWORD": "root",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
