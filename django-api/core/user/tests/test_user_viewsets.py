from rest_framework import status
from core.fixtures.user import user
from core.fixtures.post import post


class TestUserViewSet:
  endpoint = '/api/user/'
  auth_endpoint = '/api/auth/'

  def test_list(self, client, user):
    client.force_authenticate(user=user)
    response = client.get(self.endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1

  def test_retrieve(self, client, user):
    client.force_authenticate(user=user)
    response = client.get(self.endpoint + user.public_id.hex + "/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == user.public_id.hex
    assert response.data['username'] == user.username
    assert response.data['email'] == user.email

  def test_create(self, client, user):
    client.force_authenticate(user=user)
    data = {}  # no envio nada porque la vista no tiene un metodo post para crear usuario
    response = client.post(self.endpoint, data)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

  def test_update(self, client, user):
    client.force_authenticate(user=user)
    data_user = {
        "username": "test_user_update",
    }
    response = client.patch(self.endpoint + user.public_id.hex + "/", data_user) # recordar que con el patch no se ncesita enviar todos los campos, eso es el put
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == data_user["username"]
