from django.contrib import admin
from django.urls import path, include
from tb.views import aj_lista_itens, aj_lista_pedidos, aj_lista_usuarios, aj_lista_enderecos, aj_lista_endereco_principal, create_payload, get_csrf_token
from tb.views import ContatosViewSet, ClientesViewSet, AJUsuariosViewSet, AJLoginView, ItensViewSet, PedidosViewSet, EnderecosViewSet
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static
from rl.views import rl_lista_programacoes, rl_lista_diretorias, rl_lista_ministerios, rl_lista_missionarios, rl_lista_liderancas
from rl.views import rl_lista_fotosMinisterios, rl_lista_sociedades, rl_lista_cargos, rl_lista_sociedades_prog, rl_lista_usuarios
from rl.views import rl_lista_pregacoes, rl_lista_membros, rl_lista_aniversariantes, rl_lista_cargos_pastor, rl_lista_pastor
from rl.views import rl_lista_escolaDominical, rl_lista_redeSocial, rl_lista_downloads
from rl.views import RlProgramacoesViewSet, RlDiretoriasViewSet, RlMinisteriosViewSet, RlMissionariosViewSet, RlLiderancasViewSet
from rl.views import RlFotosMinisteriosViewSet, RlUsuariosViewSet, RlLoginView, RlPregacaoViewSet, RlMembrosViewSet, RlIgrejaViewSet
from rl.views import RlEscolaDominicalViewSet, RlPastorViewSet, RlRedesSociaisViewSet, RlDownloadsViewSet

from hom.views import ItensProAcosViewSet, lista_itens_proacos

from hom.views import lista_produtos, LoginLojaView
from hom.views import ProdutoViewSet, CorViewSet, ImagemViewSet, TamanhoViewSet, CategoriaViewSet, CategoriaProdutoViewSet
from hom.views import DisponibilidadeViewSet, UsuariosLojaViewSet, FavoritosViewSet, CarrinhoViewSet, PedidoViewSet, ItemPedidoViewSet

from hom.views import lista_usuarios_personal, lista_perguntas, lista_respostas, LoginPersonalView
from hom.views import UsuariosPersonalViewSet, UsuariosPersonalClientesViewSet, PerguntasViewSet, RespostasViewSet

router = routers.DefaultRouter()
router.register('contatos', ContatosViewSet, basename='Contatos')
router.register('clientes', ClientesViewSet, basename='Clientes')
router.register('aj_usuarios', AJUsuariosViewSet, basename='aj_Usuarios')
router.register('aj_itens', ItensViewSet, basename='aj_itens')
router.register('aj_pedidos', PedidosViewSet, basename='aj_Pedidos')
router.register('aj_usuarios_enderecos', EnderecosViewSet, basename='aj_usuarios_enderecos')

# ---------------------------------PERSONAL---------------------------------------------------------
router.register('usuarios_personal', UsuariosPersonalViewSet, basename='usuarios_personal')
router.register('usuarios_personal_clientes', UsuariosPersonalClientesViewSet, basename='usuarios_personal_clientes')
router.register('perguntas', PerguntasViewSet, basename='Perguntas')
router.register('respostas', RespostasViewSet, basename='Respostas')

# ---------------------------------IGREJA---------------------------------------------------------
router.register('rl_programacoes', RlProgramacoesViewSet, basename='Programacoes')
router.register('rl_diretorias', RlDiretoriasViewSet, basename='Diretorias')
router.register('rl_ministerios', RlMinisteriosViewSet, basename='Ministerios')
router.register('rl_missionarios', RlMissionariosViewSet, basename='Missionarios')
router.register('rl_liderancas', RlLiderancasViewSet, basename='Liderancas')
router.register('rl_fotosMinisterios', RlFotosMinisteriosViewSet, basename='FotosMinisterios')
router.register('rl_usuarios', RlUsuariosViewSet, basename='Usuarios')
router.register('rl_pregacoes', RlPregacaoViewSet, basename='Pregacoes')
router.register('rl_membros', RlMembrosViewSet, basename='Membros')
router.register('rl_igreja', RlIgrejaViewSet, basename='Igreja')
router.register('rl_escolaDominical', RlEscolaDominicalViewSet, basename='EscolaDominical')
router.register('rl_pastor', RlPastorViewSet, basename='Pastor')
router.register('rl_redesSociais', RlRedesSociaisViewSet, basename='redesSociais')
router.register('rl_downloads', RlDownloadsViewSet, basename='downloads')


# ---------------------------------LOJA---------------------------------------------------------
router.register('loja_usuarios', UsuariosLojaViewSet, basename='loja_Usuarios')
router.register('produto', ProdutoViewSet, basename='produto')
router.register('imagem', ImagemViewSet, basename='imagem')
router.register('tamanho', TamanhoViewSet, basename='tamanho')
router.register('disponibilidade', DisponibilidadeViewSet, basename='disponibilidade')
router.register('cor', CorViewSet, basename='cor')
router.register('categoria', CategoriaViewSet, basename='categoria')
router.register('categoria_produto', CategoriaProdutoViewSet, basename='categoria_produto')
router.register('favorito', FavoritosViewSet, basename='favorito')
router.register('carrinho', CarrinhoViewSet, basename='carrinho')
router.register('pedido', PedidoViewSet, basename='pedido')
router.register('itemPedido', ItemPedidoViewSet, basename='itemPedido')

# ---------------------------------PROACOS---------------------------------------------------------
router.register('item_proacos', ItensProAcosViewSet, basename='item_proacos')

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('controle-admin/', admin.site.urls),
    path('', include(router.urls)),
    path('aj_login/', AJLoginView.as_view(), name='aj_login'),
    path('aj_lista_itens/', aj_lista_itens, name='aj_lista_itens'),
    path('aj_lista_pedidos/', aj_lista_pedidos, name='aj_lista_pedidos'),
    path('aj_lista_usuarios/', aj_lista_usuarios, name='aj_lista_usuarios'),
    path('aj_lista_enderecos/', aj_lista_enderecos, name='aj_lista_enderecos'),
    path('aj_lista_endereco_principal/', aj_lista_endereco_principal, name='aj_lista_endereco_principal'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('api/create/', create_payload, name='create_payload'),
    # path('contatoEmail', contatoEmail),

    path('rl_lista_programacoes/', rl_lista_programacoes),
    path('rl_lista_diretorias/', rl_lista_diretorias),
    path('rl_lista_ministerios/', rl_lista_ministerios),
    path('rl_lista_missionarios/', rl_lista_missionarios),
    path('rl_lista_liderancas/', rl_lista_liderancas),
    path('rl_lista_fotosMinisterios/', rl_lista_fotosMinisterios),
    path('rl_lista_sociedades/', rl_lista_sociedades),
    path('rl_lista_cargos/', rl_lista_cargos),
    path('rl_lista_cargos_pastor/', rl_lista_cargos_pastor),
    path('rl_lista_pastor/', rl_lista_pastor),
    path('rl_lista_sociedades_prog/', rl_lista_sociedades_prog),
    path('rl_lista_usuarios/', rl_lista_usuarios),
    path('rl_lista_pregacoes/', rl_lista_pregacoes),
    path('rl_lista_membros/', rl_lista_membros),
    path('rl_lista_aniversariantes/', rl_lista_aniversariantes),
    path('rl_lista_redeSocial/', rl_lista_redeSocial),
    path('rl_lista_escolaDominical/', rl_lista_escolaDominical),
    path('rl_lista_downloads/', rl_lista_downloads),
    path('rl_login/', RlLoginView.as_view(), name='rl_login'),

# ---------------------------------Loja---------------------------------------------------------
    path('lista_produtos/', lista_produtos),
    path('login_loja/', LoginLojaView.as_view(), name='login_loja'),

# ---------------------------------PERSONAL---------------------------------------------------------
    path('lista_usuarios_personal/', lista_usuarios_personal),
    path('lista_perguntas/', lista_perguntas),
    path('lista_respostas/', lista_respostas),
    path('login_personal/', LoginPersonalView.as_view(), name='login_personal'),


# ---------------------------------PRO AÇOS---------------------------------------------------------
    path('lista_itens_proacos/', lista_itens_proacos)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
