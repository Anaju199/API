from django.contrib import admin
from django.urls import path, include
from contatos.views import ContatosViewSet, PensamentosViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('contatos', ContatosViewSet, basename='Contatos')
router.register('pensamentos', PensamentosViewSet, basename='Pensamentos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
