from rest_framework import serializers
from hom.models import UsuarioLoja, Endereco
from hom.models import Produto, Cor, Imagem, Tamanho, Categoria, CategoriaProduto, Disponibilidade
from hom.models import Favoritos, Carrinho, Pedido, ItemPedido

from hom.models import UsuarioPersonal
from hom.models import Perguntas, Respostas, Translation

from hom.models import ItensProAcos

from hom.models import UsuarioDiscipulado, IgrejaParceira, Discipulados, TurmaDiscipulado, AlunoTurmaDiscipulado
from hom.models import PerguntasDiscipulado, RespostasDiscipulado

from hom.models import UsuarioSjb, Pregacao, Membros, Devocional, Igreja, Pastor, Download

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

class UsuarioDiscipuladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioDiscipulado
        fields = ['id', 'nome', 'email', 'telefone', 'igreja', 'senha', 'nivel', 'discipulador', 'administrador']  


class TurmaDiscipuladoSerializer(serializers.ModelSerializer):
    discipulador_nome = serializers.ReadOnlyField(source='discipulador.nome')
    discipulado_nome = serializers.ReadOnlyField(source='discipulado.nome')
    alunos = serializers.SerializerMethodField()

    class Meta:
        model = TurmaDiscipulado
        fields = ['id', 'nome_turma', 'discipulador', 'discipulador_nome', 'discipulado', 'discipulado_nome', 
                  'data_inicio', 'data_fim', 'alunos']  

    def get_alunos(self, obj):
        alunos = AlunoTurmaDiscipulado.objects.filter(turma=obj)
        return AlunoTurmaDiscipuladoSerializer(alunos, many=True).data


class AlunoTurmaDiscipuladoSerializer(serializers.ModelSerializer):
    discipulo_nome = serializers.ReadOnlyField(source='discipulo.nome')

    class Meta:
        model = AlunoTurmaDiscipulado
        fields = ['id', 'turma', 'discipulo', 'discipulo_nome'] 


class DiscipuladosSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()

    class Meta:
        model = Discipulados
        fields = ['id', 'nome', 'licao', 'nivel', 'proximoEstudo' , 'foto']

    def get_foto(self, obj):
        return obj.foto.name if obj.foto else None

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
        fields = ['id', 'usuario','turma', 'pergunta', 'resposta', 'pergunta_texto']



# ---------------------------------PIB São João Betim---------------------------------------------------------

class UsuarioSjbSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSjb
        fields = ('id', 'login', 'senha')

class PregacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregacao
        fields = ('id', 'descricao', 'link','data')

class MembrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membros
        fields = '__all__'

class IgrejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Igreja
        fields = ('id', 'nome', 'lema','logo','endereco', 'instagram','youtube','email','nome_banco','num_banco','agencia','conta_corrente','chave_pix','tipo_chave_pix','qr_code_pix')

class PastorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pastor
        fields = ('id', 'nome', 'cargo','foto','data_nascimento','telefone','youtube','email')

class DevocionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devocional
        fields = '__all__'

class DownloadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ('id', 'nome', 'arquivo')
