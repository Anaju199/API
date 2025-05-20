from rest_framework import serializers
from ch.models import UsuarioCasaRohr
from ch.models import Categorias, Fotos, Catalogos

class UsuarioCasaRohrSerializer(serializers.ModelSerializer):
   class Meta:
      model = UsuarioCasaRohr
      fields = ('id','nome','cpf','email','senha')


class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
      model = Categorias
      fields = ('id', 'categoria', 'texto')

class FotosSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.ReadOnlyField(source='categoria.categoria')

    class Meta:
      model = Fotos
      fields = ('id', 'categoria', 'categoria_nome','foto', 'descricao')


class CatalogosSerializer(serializers.ModelSerializer):
    class Meta:
      model = Catalogos
      fields = ('id', 'descricao', 'arquivo')
