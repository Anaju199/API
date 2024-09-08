from rest_framework import serializers
from tb.models import Contato, Cliente, Usuario, Item, Pedido, Endereco

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
      model = Contato
      fields = ('id', 'nome', 'data_nascimento', 'celular', 'telefone_retorno', 'email', 'email_retorno', 'mensagem')

class ClienteSerializer(serializers.ModelSerializer):
   class Meta:
      model = Cliente
      fields = ('id','nome','link','foto','data_inicio','data_prevista','data_fim','valorDominio','valorSite','valorMensal','observacoes')

class UsuarioSerializer(serializers.ModelSerializer):
   class Meta:
      model = Usuario
      fields = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha')

class ItemSerializer(serializers.ModelSerializer):
   # Adicione um campo de leitura para mostrar o nome do usuario
   usuario_nome = serializers.ReadOnlyField(source='usuario.nome')

   class Meta:
      model = Item
      fields = ('id','usuario','usuario_nome','item','valor_pdt','numero_pgt')

class PedidoSerializer(serializers.ModelSerializer):
   # Adicione um campo de leitura para mostrar o nome do usuario
   usuario_nome = serializers.ReadOnlyField(source='usuario.nome')

   class Meta:
      model = Pedido
      fields = ('id','usuario','usuario_nome','itens','valor_pgt','data_pgt', 'link_pgt')

class EnderecoSerializer(serializers.ModelSerializer):
   # Adicione um campo de leitura para mostrar o nome do usuario
   usuario_nome = serializers.ReadOnlyField(source='usuario.nome')

   class Meta:
      model = Endereco
      fields = ('id','usuario','usuario_nome','rua','numero','complemento','bairro','cidade','estado','pais','cep','principal')
