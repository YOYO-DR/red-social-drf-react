import pytest
from dotenv import load_dotenv
from rest_framework.test import APIClient

load_dotenv("./.env") # carga las variables de entorno del archivo .env

@pytest.fixture
def client(): # fixture que retorna un cliente de la API, se puede usar en cualquier test, para poder hacer peticiones a la API
  return APIClient()