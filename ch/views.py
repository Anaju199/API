from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .pagination import CustomPagination
import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie



from ch.models import UsuarioCasaRohr, Fotos, Catalogos, Categorias
from ch.serializer import UsuarioCasaRohrSerializer, FotosSerializer, CatalogosSerializer, CategoriasSerializer

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
        
        
class ChCategoriasViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['descricao']
    ordering_fields = ['id']
    pagination_class = CustomPagination
        
@api_view(['GET'])
def ch_lista_categorias(request):
    categoria = request.GET.get('categoria', None)

    categorias = Categorias.objects.all()

    if categoria:
        categorias = categorias.filter(categoria=categoria)

    serializer = CategoriasSerializer(categorias, many=True)
    return Response(serializer.data)

        
class ChFotosViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = Fotos.objects.all()
    serializer_class = FotosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['descricao']
    ordering_fields = ['id']
    pagination_class = CustomPagination


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




import smtplib
from email.message import EmailMessage


@ensure_csrf_cookie
def ch_envia_email(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"error": f"Erro ao ler JSON: {str(e)}"}, status=400)

    nome = data.get("nome")
    email = data.get("email")
    cargoInteressado = data.get("cargoInteressado", "")
    email_destinatario = data.get("destinatario")
    assunto = data.get("assunto", "Sem assunto")
    mensagem = data.get("mensagem", "")

    if not email_destinatario:
        return JsonResponse({"error": "O campo 'destinatario' é obrigatório"}, status=400)

    # 🔹 Configurações fixas do remetente
    email_remetente = email_destinatario
    senha = "Expresso514#"   # ⚠️ Melhor usar variável de ambiente depois!

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = email_remetente
    msg['To'] = email_destinatario
   
    corpo = f"""
        Você recebeu uma nova mensagem do site da Casa Rohr
        Através de https://casarohr.com.br/

        Nome: {nome}
        E-mail: {email}
        """

    if cargoInteressado:  # só adiciona se não estiver vazio / None
        corpo += f"\n       Cargo de Interesse: {cargoInteressado}\n"

    corpo += f"""
    Mensagem:
    {mensagem}
    """


    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.titan.email", 465) as server:
            server.login(email_remetente, senha)
            server.send_message(msg)
        return JsonResponse({"success": "✅ E-mail enviado com sucesso!"})
    except smtplib.SMTPAuthenticationError:
        return JsonResponse({"error": "Falha na autenticação. Verifique usuário e senha."}, status=401)
    except smtplib.SMTPConnectError:
        return JsonResponse({"error": "Falha na conexão com o servidor SMTP."}, status=500)
    except smtplib.SMTPException as e:
        return JsonResponse({"error": f"Erro SMTP: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": f"Erro inesperado: {str(e)}"}, status=500)