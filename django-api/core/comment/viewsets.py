from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status
from core.abstract.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.auth.permissions import UserPermission

class CommentViewSet(AbstractViewSet):
  http_method_names = ('post', 'get', 'put', 'delete')
  permission_classes = (UserPermission,)
  serializer_class = CommentSerializer

  def get_object(self):
    obj = Comment.objects.get_object_by_public_id(self.kwargs['pk']) # este pk es el pk del comentario
    self.check_object_permissions(self.request,obj)
    return obj

  def get_queryset(self):
    if self.request.user.is_superuser:
      return Comment.objects.all()
    post_pk = self.kwargs['post_pk']
    if post_pk is None:
      return Http404
    queryset = Comment.objects.filter(post__public_id=post_pk, post__is_deleted=False)
    return queryset
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
    # en la peticion, aunque en la url este el public_id, en la peticion debe ir el campo post con el mismo valor
    # url: /api/post/95e9ea8a11d84aafbc916ae554c039ce/comment/
    # {"post":"95e9ea8a11d84aafbc916ae554c039ce",
    #"author":"e785e133864e4b6484408fc7d86b9db3",
    #"body":"Oye, mi publicación es una vrga"}