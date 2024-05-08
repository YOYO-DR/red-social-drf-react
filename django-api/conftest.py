import pytest

from rest_framework.test import APIClient

@pytest.fixture
def client(): # fixture que retorna un cliente de la API, se puede usar en cualquier test, para poder hacer peticiones a la API
  return APIClient()