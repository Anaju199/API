from rest_framework import serializers
from hom.models import UsuarioLoja, Endereco
from hom.models import Produto, Cor, Imagem, Tamanho, Categoria, CategoriaProduto, Disponibilidade
from hom.models import Favoritos, Carrinho, Pedido, ItemPedido

from hom.models import UsuarioPersonal
from hom.models import Perguntas, Respostas, Translation

from hom.models import ItensProAcos

from hom.models import UsuarioBase, Discipulador, Discipulo, IgrejaParceira, Discipulados
from hom.models import PerguntasDiscipulado, RespostasDiscipulado

class UsuarioLojaSerializer(serializers.ModelSerializer):
   class Meta:
      model = UsuarioLoja
      fields = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha','administrador')

class EnderecoSerializer(serializers.ModelSerializer):
   # Adicione um campo de leitura para mostrar o nome do usuario
   usuario_nome = serializers.ReadOnlyField(source='usuario.nome')

   class Meta:
      model = Endereco
      fields = ('id','usuario','usuario_nome','rua','numero','complemento','bairro','cidade','estado','pais','cep','principal')

class ImagemSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.ReadOnlyField(source='produto.descricao')
    cor_nome = serializers.ReadOnlyField(source='cor.cor')

    class Meta:
        model = Imagem
        fields = ['id', 'produto', 'produto_descricao', 'cor', 'cor_nome', 'foto', 'inicial']

    def get_cor(self, obj):
        cor = Cor.objects.filter(cor=obj)
        return CorSerializer(cor, many=True).data

class CorSerializer(serializers.ModelSerializer):
   # Adicione um campo de leitura para mostrar a descricao do produto
    produto_descricao = serializers.ReadOnlyField(source='produto.descricao')
    imagens = serializers.SerializerMethodField()

    class Meta:
        model = Cor
        fields = ['id', 'produto', 'produto_descricao', 'cor', 'inicial', 'imagens']

    def get_imagens(self, obj):
        imagens = Imagem.objects.filter(cor=obj)
        return ImagemSerializer(imagens, many=True).data

class ProdutoSerializer(serializers.ModelSerializer):
    cores = serializers.SerializerMethodField()
    tamanhos = serializers.SerializerMethodField()
    categorias = serializers.SerializerMethodField()
    # is_favorito = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ['id', 'descricao', 'valor', 'palavras_chave', 'cores','tamanhos','categorias']

    def get_cores(self, obj):
        cores = Cor.objects.filter(produto=obj)
        return CorSerializer(cores, many=True).data

    def get_tamanhos(self, obj):
        tamanhos = Tamanho.objects.filter(produto=obj)
        return TamanhoSerializer(tamanhos, many=True).data

    def get_categorias(self, obj):
        categorias = CategoriaProduto.objects.filter(produto=obj)
        return CategoriaProdutoSerializer(categorias, many=True).data

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
      model = Categoria
      fields = ('id','categoria')

class CategoriaProdutoSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.ReadOnlyField(source='produto.descricao')
    categoria_nome = serializers.ReadOnlyField(source='categoria.categoria')

    class Meta:
        model = CategoriaProduto
        fields = ('id', 'produto', 'produto_descricao', 'categoria', 'categoria_nome')

class TamanhoSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.ReadOnlyField(source='produto.descricao')

    class Meta:
      model = Tamanho
      fields = ('id', 'produto', 'produto_descricao', 'tamanho')

class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
      model = Disponibilidade
      fields = ('id', 'produto', 'cor', 'tamanho','quantidade_disponivel')

class FavoritosSerializer(serializers.ModelSerializer):
    class Meta:
      model = Favoritos
      fields = ('id', 'cliente', 'produto')

class CarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
      model = Carrinho
      fields = ('id', 'cliente', 'produto', 'cor', 'tamanho', 'quantidade')

class PedidoSerializer(serializers.ModelSerializer):
    itens_pedido = serializers.SerializerMethodField()
    numero_pedido = serializers.ReadOnlyField()

    class Meta:
      model = Pedido
      fields = ('id', 'cliente', 'status', 'data_pedido', 'atualizado_em','quant_itens','valor','data_pgt','itens_pedido','numero_pedido')

    def get_itens_pedido(self, obj):
        itens_pedido = ItemPedido.objects.filter(pedido=obj)
        return ItemPedidoSerializer(itens_pedido, many=True).data  

class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
      model = ItemPedido
      fields = ('id', 'pedido', 'produto_id','descricao','valor','cor','tamanho', 'quantidade','foto')

# ---------------------------------PERSONAL---------------------------------------------------------

class UsuarioPersonalSerializer(serializers.ModelSerializer):
   class Meta:
      model = UsuarioPersonal
      fields = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha','cliente','administrador')


class PerguntasSerializer(serializers.ModelSerializer):
   class Meta:
      model = Perguntas
      fields = ('id','pergunta')


class RespostasSerializer(serializers.ModelSerializer):
    pergunta_texto = serializers.CharField(source='pergunta.pergunta', read_only=True)

    class Meta:
        model = Respostas
        fields = ['id', 'usuario', 'pergunta', 'resposta', 'pergunta_texto']


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'key', 'pt', 'en', 'es']        

# ---------------------------------PRO ACOS---------------------------------------------------------

class ItensProAcosSerializer(serializers.ModelSerializer):
    class Meta:
      model = ItensProAcos
      fields = ('id', 'item','quant', 'datalote','datavenda')


# ---------------------------------DISCIPULADO---------------------------------------------------------

class UsuarioBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioBase
        fields = ['id', 'nome', 'senha', 'email', 'telefone']  # Campos comuns a todos os usuários


class DiscipuladorSerializer(UsuarioBaseSerializer):
    igreja = serializers.PrimaryKeyRelatedField(queryset=IgrejaParceira.objects.all())
    administrador = serializers.BooleanField()
    discipulados = serializers.PrimaryKeyRelatedField(
        queryset=Discipulados.objects.all(), many=True
    )

    class Meta(UsuarioBaseSerializer.Meta):
        model = Discipulador
        fields = UsuarioBaseSerializer.Meta.fields + ['discipulados','igreja','administrador']


class DiscipuloSerializer(UsuarioBaseSerializer):
    nivel = serializers.CharField()
    discipulador = serializers.PrimaryKeyRelatedField(queryset=Discipulador.objects.all())

    class Meta(UsuarioBaseSerializer.Meta):
        model = Discipulo
        fields = UsuarioBaseSerializer.Meta.fields + ['nivel', 'discipulador']


class DiscipuladosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipulados
        fields = ['id', 'nome', 'licao', 'nivel', 'proximoEstudo' , 'foto']


class IgrejaParceiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = IgrejaParceira
        fields = ['id', 'nome']


class PerguntasDiscipuladoSerializer(serializers.ModelSerializer):
    discipulado_nome = serializers.CharField(source='discipulado.nome', read_only=True)
    
    class Meta:
      model = PerguntasDiscipulado
      fields = ('id','discipulado','discipulado_nome','pergunta')


class RespostasDiscipuladoSerializer(serializers.ModelSerializer):
    pergunta_texto = serializers.CharField(source='pergunta.pergunta', read_only=True)

    class Meta:
        model = RespostasDiscipulado
        fields = ['id', 'usuario', 'pergunta', 'resposta', 'pergunta_texto']

