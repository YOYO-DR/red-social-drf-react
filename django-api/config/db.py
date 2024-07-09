import os
from config.settings import BASE_DIR

DataBasesConfig = {
  "a": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DBPOSNAME"),
    "USER": os.getenv("DBPOSUSER"),
    "PASSWORD": os.getenv("DBPOSPASS"),
    "HOST": os.getenv("DBPOSHOST"),
    "PORT": os.getenv("DBPOSPORT"),
  },
  "postgres_local": {
      "ENGINE": "django.db.backends.postgresql",
      "NAME": "django_react_libro",
      "USER": "postgres",
      "PASSWORD": "root",
      "HOST": "localhost",
      "PORT": "5432",
    },
  "default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
  },
}
