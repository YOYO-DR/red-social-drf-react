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


@pytest.fixture
def user(db) -> User:
  return User.objects.create_user(**data_user)
