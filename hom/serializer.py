from rest_framework import serializers
from hom.models import Usuario
from hom.models import Produto, Cor, Imagem, Tamanho, Categoria, Disponibilidade

class UsuarioSerializer(serializers.ModelSerializer):
   class Meta:
      model = Usuario
      fields = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha')

class ImagemSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.ReadOnlyField(source='produto.descricao')
    cor_nome = serializers.ReadOnlyField(source='cor.cor')

    class Meta:
        model = Imagem
        fields = ['id', 'produto', 'produto_descricao', 'cor', 'cor_nome', 'imagem', 'inicial']

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
        categorias = Categoria.objects.filter(produto=obj)
        return CategoriaSerializer(categorias, many=True).data

class CategoriaSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.ReadOnlyField(source='produto.descricao')

    class Meta:
      model = Categoria
      fields = ('id','produto', 'produto_descricao', 'categoria')

class TamanhoSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.ReadOnlyField(source='produto.descricao')

    class Meta:
      model = Tamanho
      fields = ('id', 'produto', 'produto_descricao', 'tamanho')

class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
      model = Disponibilidade
      fields = ('id', 'produto', 'tamanho','quantidade_disponivel')