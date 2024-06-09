from django.contrib import admin
from tb.models import Contato, Cliente, Usuario, Pedido, Endereco

class Contatos(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data_nascimento','telefone','telefone_retorno','email','email_retorno','mensagem')
    list_display_links = ('id','nome')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Contato, Contatos)

class Clientes(admin.ModelAdmin):
    list_display = ('id','nome','link','foto','data_inicio','data_prevista','data_fim','valorDominio','valorSite','valorMensal','observacoes')
    list_display_links = ('id','nome','link','foto','data_inicio','data_prevista','data_fim','valorDominio','valorSite','valorMensal','observacoes')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Cliente, Clientes)

class Usuarios(admin.ModelAdmin):
    list_display = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha')
    list_display_links = ('id','nome','cpf','email','celular_pais','celular_ddd','celular_numero','senha')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Usuario, Usuarios)

class Pedidos(admin.ModelAdmin):
    list_display = ('id','usuario_nome','item','valor_pgt','data_pgt','numero_pgt','link_pgt')
    list_display_links = ('id','usuario_nome','item','valor_pgt','data_pgt','numero_pgt','link_pgt')
    search_fields = ('usuario__nome',)
    list_per_page = 20

    def usuario_nome(self, obj):
        return obj.usuario.nome

    usuario_nome.short_description = 'Usuario'  # Nome personalizado para a coluna

admin.site.register(Pedido, Pedidos)


class Enderecos(admin.ModelAdmin):
    list_display = ('id','usuario','usuario_nome','rua','numero','complemento','bairro','cidade','estado','pais','cep','principal')
    list_display_links = ('id','usuario','usuario_nome','rua','numero','complemento','bairro','cidade','estado','pais','cep','principal')
    search_fields = ('usuario__nome',)
    list_per_page = 20

    def usuario_nome(self, obj):
        return obj.usuario.nome

    usuario_nome.short_description = 'Usuario'  # Nome personalizado para a coluna

admin.site.register(Endereco, Enderecos)

