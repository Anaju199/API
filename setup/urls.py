from django.contrib import admin
from django.urls import path, include
from tb.views import aj_lista_pedidos, aj_lista_usuarios, aj_lista_enderecos, aj_lista_endereco_principal
from tb.views import ContatosViewSet, ClientesViewSet, AJUsuariosViewSet, AJLoginView, PedidosViewSet, EnderecosViewSet
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static
from rl.views import lista_programacoes, lista_diretorias, lista_ministerios, lista_missionarios, lista_liderancas, lista_fotosMinisterios, lista_sociedades, lista_cargos, lista_sociedades_prog, lista_usuarios, lista_pregacoes
from rl.views import ProgramacoesViewSet, DiretoriasViewSet, MinisteriosViewSet, MissionariosViewSet, LiderancasViewSet, FotosMinisteriosViewSet, UsuariosViewSet, LoginView, PregacaoViewSet


router = routers.DefaultRouter()
router.register('contatos', ContatosViewSet, basename='Contatos')
router.register('clientes', ClientesViewSet, basename='Clientes')
router.register('aj_usuarios', AJUsuariosViewSet, basename='aj_Usuarios')
router.register('aj_pedidos', PedidosViewSet, basename='aj_Pedidos')
router.register('aj_usuarios_enderecos', EnderecosViewSet, basename='aj_usuarios_enderecos')

router.register('programacoes', ProgramacoesViewSet, basename='Programacoes')
router.register('diretorias', DiretoriasViewSet, basename='Diretorias')
router.register('ministerios', MinisteriosViewSet, basename='Ministerios')
router.register('missionarios', MissionariosViewSet, basename='Missionarios')
router.register('liderancas', LiderancasViewSet, basename='Liderancas')
router.register('fotosMinisterios', FotosMinisteriosViewSet, basename='FotosMinisterios')
router.register('usuarios', UsuariosViewSet, basename='Usuarios')
router.register('pregacoes', PregacaoViewSet, basename='Pregacoes')

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('controle-admin/', admin.site.urls),
    path('', include(router.urls)),
    path('aj_login/', AJLoginView.as_view(), name='aj_login'),
    path('aj_lista_pedidos/', aj_lista_pedidos, name='aj_lista_pedidos'),
    path('aj_lista_usuarios/', aj_lista_usuarios, name='aj_lista_usuarios'),
    path('aj_lista_enderecos/', aj_lista_enderecos, name='aj_lista_enderecos'),
    path('aj_lista_endereco_principal/', aj_lista_endereco_principal, name='aj_lista_endereco_principal'),
    # path('contatoEmail', contatoEmail),

    path('lista_programacoes/', lista_programacoes),
    path('lista_diretorias/', lista_diretorias),
    path('lista_ministerios/', lista_ministerios),
    path('lista_missionarios/', lista_missionarios),
    path('lista_liderancas/', lista_liderancas),
    path('lista_fotosMinisterios/', lista_fotosMinisterios),
    path('lista_sociedades/', lista_sociedades),
    path('lista_cargos/', lista_cargos),
    path('lista_sociedades_prog/', lista_sociedades_prog),
    path('lista_usuarios/', lista_usuarios),
    path('lista_pregacoes/', lista_pregacoes),
    path('login/', LoginView.as_view(), name='login')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
