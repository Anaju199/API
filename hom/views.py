from rest_framework import viewsets, filters, status

from hom.models import UsuarioPersonal, Perguntas, Respostas
from hom.serializer import UsuarioPersonalSerializer, PerguntasSerializer, RespostasSerializer


from hom.models import UsuarioLoja, Produto, Cor, Imagem, Tamanho, Categoria, CategoriaProduto, Disponibilidade
from hom.models import Favoritos, Carrinho, Pedido, ItemPedido
from hom.serializer import UsuarioLojaSerializer, ProdutoSerializer, CorSerializer, ImagemSerializer, TamanhoSerializer
from hom.serializer import CategoriaProdutoSerializer, CategoriaSerializer, DisponibilidadeSerializer
from hom.serializer import FavoritosSerializer, CarrinhoSerializer, PedidoSerializer, ItemPedidoSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import json

from hom.models import ItensProAcos
from hom.serializer import ItensProAcosSerializer
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .pagination import CustomPagination

class UsuariosLojaViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioLoja.objects.all()
    serializer_class = UsuarioLojaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']


@api_view(['GET'])
def lista_usuarios_loja(request):
    id = request.GET.get('id', None)

    usuarios = UsuarioLoja.objects.all()

    if id:
        usuarios = usuarios.filter(id=id)

    serializer = UsuarioLojaSerializer(usuarios, many=True)
    return Response(serializer.data)

class LoginLojaView(APIView):
    def post(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')
        try:
            usuario = UsuarioLoja.objects.get(cpf=cpf)
            if check_password(senha, usuario.senha):  # Certifique-se de que a senha esteja hashada corretamente
                refresh = RefreshToken.for_user(usuario)
                role = 'admin' if usuario.administrador else 'user'
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': usuario.id,  # Inclua o ID do usuário na resposta
                    'nome': usuario.nome,
                    'role': role
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UsuarioLoja.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all().order_by('descricao')
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['descricao']
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        produto = serializer.save()
        return Response({
            'id': produto.id,
            'descricao': produto.descricao
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        if id is not None:
            return Produto.objects.filter(id=id)
        return Produto.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CorViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Cor"""
    queryset = Cor.objects.all()
    serializer_class = CorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['cor']
    ordering_fields = ['cor']

    def get_queryset(self):
        produto_id = self.request.query_params.get('produto_id', None)
        if produto_id is not None:
            return Cor.objects.filter(produto_id=produto_id)
        return Cor.objects.all()

class ImagemViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Imagem"""
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['imagem']
    ordering_fields = ['imagem']

class CategoriaViewSet(viewsets.ModelViewSet):
    """Exibindo todos as categoria"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['categoria']
    ordering_fields = ['categoria']

class CategoriaProdutoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as categoria"""
    queryset = CategoriaProduto.objects.all()
    serializer_class = CategoriaProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['categoria']
    ordering_fields = ['categoria']

class TamanhoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Tamanho"""
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['tamanho']
    ordering_fields = ['tamanho']

    def get_queryset(self):
        produto_id = self.request.query_params.get('produto_id', None)
        if produto_id is not None:
            return Tamanho.objects.filter(produto_id=produto_id)
        return Tamanho.objects.all()

class DisponibilidadeViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Disponibilidade"""
    queryset = Disponibilidade.objects.all()
    serializer_class = DisponibilidadeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']


@api_view(['GET'])
def lista_produtos(request):
    filtro = request.GET.get('filtro', None)

    produtos = Produto.objects.all()

    if filtro:
         produtos = produtos.filter(Q(descricao__icontains=filtro) | Q(palavras_chave__icontains=filtro))

    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)

class FavoritosViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Favoritos"""
    queryset = Favoritos.objects.all()
    serializer_class = FavoritosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Retorna o ID do objeto criado
        favorito_id = serializer.instance.id
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"id": favorito_id, **serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

@api_view(['GET'])
def isFavorito(request):
    cliente = request.GET.get('cliente', None)
    produto = request.GET.get('produto', None)

    favorito = Favoritos.objects.all()

    if cliente:
         favorito = favorito.filter(cliente = cliente)
    if produto:
         favorito = favorito.filter(produto = produto)

    if favorito.exists():
        favorito_obj = favorito.first()  # Obtém o primeiro favorito encontrado
        return Response({'isFavorito': True, 'id': favorito_obj.id})
    else:
        return Response({'isFavorito': False, 'id': None})
    

def lista_favoritos(request):
    cliente = request.GET.get('cliente', None)

    favoritos = Favoritos.objects.all()

    if cliente:
        favoritos = favoritos.filter(cliente=cliente)

    # Monta a resposta com os produtos favoritados
    produtos = []
    for favorito in favoritos:
        produto = favorito.produto
        cores = Cor.objects.filter(produto=produto)
        imagens = Imagem.objects.filter(produto=produto)

        produtos.append({
            "id": produto.id,
            "descricao": produto.descricao,
            "valor": produto.valor,
            "cores": [
                {
                    "id": cor.id,
                    "cor": cor.cor,
                    "inicial": cor.inicial,
                    "imagens": ImagemSerializer(imagens.filter(cor=cor), many=True).data
                }
                for cor in cores
            ]
        })

    return JsonResponse(produtos, safe=False)

class CarrinhoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Carrinho"""
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']

def lista_carrinho(request):
    cliente = request.GET.get('cliente', None)

    carrinhos = Carrinho.objects.all()

    if cliente:
        carrinhos = carrinhos.filter(cliente=cliente)

    # Monta a resposta com os produtos no carrinho
    produtos = []
    for item in carrinhos:
        produto = item.produto
        cores = Cor.objects.filter(produto=produto)
        imagens = Imagem.objects.filter(produto=produto)

        produtos.append({
            "id": item.id,
            "produto_id": produto.id,
            "descricao": produto.descricao,
            "valor": produto.valor,
            "cor_selecionada": {
                "cor_id": item.cor.id,
                "cor": item.cor.cor,
                "inicial": item.cor.inicial,
                "imagens": ImagemSerializer(imagens.filter(cor=item.cor), many=True).data,
            },
            "tamanho_selecionado": {
                "id": item.tamanho.id,
                "tamanho": item.tamanho.tamanho,
            },
            "quantidade": item.quantidade,
        })

    return JsonResponse(produtos, safe=False)

class PedidoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Pedido"""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Retorna o ID do objeto criado
        pedido_id = serializer.instance.id
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"id": pedido_id, **serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

class ItemPedidoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as ItemPedido"""
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']


# ---------------------------------PERSONAL---------------------------------------------------------


class UsuariosPersonalViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioPersonal.objects.all().order_by('nome')
    serializer_class = UsuarioPersonalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

class UsuariosPersonalClientesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioPersonal.objects.filter(cliente=True, administrador=False).order_by('nome')
    serializer_class = UsuarioPersonalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


@api_view(['GET'])
def lista_usuarios_personal(request):
    nome = request.GET.get('nome', None)
    cliente = request.GET.get('cliente', None)
    administrador = request.GET.get('adm', None)

    usuarios = UsuarioPersonal.objects.all()

    if nome:
        usuarios = usuarios.filter(nome=nome)
    if cliente:
        usuarios = usuarios.filter(cliente=cliente)
    if administrador:
        usuarios = usuarios.filter(administrador=administrador)

    serializer = UsuarioPersonalSerializer(usuarios, many=True)
    return Response(serializer.data)


class LoginPersonalView(APIView):
    def post(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')
        try:
            usuario = UsuarioPersonal.objects.get(cpf=cpf)
            if check_password(senha, usuario.senha):  # Certifique-se de que a senha esteja hashada corretamente
                refresh = RefreshToken.for_user(usuario)
                role = 'admin' if usuario.administrador else 'user'
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': usuario.id,  # Inclua o ID do usuário na resposta
                    'nome': usuario.nome,
                    'role': role
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UsuarioPersonal.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class PerguntasViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Perguntas"""
    queryset = Perguntas.objects.all()
    serializer_class = PerguntasSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['pergunta']
    pagination_class = CustomPagination


@api_view(['GET'])
def lista_perguntas(request):
    pergunta = request.GET.get('pergunta', None)

    perguntas = Perguntas.objects.all()

    if pergunta:
        perguntas = perguntas.filter(pergunta__icontains=pergunta)

    serializer = PerguntasSerializer(perguntas, many=True)
    return Response(serializer.data)


class RespostasViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Respostas"""
    queryset = Respostas.objects.all()
    serializer_class = RespostasSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['resposta']
    pagination_class = CustomPagination



@api_view(['GET'])
def lista_respostas(request):
    resposta = request.GET.get('resposta', None)
    usuario = request.GET.get('usuario', None)

    respostas = Respostas.objects.all()

    if resposta:
        respostas = respostas.filter(resposta__icontains=resposta)
    if usuario:
        respostas = respostas.filter(usuario=usuario)

    serializer = RespostasSerializer(respostas, many=True)
    return Response(serializer.data)

# ---------------------------------PRO ACOS---------------------------------------------------------

class ItensProAcosViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = ItensProAcos.objects.all()
    serializer_class = ItensProAcosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['item','quant', 'datalote','datavenda']
    ordering_fields = ['id']
    pagination_class = CustomPagination


@api_view(['GET'])
def lista_itens_proacos(request):
    datalote = request.GET.get('datalote', None)
    datavenda = request.GET.get('datavenda', None)
    item = request.GET.get('item', None)

    itensProAcos = ItensProAcos.objects.all()

    datalote_date = timezone.datetime.strptime(datalote, '%Y-%m-%d').date()
    datavenda_date = timezone.datetime.strptime(datavenda, '%Y-%m-%d').date()

    # Filtra itens onde datalote está entre datalote e datavenda
    itensProAcos = itensProAcos.filter(datalote__gte=datalote_date, datalote__lte=datavenda_date)

    if item:
        itensProAcos = itensProAcos.filter(Q(item__icontains=item))

    serializer = ItensProAcosSerializer(itensProAcos, many=True)
    return Response(serializer.data)
