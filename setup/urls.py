from django.contrib import admin
from django.urls import path, include
from tb.views import aj_lista_itens, aj_lista_pedidos, aj_lista_usuarios, aj_lista_enderecos, aj_lista_endereco_principal, create_payload, get_csrf_token
from tb.views import ContatosViewSet, ClientesViewSet, AJUsuariosViewSet, AJLoginView, ItensViewSet, PedidosViewSet, EnderecosViewSet
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static
from rl.views import lista_programacoes, lista_diretorias, lista_ministerios, lista_missionarios, lista_liderancas
from rl.views import lista_fotosMinisterios, lista_sociedades, lista_cargos, lista_sociedades_prog, lista_usuarios
from rl.views import lista_pregacoes, lista_membros, lista_aniversariantes, lista_cargos_pastor, lista_pastor, lista_redeSocial
from rl.views import ProgramacoesViewSet, DiretoriasViewSet, MinisteriosViewSet, MissionariosViewSet, LiderancasViewSet
from rl.views import FotosMinisteriosViewSet, UsuariosViewSet, LoginView, PregacaoViewSet, MembrosViewSet, IgrejaViewSet
from rl.views import EscolaDominicalViewSet, PastorViewSet, RedesSociaisViewSet

from hom.views import ItensProAcosViewSet, lista_itens_proacos

from hom.views import lista_produtos
from hom.views import ProdutoViewSet, CorViewSet, ImagemViewSet, TamanhoViewSet, CategoriaViewSet, DisponibilidadeViewSet

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
router.register('programacoes', ProgramacoesViewSet, basename='Programacoes')
router.register('diretorias', DiretoriasViewSet, basename='Diretorias')
router.register('ministerios', MinisteriosViewSet, basename='Ministerios')
router.register('missionarios', MissionariosViewSet, basename='Missionarios')
router.register('liderancas', LiderancasViewSet, basename='Liderancas')
router.register('fotosMinisterios', FotosMinisteriosViewSet, basename='FotosMinisterios')
router.register('usuarios', UsuariosViewSet, basename='Usuarios')
router.register('pregacoes', PregacaoViewSet, basename='Pregacoes')
router.register('membros', MembrosViewSet, basename='Membros')
router.register('igreja', IgrejaViewSet, basename='Igreja')
router.register('escolaDominical', EscolaDominicalViewSet, basename='EscolaDominical')
router.register('pastor', PastorViewSet, basename='Pastor')
router.register('redesSociais', RedesSociaisViewSet, basename='redesSociais')


# ---------------------------------LOJA---------------------------------------------------------
router.register('produto', ProdutoViewSet, basename='produto')
router.register('imagem', ImagemViewSet, basename='imagem')
router.register('tamanho', TamanhoViewSet, basename='tamanho')
router.register('disponibilidade', DisponibilidadeViewSet, basename='disponibilidade')
router.register('cor', CorViewSet, basename='cor')
router.register('categoria', CategoriaViewSet, basename='categoria')

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

    path('lista_programacoes/', lista_programacoes),
    path('lista_diretorias/', lista_diretorias),
    path('lista_ministerios/', lista_ministerios),
    path('lista_missionarios/', lista_missionarios),
    path('lista_liderancas/', lista_liderancas),
    path('lista_fotosMinisterios/', lista_fotosMinisterios),
    path('lista_sociedades/', lista_sociedades),
    path('lista_cargos/', lista_cargos),
    path('lista_cargos_pastor/', lista_cargos_pastor),
    path('lista_pastor/', lista_pastor),
    path('lista_sociedades_prog/', lista_sociedades_prog),
    path('lista_usuarios/', lista_usuarios),
    path('lista_pregacoes/', lista_pregacoes),
    path('lista_membros/', lista_membros),
    path('lista_aniversariantes/', lista_aniversariantes),
    path('lista_redeSocial/', lista_redeSocial),
    path('login/', LoginView.as_view(), name='login'),

# ---------------------------------Loja---------------------------------------------------------
    path('lista_produtos/', lista_produtos),


# ---------------------------------PERSONAL---------------------------------------------------------
    path('lista_usuarios_personal/', lista_usuarios_personal),
    path('lista_perguntas/', lista_perguntas),
    path('lista_respostas/', lista_respostas),
    path('login_personal/', LoginPersonalView.as_view(), name='login_personal'),


# ---------------------------------PRO AÇOS---------------------------------------------------------
    path('lista_itens_proacos/', lista_itens_proacos)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
