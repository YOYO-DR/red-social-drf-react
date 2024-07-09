import pytest
from core.user.models import User

# los fixtures o accesorios son datos que se pueden reutilizar en diferentes pruebas, cuando ellas las necesiten
data_user = {
  "username": "test_user",
  "email": "test@gmail.com",
  "first_name": "Test",
  "last_name": "User",
  "password": "test_password"
}

# usuario diferencte al anterior
data_user2 = {
  "username": "test_user2",
  "email": "test2@gmil.com",
  "first_name": "Test2",
  "last_name": "User2",
  "password": "test_password2"
}

@pytest.fixture
def user(db) -> User:
  return User.objects.create_user(**data_user)

@pytest.fixture
def user2(db) -> User:
  return User.objects.create_user(**data_user2)