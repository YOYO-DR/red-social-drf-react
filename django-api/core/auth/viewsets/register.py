from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.auth.serializers import RegisterSerializer


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )  # creo una instancia del serializer con los datos de la request
        serializer.is_valid(
            raise_exception=True
        )  # raise_exception=True para que si no es valido, devuelva un error
        user = serializer.save()  # guardo el usuario
        refresh = RefreshToken.for_user(user)  # creo un token de refresco
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            {  # devuelvo el usuario, el token de refresco y el token de acceso
                "user": serializer.data,
                "refresh": res["refresh"],
                "token": res["access"],
            },
            status=status.HTTP_201_CREATED,
        )
