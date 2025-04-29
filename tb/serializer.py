from rest_framework import serializers
from tb.models import Cliente, Usuario, Item, Pedido, Endereco, Avaliacoes, Demanda, MensagemDemanda, UsuarioCliente

# class ContatoSerializer(serializers.ModelSerializer):
#     class Meta:
#       model = Contato
#       fields = ('id', 'nome', 'data_nascimento', 'celular', 'telefone_retorno', 'email', 'email_retorno', 'mensagem')

class ClienteSerializer(serializers.ModelSerializer):
   class Meta:
      model = Cliente
      fields = ('id','nome','link','foto','data_inicio','data_prevista','data_fim','valorDominio','valorSite','valorMensal','observacoes')

class AvaliacoesSerializer(serializers.ModelSerializer):
   class Meta:
      model = Avaliacoes
      fields = ('id','nome','nota','comentario','data')

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

class UsuarioClienteSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.ReadOnlyField(source='usuario.nome')
    cliente_nome = serializers.ReadOnlyField(source='cliente.nome')

    class Meta:
        model = UsuarioCliente
        fields = ('id', 'usuario', 'usuario_nome', 'cliente', 'cliente_nome', 'data_vinculo', 'is_admin')
        read_only_fields = ['data_vinculo']

class MensagemDemandaSerializer(serializers.ModelSerializer):
    demanda_titulo = serializers.ReadOnlyField(source='demanda.titulo')

    class Meta:
        model = MensagemDemanda
        fields = ('id', 'demanda', 'demanda_titulo', 'conteudo', 'autor_id', 'tipo_autor', 'criado_em', 'anexos')
        read_only_fields = ['id', 'criado_em']

class DemandaSerializer(serializers.ModelSerializer):
    mensagens = MensagemDemandaSerializer(many=True, read_only=True)
    cliente_nome = serializers.ReadOnlyField(source='cliente_id.nome')
    usuario_nome = serializers.ReadOnlyField(source='usuario.nome')
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Demanda
        fields = ['id', 'usuario', 'usuario_nome', 'titulo', 'descricao', 'status', 
                 'cliente_id', 'cliente_nome', 'is_admin',
                 'criado_em', 'atualizado_em', 'mensagens']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def get_is_admin(self, obj):
        request = self.context.get('request')
        if request and request.user and hasattr(request, 'query_params'):
            usuario_id = request.query_params.get('usuario')
            if usuario_id:
                try:
                    usuario_cliente = UsuarioCliente.objects.get(
                        usuario_id=usuario_id,
                        cliente=obj.cliente_id
                    )
                    return usuario_cliente.is_admin
                except UsuarioCliente.DoesNotExist:
                    return False
        return False 