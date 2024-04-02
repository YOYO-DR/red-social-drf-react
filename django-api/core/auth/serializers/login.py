from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from core.user.serializers import UserSerializer

class LoginSerializer(TokenObtainPairSerializer):
  
  def validate(self, attrs):
    data = super().validate(attrs) # llamo la funcion de la clase base, y obtengo los token de refresco y de acceso
    refresh = self.get_token(self.user) # obtengo el token de refresco también
    data['user'] = UserSerializer(self.user).data # obtengo los datos del usuario creando una instancia del serializer de usuario
    data['refresh'] = str(refresh) # convierto el token de refresco a string
    data['access'] = str(refresh.access_token) # convierto el token de acceso a string
    if api_settings.UPDATE_LAST_LOGIN: # si la configuración de la API es que se actualice el último inicio de sesión
      update_last_login(None, self.user) # actualizo el último inicio de sesión
    return data # devuelvo los datos