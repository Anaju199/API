from rest_framework import viewsets, filters
import json
from rl.models import Programacao, Diretoria, Ministerio, Missionario, Lideranca, FotosMinisterios, Usuario
from rl.serializer import ProgramacaoSerializer, DiretoriaSerializer, MinisterioSerializer, MissionarioSerializer, LiderancaSerializer, FotosMinisteriosSerializer, UsuariosSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

class ProgramacoesViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = Programacao.objects.all()
    serializer_class = ProgramacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['mes','ano','descricao','sociedade']
    # filterset_fields = ['sociedade']
    ordering_fields = ['dia','mes']

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

@api_view(['GET'])
def lista_usuarios(request):
    login = request.GET.get('login', None)

    usuarios = Usuario.objects.all()

    if login:
        usuarios = usuarios.filter(login=login)

    serializer = UsuariosSerializer(usuarios, many=True)
    return Response(serializer.data)
