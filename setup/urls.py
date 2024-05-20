from django.contrib import admin
from django.urls import path, include
from tb.views import ContatosViewSet, PensamentosViewSet, contatoEmail
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static
from rl.views import lista_programacoes, lista_diretorias, lista_ministerios, lista_missionarios, lista_liderancas, lista_fotosMinisterios, lista_sociedades, lista_cargos, lista_sociedades_prog, lista_usuarios
from rl.views import ProgramacoesViewSet, DiretoriasViewSet, MinisteriosViewSet, MissionariosViewSet, LiderancasViewSet, FotosMinisteriosViewSet, UsuariosViewSet


router = routers.DefaultRouter()
router.register('contatos', ContatosViewSet, basename='Contatos')
router.register('pensamentos', PensamentosViewSet, basename='Pensamentos')

router.register('programacoes', ProgramacoesViewSet, basename='Programacoes')
router.register('diretorias', DiretoriasViewSet, basename='Diretorias')
router.register('ministerios', MinisteriosViewSet, basename='Ministerios')
router.register('missionarios', MissionariosViewSet, basename='Missionarios')
router.register('liderancas', LiderancasViewSet, basename='Liderancas')
router.register('fotosMinisterios', FotosMinisteriosViewSet, basename='FotosMinisterios')
router.register('usuarios', UsuariosViewSet, basename='Usuarios')

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('controle-admin/', admin.site.urls),
    path('', include(router.urls)),
    path('contatoEmail', contatoEmail),

    path('lista_programacoes/', lista_programacoes),
    path('lista_diretorias/', lista_diretorias),
    path('lista_ministerios/', lista_ministerios),
    path('lista_missionarios/', lista_missionarios),
    path('lista_liderancas/', lista_liderancas),
    path('lista_fotosMinisterios/', lista_fotosMinisterios),
    path('lista_sociedades/', lista_sociedades),
    path('lista_cargos/', lista_cargos),
    path('lista_sociedades_prog/', lista_sociedades_prog),
    path('lista_usuarios/', lista_usuarios)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
