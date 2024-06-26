from rest_framework import viewsets, filters, status
import json
from rl.models import Programacao, Diretoria, Ministerio, Missionario, Lideranca, FotosMinisterios, Usuario, Pregacao, Membros
from rl.serializer import ProgramacaoSerializer, DiretoriaSerializer, MinisterioSerializer, MissionarioSerializer, LiderancaSerializer, FotosMinisteriosSerializer, UsuariosSerializer, PregacaoSerializer, MembrosSerializer
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class ProgramacoesViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = Programacao.objects.all()
    serializer_class = ProgramacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['mes','ano','descricao','sociedade']
    ordering_fields = ['dia','mes']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_programacoes(request):
    mes = request.GET.get('mes', None)
    ano = request.GET.get('ano', None)
    descricao = request.GET.get('descricao', None)
    sociedade = request.GET.get('sociedade', None)

    programacoes = Programacao.objects.all()

    if mes:
        programacoes = programacoes.filter(mes=mes)
    if ano:
        programacoes = programacoes.filter(ano=ano)
    if descricao:
        programacoes = programacoes.filter(Q(descricao__icontains=descricao))
    if sociedade:
        programacoes = programacoes.filter(sociedade=sociedade)

    serializer = ProgramacaoSerializer(programacoes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_sociedades_prog(request):
    sociedades = [opcao[0] for opcao in Programacao.OPCOES_SOCIEDADE]
    return Response(sociedades)


class DiretoriasViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Diretorias"""
    queryset = Diretoria.objects.all()
    serializer_class = DiretoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sociedade']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_diretorias(request):
    sociedade = request.GET.get('sociedade', None)
    ano = request.GET.get('ano', None)

    diretorias = Diretoria.objects.all()

    if sociedade:
        diretorias = diretorias.filter(sociedade=sociedade)
    if ano:
        diretorias = diretorias.filter(ano=ano)

    serializer = DiretoriaSerializer(diretorias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_sociedades(request):
    sociedades = [opcao[0] for opcao in Diretoria.OPCOES_SOCIEDADE]
    return Response(sociedades)



class MissionariosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Missionarios"""
    queryset = Missionario.objects.all()
    serializer_class = MissionarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_missionarios(request):
    nome = request.GET.get('nome', None)

    missionarios = Missionario.objects.all()

    if nome:
        missionarios = missionarios.filter(nome=nome)

    serializer = MissionarioSerializer(missionarios, many=True)
    return Response(serializer.data)



class LiderancasViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Liderancas"""
    queryset = Lideranca.objects.all()
    serializer_class = LiderancaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_liderancas(request):
    nome = request.GET.get('nome', None)
    cargo = request.GET.get('cargo', None)
    ano = request.GET.get('ano', None)

    liderancas = Lideranca.objects.all()

    if nome:
        liderancas = liderancas.filter(nome=nome)
    if cargo:
        liderancas = liderancas.filter(cargo=cargo)
    if ano:
        liderancas = liderancas.filter(ano=ano)

    serializer = LiderancaSerializer(liderancas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_cargos(request):
    cargos = [opcao[0] for opcao in Lideranca.OPCOES_CARGO]
    return Response(cargos)


class MinisteriosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Ministerios"""
    queryset = Ministerio.objects.all()
    serializer_class = MinisterioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_ministerios(request):
    nome = request.GET.get('nome', None)
    ano = request.GET.get('ano', None)

    ministerios = Ministerio.objects.all()

    if nome:
        ministerios = ministerios.filter(nome=nome)
    if ano:
        ministerios = ministerios.filter(ano=ano)

    serializer = MinisterioSerializer(ministerios, many=True)
    return Response(serializer.data)



class FotosMinisteriosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os FotosMinisterios"""
    queryset = FotosMinisterios.objects.all()
    serializer_class = FotosMinisteriosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['ministerio']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_fotosMinisterios(request):
    ministerio = request.GET.get('ministerio', None)

    fotosMinisterios = FotosMinisterios.objects.all()

    if ministerio:
        fotosMinisterios = fotosMinisterios.filter(ministerio__nome=ministerio)

    serializer = FotosMinisteriosSerializer(fotosMinisterios, many=True)
    return Response(serializer.data)


class UsuariosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuariosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['login']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_usuarios(request):
    login = request.GET.get('login', None)

    usuarios = Usuario.objects.all()

    if login:
        usuarios = usuarios.filter(login=login)

    serializer = UsuariosSerializer(usuarios, many=True)
    return Response(serializer.data)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        senha = request.data.get('senha')
        try:
            usuario = Usuario.objects.get(login=login)
            if check_password(senha, usuario.senha):  # Certifique-se de que a senha esteja hashada corretamente
                refresh = RefreshToken.for_user(usuario)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuario.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)




class PregacaoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pregacao"""
    queryset = Pregacao.objects.all()
    serializer_class = PregacaoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['descricao']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_pregacoes(request):
    descricao = request.GET.get('descricao', None)

    pregacao = Pregacao.objects.all()

    if descricao:
        pregacao = pregacao.filter(descricao=descricao)

    serializer = PregacaoSerializer(pregacao, many=True)
    return Response(serializer.data)


class MembrossViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Membross"""
    queryset = Membros.objects.all()
    serializer_class = MembrosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sociedade']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_membros(request):
    nome = request.GET.get('nome', None)
    sociedade = request.GET.get('sociedade', None)

    membros = Membros.objects.all()

    if nome:
        membros = membros.filter(nome=nome)
    if sociedade:
        membros = membros.filter(sociedade=sociedade)

    serializer = MembrosSerializer(membros, many=True)
    return Response(serializer.data)
