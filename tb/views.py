from rest_framework import viewsets, filters, status
import json
from tb.models import Contato, Cliente, Usuario, Pedido, Endereco
from tb.serializer import ContatoSerializer, ClienteSerializer, UsuarioSerializer, PedidoSerializer, EnderecoSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response

class ContatosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os contatos"""
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']


class ClientesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']


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


class PedidosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pedidos"""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario']

@api_view(['GET'])
def aj_lista_pedidos(request):
    usuario = request.GET.get('usuario', None)

    pedidos = Pedido.objects.all()

    if usuario:
        pedidos = pedidos.filter(usuario=usuario)

    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)


class EnderecosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Enderecos"""
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario']

@api_view(['GET'])
def aj_lista_enderecos(request):
    usuario = request.GET.get('usuario', None)
    id = request.GET.get('id', None)

    enderecos = Endereco.objects.all()

    if usuario:
        enderecos = enderecos.filter(usuario=usuario)
    if id:
        enderecos = enderecos.filter(id=id)

    serializer = EnderecoSerializer(enderecos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def aj_lista_endereco_principal(request):
    usuario = request.GET.get('usuario', None)
    principal = request.GET.get('principal', None)

    enderecos = Endereco.objects.all()

    if usuario:
        enderecos = enderecos.filter(usuario=usuario)

    enderecos = enderecos.filter(principal=True)

    serializer = EnderecoSerializer(enderecos, many=True)
    return Response(serializer.data)


# @csrf_exempt
# def contatoEmail(request):
#     if request.method == 'POST':
#         # Decodificar o JSON recebido
#         data = json.loads(request.body)

#         # Chamar o método send_email no modelo
#         Contato().send_email(**data)

#         # Retornar uma resposta JSON indicando sucesso
#         return JsonResponse({"mensagem": "Email enviado com sucesso"})

#     # Retornar uma resposta JSON indicando que algo deu errado
#     return JsonResponse({"mensagem": "Erro no envio do email"}, status=400)
