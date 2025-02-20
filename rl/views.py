from rest_framework import viewsets, filters, status
from django.db import connections
from rl.models import Programacao, Diretoria, Ministerio, Missionario, Lideranca, Usuario, RedesSociais
from rl.models import Pregacao, Membros, Igreja, EscolaDominical, Pastor, Download, Fotos
from rl.serializer import ProgramacaoSerializer, DiretoriaSerializer, MinisterioSerializer, MissionarioSerializer
from rl.serializer import LiderancaSerializer, UsuariosSerializer, PregacaoSerializer
from rl.serializer import MembrosSerializer, IgrejaSerializer, EscolaDominicalSerializer, PastorSerializer, RedesSociaisSerializer
from rl.serializer import DownloadsSerializer, FotosSerializer

from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count, Case, When, Value

from datetime import date

class RlProgramacoesViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = Programacao.objects.all().order_by('-data')
    serializer_class = ProgramacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['mes','ano','descricao','sociedade']
    ordering_fields = ['dia','mes']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_programacoes(request):
    mes = request.GET.get('mes', None)
    ano = request.GET.get('ano', None)
    descricao = request.GET.get('descricao', None)
    sociedade = request.GET.get('sociedade', None)

    programacoes = Programacao.objects.all()

    if mes:
        programacoes = programacoes.filter(data__month=int(mes))
    if ano:
        programacoes = programacoes.filter(data__year=int(ano))
    if descricao:
        programacoes = programacoes.filter(Q(descricao__icontains=descricao))
    if sociedade:
        programacoes = programacoes.filter(sociedade=sociedade)

    serializer = ProgramacaoSerializer(programacoes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def rl_lista_sociedades_prog(request):
    sociedades = [opcao[0] for opcao in Programacao.OPCOES_SOCIEDADE]
    return Response(sociedades)


class RlDiretoriasViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Diretorias"""
    queryset = Diretoria.objects.all()
    serializer_class = DiretoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sociedade']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_diretorias(request):
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
def rl_lista_sociedades(request):
    sociedades = [opcao[0] for opcao in Diretoria.OPCOES_SOCIEDADE]
    return Response(sociedades)



class RlMissionariosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Missionarios"""
    queryset = Missionario.objects.all()
    serializer_class = MissionarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_missionarios(request):
    nome = request.GET.get('nome', None)

    missionarios = Missionario.objects.all()

    if nome:
        missionarios = missionarios.filter(nome__icontains=nome)

    serializer = MissionarioSerializer(missionarios, many=True)
    return Response(serializer.data)



class RlLiderancasViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Liderancas"""
    queryset = Lideranca.objects.all()
    serializer_class = LiderancaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_liderancas(request):
    nome = request.GET.get('nome', None)
    cargo = request.GET.get('cargo', None)
    ano = request.GET.get('ano', None)
    ano_inicio = request.GET.get('ano_inicio', None)
    ano_fim = request.GET.get('ano_fim', None)

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
    if ano_inicio:
        liderancas = liderancas.filter(ano_inicio=ano_inicio)
    if ano_fim:
        liderancas = liderancas.filter(ano_fim=ano_fim)

    serializer = LiderancaSerializer(liderancas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def rl_lista_cargos(request):
    cargos = [opcao[0] for opcao in Lideranca.OPCOES_CARGO]
    return Response(cargos)

@api_view(['GET'])
def rl_lista_cargos_pastor(request):
    cargos = [opcao[0] for opcao in Pastor.OPCOES_CARGO]
    return Response(cargos)


class RlMinisteriosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Ministerios"""
    queryset = Ministerio.objects.all().order_by('-ano')
    serializer_class = MinisterioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_ministerios(request):
    nome = request.GET.get('nome', None)
    ano = request.GET.get('ano', None)

    ministerios = Ministerio.objects.all()

    if nome:
        ministerios = ministerios.filter(nome__icontains=nome)
    if ano:
        ministerios = ministerios.filter(ano=ano)

    serializer = MinisterioSerializer(ministerios, many=True)
    return Response(serializer.data)



# class RlFotosMinisteriosViewSet(viewsets.ModelViewSet):
#     """Exibindo todos os FotosMinisterios"""
#     queryset = FotosMinisterios.objects.all()
#     serializer_class = FotosMinisteriosSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['ministerio']
#     pagination_class = CustomPagination

# @api_view(['GET'])
# def rl_lista_fotosMinisterios(request):
#     ministerio = request.GET.get('ministerio', None)

#     fotosMinisterios = FotosMinisterios.objects.all()

#     if ministerio:
#         fotosMinisterios = fotosMinisterios.filter(ministerio__nome=ministerio)

#     serializer = FotosMinisteriosSerializer(fotosMinisterios, many=True)
#     return Response(serializer.data)


class RlUsuariosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuariosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['login']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_usuarios(request):
    login = request.GET.get('login', None)

    usuarios = Usuario.objects.all()

    if login:
        usuarios = usuarios.filter(login=login)

    serializer = UsuariosSerializer(usuarios, many=True)
    return Response(serializer.data)

class RlLoginView(APIView):
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




class RlPregacaoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pregacao"""
    queryset = Pregacao.objects.all().order_by('-data')
    serializer_class = PregacaoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['descricao']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_pregacoes(request):
    descricao = request.GET.get('descricao', None)

    pregacao = Pregacao.objects.all()

    if descricao:
        pregacao = pregacao.filter(descricao__icontains=descricao)

    serializer = PregacaoSerializer(pregacao, many=True)
    return Response(serializer.data)


class RlMembrosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Membross"""
    queryset = Membros.objects.all()
    serializer_class = MembrosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sociedade']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_estados_civis(request):
    estadosCivis = [opcao[0] for opcao in Membros.OPCOES_ESTADO_CIVIL]
    return Response(estadosCivis)

@api_view(['GET'])
def rl_lista_membros(request):
    nome = request.GET.get('nome', None)
    sociedade = request.GET.get('sociedade', None)
    ativo = request.GET.get('ativo', None)
    status = request.GET.get('status', None)

    membros = Membros.objects.all()

    if nome:
        membros = membros.filter(nome__icontains=nome)
    if sociedade:
        membros = membros.filter(sociedade=sociedade)
    if ativo:
        membros = membros.filter(ativo=ativo)
    if status:
        membros = membros.filter(status=status)

    serializer = MembrosSerializer(membros, many=True)
    return Response(serializer.data)

def calcular_idade(data_nascimento):
    hoje = date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    return idade

class RlEstatisticasIdade(APIView):
    def get(self, request):
        membros = Membros.objects.all()
        idade_dict = {}
        total_idade = 0
        total_membros = membros.count()

        for membro in membros:
            idade = calcular_idade(membro.data_nascimento)
            total_idade += idade
            if idade not in idade_dict:
                idade_dict[idade] = []
            idade_dict[idade].append(membro.nome)

        idade_lista = [{"name": f"Idade {key}", "value": len(value), "details": value} for key, value in sorted(idade_dict.items())]

        media_idade = round(total_idade / total_membros, 2) if total_membros > 0 else 0

        return Response({
            "idades": idade_lista,
            "media_idade": media_idade
        })

class RlEstatisticasSexo(APIView):
    def get(self, request):
        sexo_stats = Membros.objects.filter(ativo=True).values('sexo').annotate(total=Count('sexo'))
        return Response(sexo_stats)
    

class RlEstatisticasSociedade(APIView):
    def get(self, request):
        sociedade_stats = (
            Membros.objects
            .filter(ativo=True)
            .annotate(
                sociedade_label=Case(
                    When(sociedade='', then=Value('nenhuma')),
                    default='sociedade'
                )
            )
            .values('sociedade_label')
            .annotate(total=Count('sociedade'))
        )
        return Response(sociedade_stats)

class RlEstatisticasStatus(APIView):
    def get(self, request):
        status_stats = Membros.objects.filter(ativo=True).values('status').annotate(total=Count('status'))
        return Response(status_stats)

class RlEstatisticasEstadoCivil(APIView):
    def get(self, request):
        estado_civil_stats = (
            Membros.objects.filter(ativo=True)  # Filtra apenas membros ativos
            .values('estado_civil')
            .annotate(total=Count('estado_civil'))
        )
        return Response(estado_civil_stats)


@api_view(['GET'])
def rl_lista_aniversariantes(request):
    nome = request.GET.get('nome', '')
    mes = request.GET.get('mes')

    try:
        # Construir a query SQL base
        query = "SELECT * FROM vw_aniversariantes"
        params = []

        # Adicionar filtros se necessários
        where_clauses = []
        if nome:
            where_clauses.append("nome LIKE %s")
            params.append(f"%{nome}%")
        if mes:
            try:
                mes = int(mes)
                where_clauses.append("MONTH(data_nascimento) = %s")
                params.append(mes)
            except ValueError:
                return Response({"error": "O valor de 'mes' deve ser um número inteiro válido."}, status=400)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        query += " ORDER BY MONTH(data_nascimento), DAY(data_nascimento)"

        # Executar a consulta diretamente
        with connections['db_ipbregiaoleste'].cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Retornar os resultados
        return Response(results)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


class RlIgrejaViewSet(viewsets.ModelViewSet):
    queryset = Igreja.objects.all()
    serializer_class = IgrejaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


class RlEscolaDominicalViewSet(viewsets.ModelViewSet):
    """Exibindo todos os EscolaDominicals"""
    queryset = EscolaDominical.objects.all()
    serializer_class = EscolaDominicalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['classe']
    pagination_class = CustomPagination


@api_view(['GET'])
def rl_lista_escolaDominical(request):
    classe = request.GET.get('classe', None)
    escolaDominical = EscolaDominical.objects.all()

    if classe:
        escolaDominical = escolaDominical.filter(classe__icontains=classe)

    serializer = EscolaDominicalSerializer(escolaDominical, many=True)
    return Response(serializer.data)


class RlPastorViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pastor"""
    queryset = Pastor.objects.all()
    serializer_class = PastorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_pastor(request):
    nome = request.GET.get('nome', None)
    cargo = request.GET.get('cargo', None)

    pastor = Pastor.objects.all()

    if nome:
        pastor = pastor.filter(nome__icontains=nome)
    if cargo:
        pastor = pastor.filter(cargo=cargo)

    serializer = PastorSerializer(pastor, many=True)
    return Response(serializer.data)


class RlRedesSociaisViewSet(viewsets.ModelViewSet):
    """Exibindo todos os RedesSociais"""
    queryset = RedesSociais.objects.all()
    serializer_class = RedesSociaisSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['responsavel']
    pagination_class = CustomPagination

@api_view(['GET'])
def rl_lista_redeSocial(request):
    responsavel = request.GET.get('responsavel', None)
    rede_social = request.GET.get('rede_social', None)

    redeSocial = RedesSociais.objects.all()

    if responsavel:
        redeSocial = redeSocial.filter(responsavel=responsavel)
    if rede_social:
        redeSocial = redeSocial.filter(rede_social=rede_social)

    serializer = RedesSociaisSerializer(redeSocial, many=True)
    return Response(serializer.data)


class RlDownloadsViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Downloads"""
    queryset = Download.objects.all()
    serializer_class = DownloadsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


@api_view(['GET'])
def rl_lista_downloads(request):
    nome = request.GET.get('nome', None)

    download = Download.objects.all()

    if nome:
        download = download.filter(nome__icontains=nome)

    serializer = DownloadsSerializer(download, many=True)
    return Response(serializer.data)


class RlFotosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Fotos"""
    queryset = Fotos.objects.all()
    serializer_class = FotosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


@api_view(['GET'])
def rl_lista_fotos(request):
    nome = request.GET.get('nome', None)
    programacao = request.GET.get('programacao', None)

    foto = Fotos.objects.all()

    if nome:
        foto = foto.filter(nome__icontains=nome)
    if programacao:
        foto = foto.filter(programacao=programacao)

    serializer = FotosSerializer(foto, many=True)
    return Response(serializer.data)
