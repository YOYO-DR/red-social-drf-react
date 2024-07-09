import pytest
from core.fixtures.user import user # aunque no la llame en el codigo, el la utiliza asi que si es necesario importarla
from core.post.models import Post

@pytest.mark.django_db
def test_create_post(user): # user es un fixture que se encuentra en core/fixtures/user.py
  post = Post.objects.create(author=user,
  body="Test Post Body")
  
  assert post.body == "Test Post Body"
  assert post.author == user