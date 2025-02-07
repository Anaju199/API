from rest_framework import serializers
from ch.models import UsuarioCasaRohr
from ch.models import Fotos, Catalogos

class UsuarioCasaRohrSerializer(serializers.ModelSerializer):
   class Meta:
      model = UsuarioCasaRohr
      fields = ('id','nome','cpf','email','senha')


class FotosSerializer(serializers.ModelSerializer):
    class Meta:
      model = Fotos
      fields = ('id', 'categoria','foto', 'descricao')


class CatalogosSerializer(serializers.ModelSerializer):
    class Meta:
      model = Catalogos
      fields = ('id', 'descricao', 'arquivo')
