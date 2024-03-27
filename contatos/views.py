from rest_framework import viewsets
from contatos.models import Contato, Pensamento
from contatos.serializer import ContatoSerializer, PensamentoSerializer

class ContatosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os contatos"""
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer

class PensamentosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pensamentos"""
    queryset = Pensamento.objects.all()
    serializer_class = PensamentoSerializer

