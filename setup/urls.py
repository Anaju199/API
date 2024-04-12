from django.contrib import admin
from django.urls import path, include
from tb.views import ContatosViewSet, PensamentosViewSet, contatoEmail
from rest_framework import routers

router = routers.DefaultRouter()
router.register('contatos', ContatosViewSet, basename='Contatos')
router.register('pensamentos', PensamentosViewSet, basename='Pensamentos')

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('controle-admin/', admin.site.urls),
    path('', include(router.urls)),
    path('contatoEmail', contatoEmail)
]
