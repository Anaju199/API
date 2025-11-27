from rest_framework import viewsets, filters, status
import json
import requests
from tb.models import Cliente, Usuario, Item, Pedido, Endereco, Avaliacoes, Demanda, MensagemDemanda, UsuarioCliente
from tb.serializer import ClienteSerializer, UsuarioSerializer, ItemSerializer, PedidoSerializer, EnderecoSerializer, AvaliacoesSerializer, DemandaSerializer, MensagemDemandaSerializer, UsuarioClienteSerializer
from tb.models import FotosAmor
from tb.serializer import FotosAmorSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from .pagination import CustomPagination
from django.middleware.csrf import get_token

# class ContatosViewSet(viewsets.ModelViewSet):
#     """Exibindo todos os contatos"""
#     queryset = Contato.objects.all()
#     serializer_class = ContatoSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['nome']
#     pagination_class = CustomPagination


class ClientesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']
    pagination_class = CustomPagination


@api_view(['GET'])
def aj_lista_clientes(request):
    nome = request.GET.get('nome', None)

    clientes = Cliente.objects.all()

    if nome:
        clientes = clientes.filter(~Q(nome__icontains=nome))

    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)    


@api_view(['GET'])
def aj_lista_layouts(request):
    nome = request.GET.get('nome', None)

    clientes = Cliente.objects.all()

    if nome:
        clientes = clientes.filter(Q(nome__icontains=nome))

    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)    

class AvaliacoesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Avaliacaos"""
    queryset = Avaliacoes.objects.all()
    serializer_class = AvaliacoesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def aj_lista_avaliacoes(request):
    nome = request.GET.get('nome', None)

    avaliacoes = Avaliacoes.objects.all()

    if nome:
        avaliacoes = avaliacoes.filter(Q(nome__icontains=nome))

    serializer = AvaliacoesSerializer(avaliacoes, many=True)
    return Response(serializer.data)    

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


class ItensViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Itens"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario']

@api_view(['GET'])
def aj_lista_itens(request):
    usuario = request.GET.get('usuario', None)

    itens = Item.objects.all()

    if usuario:
        itens = itens.filter(usuario=usuario)

    serializer = ItemSerializer(itens, many=True)
    return Response(serializer.data)

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
    principal = request.GET.get('principal', None)

    enderecos = Endereco.objects.all()

    if usuario:
        enderecos = enderecos.filter(usuario=usuario)
    if id:
        enderecos = enderecos.filter(id=id)
    if principal:
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

@ensure_csrf_cookie
def create_payload(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Fazendo a requisição POST para outra API
            external_api_url = 'https://sandbox.api.pagseguro.com/orders'
            headers = {
                'Authorization': request.headers.get('Authorization'),
                'Accept': request.headers.get('Accept'),
                'Content-Type': request.headers.get('Content-Type')
            }
            response = requests.post(external_api_url, data=json.dumps(data), headers=headers)

            # Processar a resposta da outra API conforme necessário
            if response.status_code == 200 or response.status_code == 201:
                external_data = response.json()
                return JsonResponse({
                    'status_code': response.status_code,
                    'response': external_data
                }, status=response.status_code)
            else:
                try:
                    error_response = response.json()  # Tenta extrair o JSON do erro
                except ValueError:
                    error_response = response.text  # Caso o conteúdo não seja JSON

                return JsonResponse({
                    'error': 'Failed to forward data',
                    'status_code': response.status_code,
                    'response': error_response
                }, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON', 'details': str(e)}, status=400)

        except requests.RequestException as e:
            print(f"Error making external request: {e}")
            return JsonResponse({'error': f'Failed to forward data: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@ensure_csrf_cookie
def get_csrf_token(request):
    # garante que o cookie csrftoken será enviado no response
    return JsonResponse({"csrfToken": get_token(request)})

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})

@ensure_csrf_cookie
def criar_chavePublica(request):
    if request.method == 'POST':
        try:
            url = "https://sandbox.api.pagseguro.com/public-keys"
            payload = { "type": "card" }
            headers = {
                'Authorization': request.headers.get('Authorization'),
                'Accept': request.headers.get('Accept'),
                'Content-Type': request.headers.get('Content-Type')
            }

            # Fazendo a requisição POST
            response = requests.post(url, json=payload, headers=headers)
            
            # Verificando se a resposta foi bem-sucedida
            if response.status_code in [200, 201]:
                # Convertendo a resposta para JSON
                data = response.json()
                
                # Obtendo a chave gerada (ajuste conforme o nome correto da chave na resposta)
                public_key = data.get("public_key")
                
                if public_key:
                    return JsonResponse({'publicKey': public_key}, status=response.status_code)
                else:
                    return JsonResponse({'error': 'Public key not found in response'}, status=500)
            else:
                return JsonResponse({'error': 'Failed to create public key', 'details': response.text}, status=response.status_code)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON', 'details': str(e)}, status=400)

        except requests.RequestException as e:
            print(f"Error making external request: {e}")
            return JsonResponse({'error': f'Failed to forward data: {str(e)}'}, status=500)

class DemandaViewSet(viewsets.ModelViewSet):
    queryset = Demanda.objects.all()
    serializer_class = DemandaSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def get_queryset(self):
        queryset = Demanda.objects.all()
        usuario = self.request.query_params.get('usuario', None)
        cliente_id = self.request.query_params.get('cliente_id', None)
        status = self.request.query_params.get('status', None)
        only_my_clients = self.request.query_params.get('only_my_clients', False)

        if usuario:
            if only_my_clients == 'true':
                # Get all clients associated with this user through the UsuarioCliente relationship
                user_clients = Cliente.objects.filter(usuariocliente__usuario_id=usuario).values_list('id', flat=True)
                queryset = queryset.filter(cliente_id__in=user_clients)
            else:
                queryset = queryset.filter(usuario=usuario)
        
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    @action(detail=False, methods=['get'])
    def my_clients_demands(self, request):
        usuario = request.query_params.get('usuario', None)
        if not usuario:
            return Response({'error': 'Usuario parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Get all clients associated with this user through the UsuarioCliente relationship
        user_clients = Cliente.objects.filter(usuariocliente__usuario_id=usuario).values_list('id', flat=True)
        # Get all demands for these clients
        queryset = self.get_queryset().filter(cliente_id__in=user_clients)
        
        # Apply status filter if provided
        status_param = request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MensagemDemandaViewSet(viewsets.ModelViewSet):
    queryset = MensagemDemanda.objects.all()
    serializer_class = MensagemDemandaSerializer

    def get_queryset(self):
        demanda = self.request.query_params.get('demanda', None)
        if demanda:
            return MensagemDemanda.objects.filter(demanda=demanda)
        return MensagemDemanda.objects.all()

    def create(self, request, *args, **kwargs):
        demanda = request.data.get('demanda')
        if not demanda:
            return Response(
                {'error': 'demanda is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            demanda = Demanda.objects.get(id=demanda)
        except Demanda.DoesNotExist:
            return Response(
                {'error': 'Demanda not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(demanda=demanda)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UsuarioClienteViewSet(viewsets.ModelViewSet):
    queryset = UsuarioCliente.objects.all()
    serializer_class = UsuarioClienteSerializer

    def get_queryset(self):
        queryset = UsuarioCliente.objects.all()
        usuario = self.request.query_params.get('usuario', None)
        cliente = self.request.query_params.get('cliente', None)

        if usuario:
            queryset = queryset.filter(usuario_id=usuario)
        if cliente:
            queryset = queryset.filter(cliente_id=cliente)

        return queryset

    @action(detail=False, methods=['get'])
    def my_clients(self, request):
        usuario = request.query_params.get('usuario', None)
        if not usuario:
            return Response({'error': 'Usuario parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user_clients = Cliente.objects.filter(usuariocliente__usuario_id=usuario)
        serializer = ClienteSerializer(user_clients, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def aj_lista_meus_clientes(request):
    usuario = request.GET.get('usuario', None)
    is_admin = request.GET.get('is_admin', None)

    if not usuario:
        return Response({'error': 'Usuario parameter is required'}, 
                      status=status.HTTP_400_BAD_REQUEST)

    # Get all clients associated with this user through UsuarioCliente
    clientes = Cliente.objects.filter(usuariocliente__usuario_id=usuario)

    # Filter by is_admin if specified
    if is_admin is not None:
        is_admin_bool = is_admin.lower() == 'true'
        clientes = clientes.filter(usuariocliente__is_admin=is_admin_bool)

    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)




class FotosAmorViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Fotos"""
    queryset = FotosAmor.objects.all()
    serializer_class = FotosAmorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        capa = self.request.query_params.get('capa')

        if capa is not None:
            # Se vier "true", filtra capa=True
            if capa.lower() in ['true', '1', 't', 'yes']:
                queryset = queryset.filter(capa=True)
            # Se vier "false", filtra capa=False
            elif capa.lower() in ['false', '0', 'f', 'no']:
                queryset = queryset.filter(capa=False)

        return queryset

