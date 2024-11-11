from rest_framework import serializers
from hom.models import UsuarioLoja
from hom.models import Produto, Cor, Imagem, Tamanho, Categoria, CategoriaProduto, Disponibilidade
from hom.models import Favoritos, Carrinho, Pedido, ItemPedido

from hom.models import UsuarioPersonal
from hom.models import Perguntas, Respostas

from hom.models import ItensProAcos

class UsuarioLojaSerializer(serializers.ModelSerializer):
   class Meta:
      model = UsuarioLoja
      fields = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha','administrador')

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
    is_favorito = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ['id', 'descricao', 'valor', 'palavras_chave', 'cores','tamanhos','categorias','is_favorito']

    def get_cores(self, obj):
        cores = Cor.objects.filter(produto=obj)
        return CorSerializer(cores, many=True).data

    def get_tamanhos(self, obj):
        tamanhos = Tamanho.objects.filter(produto=obj)
        return TamanhoSerializer(tamanhos, many=True).data

    def get_categorias(self, obj):
        categorias = CategoriaProduto.objects.filter(produto=obj)
        return CategoriaProdutoSerializer(categorias, many=True).data

    def get_is_favorito(self, obj):
      user = self.context.get('request').user
      if user.is_authenticated:
          return Favoritos.objects.filter(cliente=user, produto=obj).exists()
      return False

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
    class Meta:
      model = Pedido
      fields = ('id', 'cliente', 'status', 'data_pedido', 'atualizado_em')

class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
      model = ItemPedido
      fields = ('id', 'pedido', 'produto', 'quantidade')

# ---------------------------------PERSONAL---------------------------------------------------------


class UsuarioPersonalSerializer(serializers.ModelSerializer):
   class Meta:
      model = UsuarioPersonal
      fields = ('id','nome','cpf','email','celular','senha','cliente','administrador')


class PerguntasSerializer(serializers.ModelSerializer):
   class Meta:
      model = Perguntas
      fields = ('id','pergunta')


class RespostasSerializer(serializers.ModelSerializer):
    pergunta_texto = serializers.CharField(source='pergunta.pergunta', read_only=True)

    class Meta:
        model = Respostas
        fields = ['id', 'usuario', 'pergunta', 'resposta', 'pergunta_texto']

# ---------------------------------PRO ACOS---------------------------------------------------------

class ItensProAcosSerializer(serializers.ModelSerializer):
    class Meta:
      model = ItensProAcos
      fields = ('id', 'item','quant', 'datalote','datavenda')
