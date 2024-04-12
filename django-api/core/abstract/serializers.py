from rest_framework import serializers

class AbstractSerializer(serializers.ModelSerializer):
  id = serializers.UUIDField(source='public_id', # el source es el campo del modelo que se utilizara para serializar, en este caso public_id
  read_only=True, format='hex')
  created = serializers.DateTimeField(read_only=True)
  updated = serializers.DateTimeField(read_only=True)