from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .pagination import CustomPagination

from ch.models import UsuarioCasaRohr, Fotos, Catalogos
from ch.serializer import UsuarioCasaRohrSerializer, FotosSerializer, CatalogosSerializer

class ChUsuariosCasaRohrViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioCasaRohr.objects.all().order_by('nome')
    serializer_class = UsuarioCasaRohrSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

    
class ChLoginCasaRohrView(APIView):
    def post(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')
        try:
            usuario = UsuarioCasaRohr.objects.get(cpf=cpf)
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
        except UsuarioCasaRohr.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class ChFotosViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = Fotos.objects.all()
    serializer_class = FotosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['descricao']
    ordering_fields = ['id']
    pagination_class = CustomPagination

@api_view(['GET'])
def ch_lista_categorias(request):
    categoria = [opcao[0] for opcao in Fotos.OPCOES_CATEGORIA]
    return Response(categoria)

@api_view(['GET'])
def ch_lista_fotos(request):
    categoria = request.GET.get('categoria', None)

    fotos = Fotos.objects.all()

    if categoria:
        fotos = fotos.filter(categoria=categoria)

    serializer = FotosSerializer(fotos, many=True)
    return Response(serializer.data)


class ChCatalogosViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = Catalogos.objects.all()
    serializer_class = CatalogosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['descricao']
    ordering_fields = ['id']
    pagination_class = CustomPagination