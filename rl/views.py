from rest_framework import viewsets, filters, status
import json
from rl.models import Programacao, Diretoria, Ministerio, Missionario, Lideranca, FotosMinisterios, Usuario, RedesSociais
from rl.models import Pregacao, Membros, Igreja, EscolaDominical, Pastor
from rl.serializer import ProgramacaoSerializer, DiretoriaSerializer, MinisterioSerializer, MissionarioSerializer
from rl.serializer import LiderancaSerializer, FotosMinisteriosSerializer, UsuariosSerializer, PregacaoSerializer
from rl.serializer import MembrosSerializer, IgrejaSerializer, EscolaDominicalSerializer, PastorSerializer, RedesSociaisSerializer
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.functions import ExtractMonth

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

    # Filtra pelas condições de sociedade e ano
    if sociedade:
        diretorias = diretorias.filter(sociedade=sociedade)
    if ano:
        diretorias = diretorias.filter(ano=ano)

    # Serializa as diretorias
    serializer = DiretoriaSerializer(diretorias, many=True)
    diretorias_data = serializer.data

    # Para cada diretoria, busca as redes sociais correspondentes ao responsável
    for diretoria in diretorias_data:
        redes_sociais = RedesSociais.objects.filter(responsavel=sociedade, rede_social = 'Instagram').values_list('link', flat=True)
        diretoria['instagram'] = redes_sociais  # Adiciona apenas os links ao resultado

    return Response(diretorias_data)


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
        liderancas = liderancas.filter(nome__icontains=nome)
    if cargo:
        liderancas = liderancas.filter(cargo=cargo)
    if ano:
        try:
            ano = int(ano)  # Certifique-se de que o valor do ano seja um número
            liderancas = liderancas.filter(ano_inicio__lte=ano, ano_fim__gte=ano)
        except ValueError:
            return Response({"error": "O valor de 'ano' deve ser um número inteiro válido."}, status=400)

    serializer = LiderancaSerializer(liderancas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_cargos(request):
    cargos = [opcao[0] for opcao in Lideranca.OPCOES_CARGO]
    return Response(cargos)

@api_view(['GET'])
def lista_cargos_pastor(request):
    cargos = [opcao[0] for opcao in Pastor.OPCOES_CARGO]
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


class MembrosViewSet(viewsets.ModelViewSet):
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
    mes = request.GET.get('mes', None)

    membros = Membros.objects.all()

    if nome:
        membros = membros.filter(nome__icontains=nome)
    if sociedade:
        membros = membros.filter(sociedade=sociedade)
    if mes:
        try:
            mes = int(mes)  # Certifique-se de que o valor do mes seja um número
            membros = membros.annotate(mes_nascimento=ExtractMonth('data_nascimento')).filter(mes_nascimento=mes)
        except ValueError:
            return Response({"error": "O valor de 'mes' deve ser um número inteiro válido."}, status=400)

    serializer = MembrosSerializer(membros, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_aniversariantes(request):
    nome = request.GET.get('nome', None)
    mes = request.GET.get('mes', None)

    # Filtrar membros e pastores
    membros = Membros.objects.filter(ativo=1)  # Somente membros com ativo = 1
    pastores = Pastor.objects.all()

    # Filtros aplicados a membros e pastores
    if nome:
        membros = membros.filter(nome__icontains=nome)
        pastores = pastores.filter(nome__icontains=nome)

    if mes:
        try:
            mes = int(mes)  # Certifique-se de que o valor do mês seja um número
            membros = membros.annotate(mes_nascimento=ExtractMonth('data_nascimento')).filter(mes_nascimento=mes)
            pastores = pastores.annotate(mes_nascimento=ExtractMonth('data_nascimento')).filter(mes_nascimento=mes)
        except ValueError:
            return Response({"error": "O valor de 'mes' deve ser um número inteiro válido."}, status=400)

    # Unificar os dados de membros e pastores em uma única lista
    lista_unificada = []

    for membro in membros:
        lista_unificada.append({
            "nome": membro.nome,
            "data_nascimento": membro.data_nascimento
        })

    for pastor in pastores:
        lista_unificada.append({
            "nome": pastor.nome,
            "data_nascimento": pastor.data_nascimento
        })

    # Ordenar a lista unificada por mês e dia de nascimento
    lista_unificada.sort(key=lambda x: (x['data_nascimento'].month, x['data_nascimento'].day))

    return Response(lista_unificada)


class IgrejaViewSet(viewsets.ModelViewSet):
    queryset = Igreja.objects.all()
    serializer_class = IgrejaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


class EscolaDominicalViewSet(viewsets.ModelViewSet):
    """Exibindo todos os EscolaDominicals"""
    queryset = EscolaDominical.objects.all()
    serializer_class = EscolaDominicalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['classe']
    pagination_class = CustomPagination


class PastorViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pastor"""
    queryset = Pastor.objects.all()
    serializer_class = PastorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_pastor(request):
    nome = request.GET.get('nome', None)
    cargo = request.GET.get('cargo', None)

    pastor = Pastor.objects.all()

    if nome:
        pastor = pastor.filter(nome__icontains=nome)
    if cargo:
        pastor = pastor.filter(cargo=cargo)

    serializer = PastorSerializer(pastor, many=True)
    return Response(serializer.data)


class RedesSociaisViewSet(viewsets.ModelViewSet):
    """Exibindo todos os RedesSociais"""
    queryset = RedesSociais.objects.all()
    serializer_class = RedesSociaisSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['responsavel']
    pagination_class = CustomPagination

@api_view(['GET'])
def lista_redeSocial(request):
    responsavel = request.GET.get('responsavel', None)
    rede_social = request.GET.get('rede_social', None)

    redeSocial = RedesSociais.objects.all()

    if responsavel:
        redeSocial = redeSocial.filter(responsavel=responsavel)
    if rede_social:
        redeSocial = redeSocial.filter(rede_social=rede_social)

    serializer = RedesSociaisSerializer(redeSocial, many=True)
    return Response(serializer.data)
