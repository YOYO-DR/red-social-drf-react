from rest_framework import status
from core.fixtures.user import user,user2
from core.fixtures.post import post


class TestPostViewSet:
  endpoint = '/api/post/'

  # probar el listado
  def test_list(self, client, user, post):
    # para que el cliente este autenticado
    client.force_authenticate(user=user)
    response = client.get(self.endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1

  # probar obtener un post
  def test_retrieve(self, client, user, post):
    # para que el cliente este autenticado
    client.force_authenticate(user=user)
    response = client.get(self.endpoint + str(post.public_id) + "/")
    assert response.status_code == status.HTTP_200_OK
    # hex es el valor hexadecimal del public_id, para poder comparar con el public_id del post que retorna la API
    assert response.data['id'] == post.public_id.hex
    assert response.data['body'] == post.body
    assert response.data['author']['id'] == post.author.public_id.hex

  # probar crear un post
  def test_create(self, client, user):
    client.force_authenticate(user=user)
    data = {
        "body": "Test Post Body",
        "author": user.public_id.hex
    }
    response = client.post(self.endpoint, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['body'] == data['body']
    assert response.data['author']['id'] == user.public_id.hex

  def test_update(self, client, user, post):
    client.force_authenticate(user=user)
    data = {
        "body": "Test Post Body Edit",
        "author": user.public_id.hex
    }
    response = client.put(self.endpoint + post.public_id.hex + "/", data)
    assert response.status_code == status.HTTP_200_OK

    assert response.data['body'] == data['body']

  def test_delete(self, client, user, post):
    client.force_authenticate(user=user)
    response = client.delete(self.endpoint + post.public_id.hex + "/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

  # probar el listado y obtener un post sin autenticacion
  def test_list_anonymous(self, client, post):
    response = client.get(self.endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1

  # probar obtener un post sin autenticacion
  def test_retrieve_anonymous(self, client, post):
    response = client.get(self.endpoint + post.public_id.hex + "/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == post.public_id.hex
    assert response.data['body'] == post.body
    assert response.data['author']['id'] == post.author.public_id.hex

  # probar crear un post sin autenticacion
  def test_create_anonymous(self, client):
    data = {
        "body": "Test Post Body",
        "author": "test_user"
    }
    response = client.post(self.endpoint, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  # probar actualizar un post sin autenticacion
  def test_update_anonymous(self, client, post):
    data = {
        "body": "Test Post Body",
        "author": "test_user"
    }
    response = client.put(self.endpoint + post.public_id.hex + "/", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  # probar eliminar un post sin autenticacion
  def test_delete_anonymous(self, client, post):
    response = client.delete(self.endpoint + post.public_id.hex + "/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  # probar eliminar un post con un usuario diferente
  def test_delete_different_user(self, client, user2, post):
    client.force_authenticate(user=user2)
    response = client.delete(self.endpoint + post.public_id.hex + "/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
  
  # probar actualizar un post con un usuario diferente
  def test_update_different_user(self, client, user2, post):
    client.force_authenticate(user=user2)
    data = {
        "body": "Test Post Body",
        "author": user2.public_id.hex,
        "post": post.public_id.hex
    }
    response = client.put(self.endpoint + post.public_id.hex + "/", data)
    assert response.status_code == status.HTTP_403_FORBIDDEN