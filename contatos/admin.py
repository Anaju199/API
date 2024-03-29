from django.contrib import admin
from contatos.models import Contato, Pensamento

class Contatos(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data_nascimento','telefone','telefone_check','email','email_check','mensagem')
    list_display_links = ('id','nome')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Contato, Contatos)

class Pensamentos(admin.ModelAdmin):
    list_display = ('id','conteudo','autoria','modelo','favorito')
    list_display_links = ('id','autoria')
    search_fields = ('autoria',)
    list_per_page = 20

admin.site.register(Pensamento, Pensamentos)

