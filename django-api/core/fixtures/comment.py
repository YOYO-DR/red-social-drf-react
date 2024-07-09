import pytest
from core.fixtures.user import user
from core.fixtures.post import post
from core.comment.models import Comment

@pytest.fixture
def comment(db, user, post):
  return Comment.objects.create(author=user, post=post,
                                body="Test Comment Body")

@pytest.fixture
def comment2(db, user2, post): # comentario al mismo post pero con otro usuario
  return Comment.objects.create(author=user2, post=post,
                                body="Test Comment Body 2")
