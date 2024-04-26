from django.db import models
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractManager(models.Manager):
    # AbstractManager: es el administrador de modelos que se utilizará para interactuar con la base de datos, en este caso creamos un método para obtener un objeto por su public_id, y como varios modelos tendran la misma funcion, lo creamos en un solo lugar para no repetir codigo

    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id, is_deleted=False)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404("Object does not exist")


class AbstractModel(
    models.Model
):  # AbstractModel: es una clase abstracta que hereda de models.Model, y se utiliza para definir campos comunes a todos los modelos, como public_id, created y updated
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(
        default=False
    )  # para no eliminar los registros de la base de datos, sino marcarlos como eliminados
    objects = AbstractManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True  # Meta: es una clase interna de la clase AbstractModel, y se utiliza para definir metadatos de la clase, en este caso, abstract=True indica que la clase es abstracta y no se creará una tabla en la base de datos para ella
