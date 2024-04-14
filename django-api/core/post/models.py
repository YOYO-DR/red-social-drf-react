from django.db import models
from core.abstract.models import AbstractModel, AbstractManager


class PostManager(
    AbstractManager
):  # por si depronto se necesita un manager personalizado, se puede sobreescribir los metodos de la clase padre, en este caso AbstractManager
    pass


class Post(AbstractModel):
    author = models.ForeignKey(
        to="core_user.User",  # con to le digo el modelo, puedo poner la ruta del modelo como importacio o solo el label de la app y su modelo
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    edited = models.BooleanField(default=False)
    objects = PostManager()

    def __str__(self):
        return f"{self.author.name}"
