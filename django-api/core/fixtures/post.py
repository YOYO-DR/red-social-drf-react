import pytest
from core.fixtures.user import user # aunque no la llame en el codigo, el la utiliza asi que si es necesario importarla
from core.post.models import Post

@pytest.fixture
def post(db, user): # un fixture que depende de otro fixture
  return Post.objects.create(author=user,
  body="Test Post Body")