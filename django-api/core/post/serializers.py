from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer

class PostSerializer(AbstractSerializer):
  # utilizo el SlugRelatedField para que en vez de mandar todo el usuario serializado, solo mande el campo public_id, por eso no utilizo
  author = serializers.SlugRelatedField(
  queryset=User.objects.all(), # para especificar la relacion y decirle donde buscar, con el campo dicho en el slug_field
  slug_field='public_id') # con el slug_field le digo que campo se le enviara en respuesta al cliente, en vez de mandar todo el usuario serializado

  def validate_author(self, value): # valido que el usuario que esta creando el post sea el mismo que esta logueado
    if self.context["request"].user != value:
      raise ValidationError("You can't create a post for another user.")
    return value
  
  def to_representation(self, instance): # sobreescribo el metodo to_representation para que me devuelva el usuario serializado, por si quiero modificar o agregar campos en la respuesta o serializacion
    rep = super().to_representation(instance) # obtengo la representacion del objeto
    author = User.objects.get_object_by_public_id(
    rep["author"]) # obtengo el usuario por su public_id
    rep["author"] = UserSerializer(author).data # serializo el usuario
    return rep # retorno la representacion
  
  def update(self, instance, validated_data): # sobreescribo el metodo update para que si no se ha editado, lo edite
    if not instance.edited: # pregunto si no se ha editado, si no se ha editado, pongo edited en True ya que se va a editar
      validated_data['edited'] = True
    instance = super().update(instance, validated_data) # actualizo el objeto
    return instance
  # se hace la peticion, maandando el public_id del post en la URL /api/post/c7578998689f4db8bdc11361c87f75b3/, y en el cuerpo, el author con su public_id, y la modificacion en el body

  class Meta:
    model = Post
    # List of all the fields that can be included in a
    # request or a response
    fields = ['id', 'author', 'body', 'edited',
 'created', 'updated']
    read_only_fields = ["edited"]