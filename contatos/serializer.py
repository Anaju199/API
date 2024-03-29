from rest_framework import serializers
from contatos.models import Contato, Pensamento

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
      model = Contato
      fields = ('id', 'nome', 'data_nascimento', 'telefone', 'telefone_check', 'email', 'email_check', 'mensagem')

class PensamentoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Pensamento
      fields = ('id','conteudo','autoria','modelo','favorito')
