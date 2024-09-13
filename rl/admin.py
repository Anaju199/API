from django.contrib import admin
from rl.models import Programacao, Diretoria, Ministerio, Missionario, Lideranca, FotosMinisterios, Usuario, Pregacao, Membros, Igreja, EscolaDominical

class Programacoes(admin.ModelAdmin):
    list_display = ('id', 'dia', 'mes','ano','descricao','sociedade')
    list_display_links = ('id', 'dia', 'mes','ano','descricao','sociedade')
    search_fields = ('dia','mes','ano','descricao','sociedade',)
    list_per_page = 20
    ordering = ('dia','mes')

admin.site.register(Programacao, Programacoes)

class Diretorias(admin.ModelAdmin):
    list_display = ('id','sociedade','presidente','vice_presidente','pri_secretario', 'seg_secretario', 'tesoureiro')
    list_display_links = ('id','sociedade','presidente','vice_presidente','pri_secretario', 'seg_secretario', 'tesoureiro')
    search_fields = ('sociedade',)
    list_per_page = 20

admin.site.register(Diretoria, Diretorias)

class Missionarios(admin.ModelAdmin):
    list_display = ('id','nome','campo','familia','foto')
    list_display_links = ('id','nome','campo','familia','foto')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Missionario, Missionarios)

class Liderancas(admin.ModelAdmin):
    list_display = ('id','nome','cargo','ano_inicio','ano_fim','foto')
    list_display_links = ('id','nome','cargo','ano_inicio','ano_fim','foto')
    search_fields = ('nome','cargo')
    list_per_page = 20

admin.site.register(Lideranca, Liderancas)

class MinisterioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'lideres', 'ano')
    list_display_links = ('id', 'nome', 'lideres')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Ministerio, MinisterioAdmin)

class FotosMinisteriosAdmin(admin.ModelAdmin):
    list_display = ('id', 'ministerio_nome', 'foto')
    list_display_links = ('id', 'ministerio_nome', 'foto')
    search_fields = ('ministerio__nome',)  # Filtrar por nome do ministério
    list_per_page = 20

    def ministerio_nome(self, obj):
        return obj.ministerio.nome

    ministerio_nome.short_description = 'Ministério'  # Nome personalizado para a coluna

admin.site.register(FotosMinisterios, FotosMinisteriosAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'senha')
    list_display_links = ('id', 'login', 'senha')
    search_fields = ('login',)
    list_per_page = 20

admin.site.register(Usuario, UsuarioAdmin)

class PregacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'link','data')
    list_display_links = ('id', 'descricao', 'link','data')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Pregacao, PregacaoAdmin)

class MembrosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data_nascimento','sexo','sociedade', 'status')
    list_display_links = ('id', 'nome', 'data_nascimento','sexo','sociedade', 'status')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Membros, MembrosAdmin)

class IgrejaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'lema','logo','instagram', 'email')
    list_display_links = ('id', 'nome', 'lema','logo','instagram', 'email')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Igreja, IgrejaAdmin)

class EscolaDominicalAdmin(admin.ModelAdmin):
    list_display = ('id', 'classe', 'professores')
    list_display_links = ('id', 'classe', 'professores')
    search_fields = ('classe',)
    list_per_page = 20

admin.site.register(EscolaDominical, EscolaDominicalAdmin)
