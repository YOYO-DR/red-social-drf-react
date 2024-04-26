from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from core.auth.permissions import UserPermission


class PostViewSet(AbstractViewSet):
    # post crear, get obtener, put actualizar, delete eliminar
    http_method_names = ("post", "get", "put", "delete")
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer  # utilizo el serializer PostSerializer

    def get_queryset(self):
        # obtengo los objetos que no han sido eliminados
        return Post.objects.filter(is_deleted=False)

    def get_object(self):
        obj = (
            Post.objects.get_object_by_public_id(  # obtengo el objeto por su public_id
                self.kwargs["pk"]
            )
        )
        # verifico que el usuario tenga permisos para acceder a este objeto
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        # creo una instancia del serializer con los datos de la request
        serializer = self.get_serializer(data=request.data)
        # raise_exception=True para que si no es valido, devuelva un error
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # el detail=True es para que se aplique a un objeto en particular
    @action(methods=["post"], detail=True)
    # en detail=False se aplica a la lista de objetos
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        user.like(post)
        serializer = self.serializer_class(
            post, context={"request": request}
        )  # le paso el request al serializer
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        user.remove_like(post)
        serializer = self.serializer_class(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
