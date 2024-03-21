import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

#BaseUserManager: es el administrador de modelos que se utilizará para interactuar con la base de datos

#AbstractBaseUser proporciona la funcionalidad básica para la autenticación

#PermissionsMixin agrega campos y métodos para manejar permisos

# Importa el módulo uuid para generar identificadores únicos universales (UUIDs).

class UserManager(BaseUserManager):
    def get_object_by_public_id(self, public_id): # obtener usuario por su public_id, si no existe, retorno un error 404, porque se utilizara un UUID en vez de números autoincrementales
      try:
        instance = self.get(public_id=public_id)
        return instance
      except (ObjectDoesNotExist, ValueError, TypeError):
        return Http404
    
    def create_user(self, username, email, password=None, **kwargs):
      """Create and return a `User` with an email, phone number, username and password."""
      if username is None:
          raise TypeError('Users must have a username.')
      if email is None:
          raise TypeError('User must have an email.')
      if password is None:
          raise TypeError('User must have a password.')
      
      # el nomrmalize_email pone el dominio en minusculas
      user = self.model(username=username, email=self.normalize_email(email), **kwargs)
      user.set_password(password)
      user.save(using=self._db)

      return user

    def create_superuser(self, username, email, password, **kwargs):
      """
      Create and return a `User` with superuser (admin) permissions.
      """
      if password is None:
          raise TypeError('Superusers must have a password.')
      if email is None:
          raise TypeError('Superusers must have an email.')
      if username is None:
          raise TypeError('Superusers must have an username.')

      user = self.create_user(username, email, password, **kwargs)
      user.is_superuser = True
      user.is_staff = True
      user.save(using=self._db)

      return user

class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False) #UUIDField es un campo que almacena un identificador único universal (UUID).
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    bio = models.TextField(null=True) # biografia
    avatar = models.ImageField(null=True) # imagen de perfil

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' # campo que se utilizara para el login, la cua es unico
    REQUIRED_FIELDS = ['username']

    objects = UserManager() # Asigna el administrador de modelos personalizado a la clase User.

    def __str__(self):
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"