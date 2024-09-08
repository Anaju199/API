from rest_framework import viewsets, filters, status
from hom.models import Usuario
from hom.serializer import UsuarioSerializer
from hom.models import Produto, Cor, Imagem, Tamanho, Categoria, Disponibilidade
from hom.serializer import ProdutoSerializer, CorSerializer, ImagemSerializer, TamanhoSerializer, CategoriaSerializer, DisponibilidadeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class AJUsuariosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']


@api_view(['GET'])
def aj_lista_usuarios(request):
    id = request.GET.get('id', None)

    usuarios = Usuario.objects.all()

    if id:
        usuarios = usuarios.filter(id=id)

    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

class AJLoginView(APIView):
    def post(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')
        try:
            usuario = Usuario.objects.get(cpf=cpf)
            if check_password(senha, usuario.senha):  # Certifique-se de que a senha esteja hashada corretamente
                refresh = RefreshToken.for_user(usuario)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': usuario.id,  # Inclua o ID do usuário na resposta
                    'nome': usuario.nome
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuario.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ProdutoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Produto"""
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['descricao']
    ordering_fields = ['descricao']

class CorViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Cor"""
    queryset = Cor.objects.all()
    serializer_class = CorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['cor']
    ordering_fields = ['cor']

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

class TamanhoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Tamanho"""
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['tamanho']
    ordering_fields = ['tamanho']

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
