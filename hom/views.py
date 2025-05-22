from rest_framework import viewsets, filters, status
from django.db import connections

from hom.models import UsuarioPersonal, Perguntas, Respostas, Translation
from hom.serializer import UsuarioPersonalSerializer, PerguntasSerializer, RespostasSerializer, TranslationSerializer

from hom.models import UsuarioLoja, Endereco, Produto, Cor, Imagem, Tamanho, Categoria, CategoriaProduto, Disponibilidade
from hom.models import Favoritos, Carrinho, Pedido, ItemPedido
from hom.serializer import UsuarioLojaSerializer, EnderecoSerializer, ProdutoSerializer, CorSerializer, ImagemSerializer, TamanhoSerializer
from hom.serializer import CategoriaProdutoSerializer, CategoriaSerializer, DisponibilidadeSerializer
from hom.serializer import FavoritosSerializer, CarrinhoSerializer, PedidoSerializer, ItemPedidoSerializer
from django.http import JsonResponse

from hom.models import ItensProAcos
from hom.serializer import ItensProAcosSerializer
from django.utils import timezone

from hom.models import Discipulados, PerguntasDiscipulado, RespostasDiscipulado, UsuarioDiscipulado
from hom.models import IgrejaParceira, TurmaDiscipulado, AlunoTurmaDiscipulado
from hom.serializer import DiscipuladosSerializer, PerguntasDiscipuladoSerializer, RespostasDiscipuladoSerializer
from hom.serializer import UsuarioDiscipuladoSerializer, IgrejaParceiraSerializer, TurmaDiscipuladoSerializer, AlunoTurmaDiscipuladoSerializer

from hom.models import UsuarioSjb, Pregacao, Membros, Devocional, Igreja, Pastor
from hom.serializer import UsuarioSjbSerializer, PregacaoSerializer, MembrosSerializer, DevocionalSerializer, IgrejaSerializer, PastorSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .pagination import CustomPagination

class HomUsuariosLojaViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioLoja.objects.all()
    serializer_class = UsuarioLojaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']


@api_view(['GET'])
def hom_loja_lista_usuarios(request):
    id = request.GET.get('id', None)

    usuarios = UsuarioLoja.objects.all()

    if id:
        usuarios = usuarios.filter(id=id)

    serializer = UsuarioLojaSerializer(usuarios, many=True)
    return Response(serializer.data)

class HomLoginLojaView(APIView):
    def post(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')
        try:
            usuario = UsuarioLoja.objects.get(cpf=cpf)
            if check_password(senha, usuario.senha):  # Certifique-se de que a senha esteja hashada corretamente
                refresh = RefreshToken.for_user(usuario)
                role = 'admin' if usuario.administrador else 'user'
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': usuario.id,  # Inclua o ID do usuário na resposta
                    'nome': usuario.nome,
                    'role': role
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UsuarioLoja.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class HomEnderecosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Enderecos"""
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario']

@api_view(['GET'])
def hom_loja_lista_enderecos(request):
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

class HomProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all().order_by('descricao')
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['descricao']
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        produto = serializer.save()
        return Response({
            'id': produto.id,
            'descricao': produto.descricao
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        if id is not None:
            return Produto.objects.filter(id=id)
        return Produto.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class HomCorViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Cor"""
    queryset = Cor.objects.all()
    serializer_class = CorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['cor']
    ordering_fields = ['cor']

    def get_queryset(self):
        produto_id = self.request.query_params.get('produto_id', None)
        if produto_id is not None:
            return Cor.objects.filter(produto_id=produto_id)
        return Cor.objects.all()

class HomImagemViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Imagem"""
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['imagem']
    ordering_fields = ['imagem']

class HomCategoriaViewSet(viewsets.ModelViewSet):
    """Exibindo todos as categoria"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['categoria']
    ordering_fields = ['categoria']

class HomCategoriaProdutoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as categoria"""
    queryset = CategoriaProduto.objects.all()
    serializer_class = CategoriaProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['categoria']
    ordering_fields = ['categoria']

class HomTamanhoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Tamanho"""
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['tamanho']
    ordering_fields = ['tamanho']

    def get_queryset(self):
        produto_id = self.request.query_params.get('produto_id', None)
        if produto_id is not None:
            return Tamanho.objects.filter(produto_id=produto_id)
        return Tamanho.objects.all()

class HomDisponibilidadeViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Disponibilidade"""
    queryset = Disponibilidade.objects.all()
    serializer_class = DisponibilidadeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']


@api_view(['GET'])
def hom_lista_produtos(request):
    filtro = request.GET.get('filtro', None)

    produtos = Produto.objects.all()

    if filtro:
         produtos = produtos.filter(Q(descricao__icontains=filtro) | Q(palavras_chave__icontains=filtro))

    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)

class HomFavoritosViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Favoritos"""
    queryset = Favoritos.objects.all()
    serializer_class = FavoritosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Retorna o ID do objeto criado
        favorito_id = serializer.instance.id
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"id": favorito_id, **serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

@api_view(['GET'])
def hom_isFavorito(request):
    cliente = request.GET.get('cliente', None)
    produto = request.GET.get('produto', None)

    favorito = Favoritos.objects.all()

    if cliente:
         favorito = favorito.filter(cliente = cliente)
    if produto:
         favorito = favorito.filter(produto = produto)

    if favorito.exists():
        favorito_obj = favorito.first()  # Obtém o primeiro favorito encontrado
        return Response({'isFavorito': True, 'id': favorito_obj.id})
    else:
        return Response({'isFavorito': False, 'id': None})
    

def hom_lista_favoritos(request):
    cliente = request.GET.get('cliente', None)

    favoritos = Favoritos.objects.all()

    if cliente:
        favoritos = favoritos.filter(cliente=cliente)

    # Monta a resposta com os produtos favoritados
    produtos = []
    for favorito in favoritos:
        produto = favorito.produto
        cores = Cor.objects.filter(produto=produto)
        imagens = Imagem.objects.filter(produto=produto)

        produtos.append({
            "id": produto.id,
            "descricao": produto.descricao,
            "valor": produto.valor,
            "cores": [
                {
                    "id": cor.id,
                    "cor": cor.cor,
                    "inicial": cor.inicial,
                    "imagens": ImagemSerializer(imagens.filter(cor=cor), many=True).data
                }
                for cor in cores
            ]
        })

    return JsonResponse(produtos, safe=False)

class HomCarrinhoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Carrinho"""
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']

def hom_lista_carrinho(request):
    cliente = request.GET.get('cliente', None)

    carrinhos = Carrinho.objects.all()

    if cliente:
        carrinhos = carrinhos.filter(cliente=cliente)

    # Monta a resposta com os produtos no carrinho
    produtos = []
    for item in carrinhos:
        produto = item.produto
        cores = Cor.objects.filter(produto=produto)
        imagens = Imagem.objects.filter(produto=produto)

        produtos.append({
            "id": item.id,
            "produto_id": produto.id,
            "descricao": produto.descricao,
            "valor": produto.valor,
            "cor_selecionada": {
                "cor_id": item.cor.id,
                "cor": item.cor.cor,
                "inicial": item.cor.inicial,
                "imagens": ImagemSerializer(imagens.filter(cor=item.cor), many=True).data,
            },
            "tamanho_selecionado": {
                "id": item.tamanho.id,
                "tamanho": item.tamanho.tamanho,
            },
            "quantidade": item.quantidade,
        })

    return JsonResponse(produtos, safe=False)

class HomPedidoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Pedido"""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Retorna o ID do objeto criado
        pedido_id = serializer.instance.id
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"id": pedido_id, **serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

class HomItemPedidoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as ItemPedido"""
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['produto']
    ordering_fields = ['produto']

@api_view(['GET'])
def hom_lista_pedidos(request):
    cliente = request.GET.get('cliente')

    if not cliente:
        return Response({'error': 'Parâmetro "cliente" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pedido = Pedido.objects.filter(cliente=cliente)
    except ValueError:
        return Response({'error': 'Parâmetro "pedido" inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PedidoSerializer(pedido, many=True)
    return Response(serializer.data)

# ---------------------------------PERSONAL---------------------------------------------------------


class HomUsuariosPersonalViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioPersonal.objects.all().order_by('nome')
    serializer_class = UsuarioPersonalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

class HomUsuariosPersonalClientesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioPersonal.objects.filter(cliente=True, administrador=False).order_by('nome')
    serializer_class = UsuarioPersonalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


@api_view(['GET'])
def hom_lista_usuarios_personal(request):
    nome = request.GET.get('nome', None)
    cliente = request.GET.get('cliente', None)
    administrador = request.GET.get('adm', None)

    usuarios = UsuarioPersonal.objects.all()

    if nome:
        usuarios = usuarios.filter(nome=nome)
    if cliente:
        usuarios = usuarios.filter(cliente=cliente)
    if administrador:
        usuarios = usuarios.filter(administrador=administrador)

    serializer = UsuarioPersonalSerializer(usuarios, many=True)
    return Response(serializer.data)


class HomLoginPersonalView(APIView):
    def post(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')
        try:
            usuario = UsuarioPersonal.objects.get(cpf=cpf)
            if check_password(senha, usuario.senha):  # Certifique-se de que a senha esteja hashada corretamente
                refresh = RefreshToken.for_user(usuario)
                role = 'admin' if usuario.administrador else 'user'
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': usuario.id,  # Inclua o ID do usuário na resposta
                    'nome': usuario.nome,
                    'role': role
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UsuarioPersonal.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class HomPerguntasViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Perguntas"""
    queryset = Perguntas.objects.all()
    serializer_class = PerguntasSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['pergunta']
    pagination_class = CustomPagination


@api_view(['GET'])
def hom_lista_perguntas(request):
    pergunta = request.GET.get('pergunta', None)

    perguntas = Perguntas.objects.all()

    if pergunta:
        perguntas = perguntas.filter(pergunta__icontains=pergunta)

    serializer = PerguntasSerializer(perguntas, many=True)
    return Response(serializer.data)


class HomRespostasViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Respostas"""
    queryset = Respostas.objects.all()
    serializer_class = RespostasSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['resposta']
    pagination_class = CustomPagination



@api_view(['GET'])
def hom_lista_respostas(request):
    resposta = request.GET.get('resposta', None)
    usuario = request.GET.get('usuario', None)

    respostas = Respostas.objects.all()

    if resposta:
        respostas = respostas.filter(resposta__icontains=resposta)
    if usuario:
        respostas = respostas.filter(usuario=usuario)

    serializer = RespostasSerializer(respostas, many=True)
    return Response(serializer.data)


class HomTranslationViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Translation"""
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['resposta']
    pagination_class = CustomPagination


class HomTranslationView(APIView):
    def get(self, request, lang="pt"):  # Padrão para português
        if lang not in ['pt', 'en', 'es']:  
            return Response({"error": "Idioma não suportado"}, status=400)

        translations = Translation.objects.all()
        return Response({t.key: getattr(t, lang) for t in translations})
# ---------------------------------PRO ACOS---------------------------------------------------------

class ItensProAcosViewSet(viewsets.ModelViewSet):
    """Exibindo todos as programacoes"""
    queryset = ItensProAcos.objects.all()
    serializer_class = ItensProAcosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['item','quant', 'datalote','datavenda']
    ordering_fields = ['id']
    pagination_class = CustomPagination


@api_view(['GET'])
def lista_itens_proacos(request):
    datalote = request.GET.get('datalote', None)
    datavenda = request.GET.get('datavenda', None)
    item = request.GET.get('item', None)

    itensProAcos = ItensProAcos.objects.all()

    datalote_date = timezone.datetime.strptime(datalote, '%Y-%m-%d').date()
    datavenda_date = timezone.datetime.strptime(datavenda, '%Y-%m-%d').date()

    # Filtra itens onde datalote está entre datalote e datavenda
    itensProAcos = itensProAcos.filter(datalote__gte=datalote_date, datalote__lte=datavenda_date)

    if item:
        itensProAcos = itensProAcos.filter(Q(item__icontains=item))

    serializer = ItensProAcosSerializer(itensProAcos, many=True)
    return Response(serializer.data)

# ---------------------------------DISCIPULADO---------------------------------------------------------
class HomLoginDiscipuladoView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        senha = request.data.get('senha')

        try:
            usuario = UsuarioDiscipulado.objects.get(email=email)
            if check_password(senha, usuario.senha):  
                refresh = RefreshToken.for_user(usuario)

                if usuario.administrador:
                    role = 'admin'
                elif usuario.discipulador:
                    role = 'discipulador'
                else:
                    role = 'discipulo'

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'role': role
                })

            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UsuarioDiscipulado.DoesNotExist:
                    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

class HomIgrejasParceirasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as Igrejas Parceiras"""
    queryset = IgrejaParceira.objects.all().order_by('nome')
    serializer_class = IgrejaParceiraSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


@api_view(['GET'])
def hom_lista_igrejas(request):
    nome = request.GET.get('nome', None)
    igrejas = IgrejaParceira.objects.all().order_by('nome')

    if nome:
        igrejas = igrejas.filter(nome__icontains=nome)

    serializer = IgrejaParceiraSerializer(igrejas, many=True)
    return Response(serializer.data)


class HomUsuarioDiscipuladoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Discipuladores"""
    queryset = UsuarioDiscipulado.objects.all().order_by('nome')
    serializer_class = UsuarioDiscipuladoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination


class HomTurmaDiscipuladoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Discipuladores"""
    queryset = TurmaDiscipulado.objects.all()
    serializer_class = TurmaDiscipuladoSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination


@api_view(['GET'])
def hom_lista_turma_discipulados(request):
    nome = request.GET.get('nome', None)
    discipulador = request.GET.get('discipulador', None)

    discipulados = TurmaDiscipulado.objects.all()

    if nome:
        discipulados = discipulados.filter(nome_turma__icontains=nome)
    if discipulador:
        discipulados = discipulados.filter(discipulador=discipulador)

    serializer = TurmaDiscipuladoSerializer(discipulados, many=True)
    return Response(serializer.data)


class HomAlunoTurmaDiscipuladoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Discipuladores"""
    queryset = AlunoTurmaDiscipulado.objects.all()
    serializer_class = AlunoTurmaDiscipuladoSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination

    @action(detail=False, methods=['delete'], url_path='remover_alunos_turma/(?P<turma_id>[^/.]+)')
    def remover_alunos_da_turma(self, request, turma_id=None):
        alunos_removidos, _ = AlunoTurmaDiscipulado.objects.filter(turma_id=turma_id).delete()
        return Response(
            {"mensagem": f"{alunos_removidos} alunos removidos da turma {turma_id}."},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def hom_lista_aluno_discipulados(request):
    discipulo_id = request.GET.get('discipulo', None)

    if not discipulo_id:
        return Response({'erro': 'Parâmetro "discipulo" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        aluno_turmas = AlunoTurmaDiscipulado.objects.select_related('turma__discipulado').filter(discipulo_id=discipulo_id)
        
        resultado = []
        for aluno in aluno_turmas:
            turma = aluno.turma
            discipulado = turma.discipulado
            resultado.append({
                'turma': {
                    'id': turma.id,
                    'nome_turma': turma.nome_turma,
                    'nome_discipulador': turma.discipulador.nome,
                    'id_discipulador': turma.discipulador.id,
                    'data_inicio': turma.data_inicio,
                    'data_fim': turma.data_fim,
                },
                'discipulado': {
                    'id': discipulado.id,
                    'nome': discipulado.nome,
                    'licao': discipulado.licao,
                    'nivel': discipulado.nivel,
                    'proximoEstudo': discipulado.proximoEstudo,
                    'foto': discipulado.foto.url if discipulado.foto else None,
                }
            })

        return Response(resultado, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'erro': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HomDiscipuladosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Discipulados"""
    queryset = Discipulados.objects.all().order_by('nome')
    serializer_class = DiscipuladosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def hom_lista_discipulados(request):
    nome = request.GET.get('nome', None)
    nivel = request.GET.get('nivel', None)

    discipulados = Discipulados.objects.all()

    if nome:
        discipulados = discipulados.filter(nome__icontains=nome)
    if nivel:
        discipulados = discipulados.filter(nivel=nivel)

    serializer = DiscipuladosSerializer(discipulados, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def hom_lista_usuario_discipulado(request):
    nome = request.GET.get('nome', None)
    cliente = request.GET.get('cliente', None)
    discipulador = request.GET.get('discipulador', None)

    usuario = UsuarioDiscipulado.objects.all()

    if nome:
        usuario = usuario.filter(nome__icontains=nome)
    if cliente:
        usuario = usuario.filter(cliente=cliente)
    if discipulador:
        usuario = usuario.filter(discipulador=discipulador)

    serializer = UsuarioDiscipuladoSerializer(usuario, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def hom_lista_niveis_discipulo(request):
    niveis = [opcao[0] for opcao in UsuarioDiscipulado.NIVEIS]
    return Response(niveis)


class HomPerguntasDiscipuladoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as PerguntasDiscipulado"""
    queryset = PerguntasDiscipulado.objects.all()
    serializer_class = PerguntasDiscipuladoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['pergunta']
    pagination_class = CustomPagination


@api_view(['GET'])
def hom_lista_perguntas_discipulado(request):
    pergunta = request.GET.get('pergunta', None)
    discipulado = request.GET.get('discipulado', None)

    perguntas = PerguntasDiscipulado.objects.all()

    if pergunta:
        perguntas = perguntas.filter(pergunta__icontains=pergunta)
    if discipulado:
        perguntas = perguntas.filter(discipulado=discipulado)

    serializer = PerguntasDiscipuladoSerializer(perguntas, many=True)
    return Response(serializer.data)


class HomRespostasDiscipuladoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as RespostasDiscipulado"""
    queryset = RespostasDiscipulado.objects.all()
    serializer_class = RespostasDiscipuladoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['resposta']
    pagination_class = CustomPagination



@api_view(['GET'])
def hom_lista_respostas_discipulado(request):
    resposta = request.GET.get('resposta', None)
    usuario = request.GET.get('usuario', None)
    turma = request.GET.get('turma', None)

    respostas = RespostasDiscipulado.objects.all()

    if resposta:
        respostas = respostas.filter(resposta__icontains=resposta)
    if usuario:
        respostas = respostas.filter(usuario=usuario)
    if turma:
        respostas = respostas.filter(turma=turma)

    serializer = RespostasDiscipuladoSerializer(respostas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hom_verificar_resposta(request):
    usuario = request.GET.get('usuario')
    turma = request.GET.get('turma')
    pergunta = request.GET.get('pergunta')

    try:
        resposta = RespostasDiscipulado.objects.get(usuario=usuario, turma=turma, pergunta=pergunta)
        serializer = RespostasDiscipuladoSerializer(resposta)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except RespostasDiscipulado.DoesNotExist:
        return Response(None, status=status.HTTP_200_OK)



# ---------------------------------PIB São João Betim---------------------------------------------------------


class SjbUsuariosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Usuarios"""
    queryset = UsuarioSjb.objects.all()
    serializer_class = UsuarioSjbSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['login']
    pagination_class = CustomPagination

@api_view(['GET'])
def sjb_lista_usuarios(request):
    login = request.GET.get('login', None)

    usuarios = UsuarioSjb.objects.all()

    if login:
        usuarios = usuarios.filter(login=login)

    serializer = UsuarioSjbSerializer(usuarios, many=True)
    return Response(serializer.data)

class SjbLoginView(APIView):
    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        senha = request.data.get('senha')
        try:
            usuario = UsuarioSjb.objects.get(login=login)
            if check_password(senha, usuario.senha):  # Certifique-se de que a senha esteja hashada corretamente
                refresh = RefreshToken.for_user(usuario)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UsuarioSjb.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)




class SjbPregacaoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pregacao"""
    queryset = Pregacao.objects.all().order_by('-data')
    serializer_class = PregacaoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['descricao']
    pagination_class = CustomPagination

@api_view(['GET'])
def sjb_lista_pregacoes(request):
    descricao = request.GET.get('descricao', None)

    pregacao = Pregacao.objects.all()

    if descricao:
        pregacao = pregacao.filter(descricao__icontains=descricao)

    serializer = PregacaoSerializer(pregacao, many=True)
    return Response(serializer.data)


class SjbMembrosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Membross"""
    queryset = Membros.objects.all()
    serializer_class = MembrosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sociedade']
    pagination_class = CustomPagination

@api_view(['GET'])
def sjb_lista_membros(request):
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


@api_view(['GET'])
def sjb_lista_aniversariantes(request):
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
        with connections['db_homol'].cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Retornar os resultados
        return Response(results)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


class SjbIgrejaViewSet(viewsets.ModelViewSet):
    queryset = Igreja.objects.all()
    serializer_class = IgrejaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

   
class SjbPastorViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pastor"""
    queryset = Pastor.objects.all()
    serializer_class = PastorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def sjb_lista_pastor(request):
    nome = request.GET.get('nome', None)
    cargo = request.GET.get('cargo', None)

    pastor = Pastor.objects.all()

    if nome:
        pastor = pastor.filter(nome__icontains=nome)
    if cargo:
        pastor = pastor.filter(cargo=cargo)

    serializer = PastorSerializer(pastor, many=True)
    return Response(serializer.data)


   
class SjbPastorViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Pastor"""
    queryset = Pastor.objects.all()
    serializer_class = PastorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def sjb_lista_pastor(request):
    nome = request.GET.get('nome', None)
    cargo = request.GET.get('cargo', None)

    pastor = Pastor.objects.all()

    if nome:
        pastor = pastor.filter(nome__icontains=nome)
    if cargo:
        pastor = pastor.filter(cargo=cargo)

    serializer = PastorSerializer(pastor, many=True)
    return Response(serializer.data)


   
class SjbDevocionalViewSet(viewsets.ModelViewSet):
    """Exibindo todos os Devocional"""
    queryset = Devocional.objects.all().order_by('-data')
    serializer_class = DevocionalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    pagination_class = CustomPagination

@api_view(['GET'])
def sjb_lista_devocional(request):
    nome = request.GET.get('nome', None)
    cargo = request.GET.get('cargo', None)

    devocional = Devocional.objects.all()

    if nome:
        devocional = devocional.filter(nome__icontains=nome)
    if cargo:
        devocional = devocional.filter(cargo=cargo)

    serializer = DevocionalSerializer(devocional, many=True)
    return Response(serializer.data)
