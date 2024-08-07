from rest_framework import status
from core.fixtures.user import user,user2
from core.fixtures.post import post, post2
from core.fixtures.comment import comment,comment2


class TestCommentViewSet:
  #  El recurso de comentario está anidado debajo del recurso de publicación
  endpoint = '/api/post/'

  def test_list(self, client, user, post,comment):
    client.force_authenticate(user=user)
    response = client.get(self.endpoint + post.public_id.hex + "/comment/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1

  def test_retrieve(self, client, user, post, comment):
    client.force_authenticate(user=user)
    response = client.get(self.endpoint + post.public_id.hex +
                          "/comment/" + comment.public_id.hex + "/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == comment.public_id.hex
    assert response.data['body'] == comment.body
    assert response.data['author']['id'] == comment.author.public_id.hex

  def test_create(self, client, user, post):
    client.force_authenticate(user=user)
    data = {
        "body": "Test Comment Body",
        "author": user.public_id.hex,
        "post": post.public_id.hex
    }
    response = client.post(
      self.endpoint + post.public_id.hex + "/comment/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['body'] == data['body']
    assert response.data['author']['id'] == user.public_id.hex

  def test_update(self, client, user, post, comment):
    client.force_authenticate(user=user)
    data = {
        "body": "Test Comment Body Updated",
        "author": user.public_id.hex,
        "post": post.public_id.hex
    }
    response = client.put(self.endpoint + post.public_id.hex +
                          "/comment/" + comment.public_id.hex + "/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['body'] == data['body']

  def test_delete(self, client, user, post, comment):
    client.force_authenticate(user=user)
    response = client.delete(
      self.endpoint + post.public_id.hex + "/comment/" + comment.public_id.hex + "/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Usuario anónimos

  def test_list_anonymous(self, client, post, comment):
    response = client.get(self.endpoint + post.public_id.hex + "/comment/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1

  def test_retrieve_anonymous(self, client, post, comment):
    response = client.get(self.endpoint + post.public_id.hex + "/comment/" + comment.public_id.hex + "/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == comment.public_id.hex
    assert response.data['body'] == comment.body
    assert response.data['author']['id'] == comment.author.public_id.hex

    # Intentar editar o crear
  
  def test_create_anonymous(self, client, post):
    data = {}
    response = client.post(self.endpoint + post.public_id.hex + "/comment/", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
  def test_update_anonymous(self, client, post, comment):
    data = {}
    response = client.put(self.endpoint + post.public_id.hex + "/comment/" + comment.public_id.hex + "/", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
  def test_delete_anonymous(self, client, post, comment):
    response = client.delete(self.endpoint + post.public_id.hex + "/comment/" + comment.public_id.hex + "/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  # probando permisos de usuario segun si es el autor del comentario o el autor del post
  def test_update_author(self,client,user,post,comment):
    client.force_authenticate(user=user)
    data = {
      "body": "Test Comment Body Updated",
      "author": user.public_id.hex,
      "post": post.public_id.hex
    }
    response = client.put(self.endpoint + post.public_id.hex + "/comment/" + comment.public_id.hex + "/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['body'] == data['body']

  def test_update_comment_other_author(self,client,user,user2,post,comment2): # verificar que el autor del post, no pueda actualizar un comentario de otro usuario
    client.force_authenticate(user=user)
    data = {
      "body": "Test Comment Body Updated",
      "author": user2.public_id.hex,
      "post": post.public_id.hex
    }
    response = client.put(self.endpoint + post.public_id.hex + "/comment/" + comment2.public_id.hex + "/", data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
  
  
