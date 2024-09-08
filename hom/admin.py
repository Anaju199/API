from django.contrib import admin
from hom.models import Usuario
from hom.models import Produto, Cor, Imagem, Tamanho, Categoria, Disponibilidade

class Usuarios(admin.ModelAdmin):
    list_display = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha')
    list_display_links = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Usuario, Usuarios)

class ProdutoAdmin(admin.ModelAdmin):
    list_display =  ('id', 'descricao','palavras_chave')
    list_display_links =  ('id', 'descricao','palavras_chave')
    search_fields = ('id','descricao','palavras_chave',)
    list_per_page = 20

admin.site.register(Produto, ProdutoAdmin)


class CorAdmin(admin.ModelAdmin):
    list_display =  ('id', 'cor')
    list_display_links =  ('id', 'cor')
    search_fields = ('id','cor',)
    list_per_page = 20

admin.site.register(Cor, CorAdmin)


class ImagemAdmin(admin.ModelAdmin):
    list_display =  ('id', 'imagem','imagem_link')
    list_display_links =  ('id', 'imagem','imagem_link')
    search_fields = ('id','imagem',)
    list_per_page = 20

    def imagem_link(self, obj):
        return obj.imagem.imagem

admin.site.register(Imagem, ImagemAdmin)


class TamanhoAdmin(admin.ModelAdmin):
    list_display =  ('id', 'tamanho')
    list_display_links =  ('id', 'tamanho')
    search_fields = ('id','tamanho',)
    list_per_page = 20

admin.site.register(Tamanho, TamanhoAdmin)


class CategoriaAdmin(admin.ModelAdmin):
    list_display =  ('id', 'categoria')
    list_display_links =  ('id', 'categoria')
    search_fields = ('id','categoria',)
    list_per_page = 20

admin.site.register(Categoria, CategoriaAdmin)


class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display =  ('id', 'produto')
    list_display_links =  ('id', 'produto')
    search_fields = ('id','produto',)
    list_per_page = 20

admin.site.register(Disponibilidade, DisponibilidadeAdmin)
