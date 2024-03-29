from rest_framework import viewsets, filters
from contatos.models import Contato, Pensamento
from contatos.serializer import ContatoSerializer, PensamentoSerializer

class ContatosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os contatos"""
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

class PensamentosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pensamentos"""
    queryset = Pensamento.objects.all()
    serializer_class = PensamentoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['conteudo']
    filterset_fields = ['favorito']

