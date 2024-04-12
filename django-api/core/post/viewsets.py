from rest_framework.permissions import IsAuthenticated
from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import BasePermission, SAFE_METHODS,AllowAny

class UserPermission(BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.user.is_anonymous:
      return request.method in SAFE_METHODS # si el usuario es anonimo, solo permito los metodos seguros (GET, HEAD, OPTIONS)
    
    if view.basename in ["post"]: # si el viewset es de post
      return bool(request.user and # solo permito que el usuario autenticado pueda acceder a este objeto
      request.user.is_authenticated)
    return False
  
  def has_permission(self, request, view): # verifico si el usuario tiene permisos para acceder a esta vista
    if view.basename in ["post"]: # si el viewset es de post
      if request.user.is_anonymous: # si el usuario es anonimo, solo permito los metodos seguros (GET, HEAD, OPTIONS)
        return request.method in SAFE_METHODS
      return bool(request.user and # solo permito que el usuario autenticado pueda acceder a esta vista
        request.user.is_authenticated)
    return False

class PostViewSet(AbstractViewSet):
  # post crear, get obtener, put actualizar, delete eliminar
  http_method_names = ('post', 'get', 'put', 'delete')
  permission_classes = (UserPermission,)
  serializer_class = PostSerializer # utilizo el serializer PostSerializer
  
  def get_queryset(self): 
    return Post.objects.all()

  def get_object(self):
    obj = Post.objects.get_object_by_public_id( # obtengo el objeto por su public_id
    self.kwargs['pk'])
    self.check_object_permissions(self.request, obj) # verifico que el usuario tenga permisos para acceder a este objeto
    return obj
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data) # creo una instancia del serializer con los datos de la request
    serializer.is_valid(raise_exception=True) # raise_exception=True para que si no es valido, devuelva un error
    self.perform_create(serializer) 
    return Response(serializer.data,
    status=status.HTTP_201_CREATED)