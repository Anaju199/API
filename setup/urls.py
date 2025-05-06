from django.contrib import admin
from django.urls import path, include
from tb.views import aj_lista_itens, aj_lista_pedidos, aj_lista_usuarios, aj_lista_enderecos, create_payload, get_csrf_token, criar_chavePublica, aj_lista_meus_clientes
from tb.views import aj_lista_clientes, aj_lista_layouts, aj_lista_avaliacoes
from tb.views import ClientesViewSet, AJUsuariosViewSet, AJLoginView, ItensViewSet, PedidosViewSet, EnderecosViewSet, AvaliacoesViewSet
from tb.views import UsuarioClienteViewSet, DemandaViewSet, MensagemDemandaViewSet
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static
from rl.views import rl_lista_programacoes, rl_lista_diretorias, rl_lista_ministerios, rl_lista_missionarios, rl_lista_liderancas
from rl.views import rl_lista_fotos, rl_lista_sociedades, rl_lista_cargos, rl_lista_sociedades_prog, rl_lista_usuarios
from rl.views import rl_lista_pregacoes, rl_lista_membros, rl_lista_aniversariantes, rl_lista_cargos_pastor, rl_lista_pastor
from rl.views import rl_lista_escolaDominical, rl_lista_redeSocial, rl_lista_downloads, rl_lista_estados_civis, rl_contar_membros_relacionamentos
from rl.views import RlProgramacoesViewSet, RlDiretoriasViewSet, RlMinisteriosViewSet, RlMissionariosViewSet, RlLiderancasViewSet
from rl.views import RlFotosViewSet, RlUsuariosViewSet, RlLoginView, RlPregacaoViewSet, RlMembrosViewSet, RlIgrejaViewSet
from rl.views import RlEscolaDominicalViewSet, RlPastorViewSet, RlRedesSociaisViewSet, RlDownloadsViewSet
from rl.views import RlEstatisticasIdade, RlEstatisticasEstadoCivil, RlEstatisticasSexo, RlEstatisticasSociedade, RlEstatisticasStatus

from hom.views import ItensProAcosViewSet, lista_itens_proacos

from ch.views import ChUsuariosCasaRohrViewSet, ChLoginCasaRohrView, ChFotosViewSet, ChCategoriasViewSet, ch_lista_fotos, ChCatalogosViewSet, ch_lista_categorias

from hom.views import hom_lista_produtos, HomLoginLojaView, hom_isFavorito, hom_lista_favoritos, hom_lista_carrinho, hom_lista_pedidos
from hom.views import hom_loja_lista_usuarios, hom_loja_lista_enderecos
from hom.views import HomProdutoViewSet, HomCorViewSet, HomImagemViewSet, HomTamanhoViewSet, HomCategoriaViewSet, HomCategoriaProdutoViewSet
from hom.views import HomDisponibilidadeViewSet, HomUsuariosLojaViewSet, HomFavoritosViewSet, HomCarrinhoViewSet, HomPedidoViewSet 
from hom.views import HomItemPedidoViewSet, HomEnderecosViewSet

from hom.views import hom_lista_usuarios_personal, hom_lista_perguntas, hom_lista_respostas, HomLoginPersonalView
from hom.views import HomUsuariosPersonalViewSet, HomUsuariosPersonalClientesViewSet, HomPerguntasViewSet, HomRespostasViewSet, HomTranslationView, HomTranslationViewSet

from hom.views import hom_lista_discipulados, hom_lista_perguntas_discipulado, hom_lista_respostas_discipulado, HomLoginDiscipuladoView
from hom.views import HomDiscipuladosViewSet, HomUsuarioDiscipuladoViewSet, hom_lista_usuario_discipulado, hom_lista_igrejas
from hom.views import HomIgrejasParceirasViewSet, HomPerguntasDiscipuladoViewSet, HomRespostasDiscipuladoViewSet, hom_lista_niveis_discipulo
from hom.views import HomAlunoTurmaDiscipuladoViewSet, HomTurmaDiscipuladoViewSet, hom_lista_turma_discipulados,hom_lista_aluno_discipulados
from hom.views import hom_verificar_resposta

router = routers.DefaultRouter()
# router.register('aj_contatos', ContatosViewSet, basename='aj_Contatos')
router.register('aj_clientes', ClientesViewSet, basename='aj_Clientes')
router.register('aj_usuarios', AJUsuariosViewSet, basename='aj_Usuarios')
router.register('aj_itens', ItensViewSet, basename='aj_itens')
router.register('aj_pedidos', PedidosViewSet, basename='aj_Pedidos')
router.register('aj_usuarios_enderecos', EnderecosViewSet, basename='aj_usuarios_enderecos')
router.register('aj_avaliacoes', AvaliacoesViewSet, basename='aj_avaliacoes')
router.register('aj_demandas', DemandaViewSet, basename='aj_demandas')
router.register('aj_mensagens_demanda', MensagemDemandaViewSet, basename='aj_mensagens_demanda')

# ---------------------------------PERSONAL---------------------------------------------------------
router.register('hom_usuarios_personal', HomUsuariosPersonalViewSet, basename='hom_usuarios_personal')
router.register('hom_usuarios_personal_clientes', HomUsuariosPersonalClientesViewSet, basename='hom_usuarios_personal_clientes')
router.register('hom_perguntas', HomPerguntasViewSet, basename='hom_Perguntas')
router.register('hom_respostas', HomRespostasViewSet, basename='hom_Respostas')
router.register('hom_translate', HomTranslationViewSet, basename='hom_translate')

# ---------------------------------IGREJA---------------------------------------------------------
router.register('rl_programacoes', RlProgramacoesViewSet, basename='Programacoes')
router.register('rl_diretorias', RlDiretoriasViewSet, basename='Diretorias')
router.register('rl_ministerios', RlMinisteriosViewSet, basename='Ministerios')
router.register('rl_missionarios', RlMissionariosViewSet, basename='Missionarios')
router.register('rl_liderancas', RlLiderancasViewSet, basename='Liderancas')
router.register('rl_fotos', RlFotosViewSet, basename='Fotos')
router.register('rl_usuarios', RlUsuariosViewSet, basename='Usuarios')
router.register('rl_pregacoes', RlPregacaoViewSet, basename='Pregacoes')
router.register('rl_membros', RlMembrosViewSet, basename='Membros')
router.register('rl_igreja', RlIgrejaViewSet, basename='Igreja')
router.register('rl_escolaDominical', RlEscolaDominicalViewSet, basename='EscolaDominical')
router.register('rl_pastor', RlPastorViewSet, basename='Pastor')
router.register('rl_redesSociais', RlRedesSociaisViewSet, basename='redesSociais')
router.register('rl_downloads', RlDownloadsViewSet, basename='downloads')


# ---------------------------------LOJA---------------------------------------------------------
router.register('hom_loja_usuarios', HomUsuariosLojaViewSet, basename='hom_loja_Usuarios')
router.register('hom_loja_usuarios_enderecos', HomEnderecosViewSet, basename='hom_loja_Usuarios_enderecos')
router.register('hom_produto', HomProdutoViewSet, basename='hom_produto')
router.register('hom_imagem', HomImagemViewSet, basename='hom_imagem')
router.register('hom_tamanho', HomTamanhoViewSet, basename='hom_tamanho')
router.register('hom_disponibilidade', HomDisponibilidadeViewSet, basename='hom_disponibilidade')
router.register('hom_cor', HomCorViewSet, basename='hom_cor')
router.register('hom_categoria', HomCategoriaViewSet, basename='hom_categoria')
router.register('hom_categoria_produto', HomCategoriaProdutoViewSet, basename='hom_categoria_produto')
router.register('hom_favorito', HomFavoritosViewSet, basename='hom_favorito')
router.register('hom_carrinho', HomCarrinhoViewSet, basename='hom_carrinho')
router.register('hom_pedido', HomPedidoViewSet, basename='hom_pedido')
router.register('hom_itemPedido', HomItemPedidoViewSet, basename='hom_itemPedido')

# ---------------------------------PROACOS---------------------------------------------------------
router.register('item_proacos', ItensProAcosViewSet, basename='item_proacos')

# ---------------------------------CASAROHR---------------------------------------------------------
router.register('ch_usuarios_casarohr', ChUsuariosCasaRohrViewSet, basename='ch_usuarios_casarohr')
router.register('ch_fotos', ChFotosViewSet, basename='ch_fotos')
router.register('ch_categorias', ChCategoriasViewSet, basename='ch_categorias')
router.register('ch_catalogos', ChCatalogosViewSet, basename='ch_catalogos')

# ---------------------------------DISCIPULADO---------------------------------------------------------
router.register('hom_usuario_discipulado', HomUsuarioDiscipuladoViewSet, basename='hom_usuario_discipulado')
router.register('hom_turma_discipulado', HomTurmaDiscipuladoViewSet, basename='hom_turma_discipulado')
router.register('hom_aluno_turma_discipulado', HomAlunoTurmaDiscipuladoViewSet, basename='hom_aluno_turma_discipulado')
router.register('hom_igrejas', HomIgrejasParceirasViewSet, basename='hom_igrejas')
router.register('hom_discipulados', HomDiscipuladosViewSet, basename='hom_discipulados')
router.register('hom_perguntas_discipulado', HomPerguntasDiscipuladoViewSet, basename='hom_Perguntas_discipulado')
router.register('hom_respostas_discipulado', HomRespostasDiscipuladoViewSet, basename='hom_Respostas_discipulado')

router.register('aj_usuario_cliente', UsuarioClienteViewSet, basename='aj_usuario_cliente')

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('controle-admin/', admin.site.urls),
    path('', include(router.urls)),
    path('aj_login/', AJLoginView.as_view(), name='aj_login'),
    path('aj_lista_itens/', aj_lista_itens, name='aj_lista_itens'),
    path('aj_lista_pedidos/', aj_lista_pedidos, name='aj_lista_pedidos'),
    path('aj_lista_usuarios/', aj_lista_usuarios, name='aj_lista_usuarios'),
    path('aj_lista_enderecos/', aj_lista_enderecos, name='aj_lista_enderecos'),
    path('aj_lista_clientes/', aj_lista_clientes, name='aj_lista_clientes'),
    path('aj_lista_avaliacoes/', aj_lista_avaliacoes, name='aj_lista_avaliacoes'),
    path('aj_lista_layouts/', aj_lista_layouts, name='aj_lista_layouts'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('api/create/', create_payload, name='create_payload'),
    path('api/criar_chavePublica/', criar_chavePublica, name='criar_chavePublica'),
    path('aj_lista_meus_clientes/', aj_lista_meus_clientes, name='aj_lista_meus_clientes'),
    # path('contatoEmail', contatoEmail),


# ---------------------------------Regiao Leste---------------------------------------------------------
    path('rl_lista_programacoes/', rl_lista_programacoes),
    path('rl_lista_diretorias/', rl_lista_diretorias),
    path('rl_lista_ministerios/', rl_lista_ministerios),
    path('rl_lista_missionarios/', rl_lista_missionarios),
    path('rl_lista_liderancas/', rl_lista_liderancas),
    path('rl_lista_fotos/', rl_lista_fotos),
    path('rl_lista_sociedades/', rl_lista_sociedades),
    path('rl_lista_cargos/', rl_lista_cargos),
    path('rl_lista_cargos_pastor/', rl_lista_cargos_pastor),
    path('rl_lista_pastor/', rl_lista_pastor),
    path('rl_lista_sociedades_prog/', rl_lista_sociedades_prog),
    path('rl_lista_usuarios/', rl_lista_usuarios),
    path('rl_lista_pregacoes/', rl_lista_pregacoes),
    path('rl_lista_estados_civis/', rl_lista_estados_civis),
    path('rl_lista_membros/', rl_lista_membros),
    path('rl_lista_aniversariantes/', rl_lista_aniversariantes),
    path('rl_lista_redeSocial/', rl_lista_redeSocial),
    path('rl_lista_escolaDominical/', rl_lista_escolaDominical),
    path('rl_lista_downloads/', rl_lista_downloads),
    path('rl_login/', RlLoginView.as_view(), name='rl_login'),
    path('rl_estatisticas_idade/', RlEstatisticasIdade.as_view(), name='rl_estatisticas_idade'),
    path('rl_estatisticas_sexo/', RlEstatisticasSexo.as_view(), name='rl_estatisticas_sexo'),
    path('rl_estatisticas_sociedade/', RlEstatisticasSociedade.as_view(), name='rl_estatisticas_sociedade'),
    path('rl_estatisticas_status/', RlEstatisticasStatus.as_view(), name='rl_estatisticas_status'),
    path('rl_estatisticas_estados_civis/', RlEstatisticasEstadoCivil.as_view(), name='rl_estatisticas_estados_civis'),
    path('rl_contar_membros_relacionamentos/', rl_contar_membros_relacionamentos),
# ---------------------------------Loja---------------------------------------------------------
    path('hom_lista_produtos/', hom_lista_produtos),
    path('hom_isFavorito/', hom_isFavorito),
    path('hom_lista_favoritos/', hom_lista_favoritos),
    path('hom_lista_carrinho/', hom_lista_carrinho),
    path('hom_lista_pedidos/', hom_lista_pedidos),
    path('hom_loja_lista_usuarios/', hom_loja_lista_usuarios),
    path('hom_loja_lista_enderecos/', hom_loja_lista_enderecos),
    path('hom_login_loja/', HomLoginLojaView.as_view(), name='hom_login_loja'),

# ---------------------------------PERSONAL---------------------------------------------------------
    path('hom_lista_usuarios_personal/', hom_lista_usuarios_personal),
    path('hom_lista_perguntas/', hom_lista_perguntas),
    path('hom_lista_respostas/', hom_lista_respostas),
    path('hom_login_personal/', HomLoginPersonalView.as_view(), name='hom_login_personal'),
    path('hom_translations/<str:lang>/', HomTranslationView.as_view(), name='hom_translations'),

# ---------------------------------PRO AÇOS---------------------------------------------------------
    path('lista_itens_proacos/', lista_itens_proacos),

    
# ---------------------------------CASAROHR---------------------------------------------------------
    path('ch_logincasarohr/', ChLoginCasaRohrView.as_view(), name='ch_logincasarohr'),
    path('ch_lista_categorias/', ch_lista_categorias),
    path('ch_lista_fotos/', ch_lista_fotos),

# ---------------------------------DISCIPULADOS---------------------------------------------------------
    path('hom_lista_usuario_discipulado/', hom_lista_usuario_discipulado),
    path('hom_lista_discipulados/', hom_lista_discipulados),
    path('hom_lista_turma_discipulados/', hom_lista_turma_discipulados),
    path('hom_lista_aluno_discipulados/', hom_lista_aluno_discipulados),
    path('hom_lista_igrejas/', hom_lista_igrejas),
    path('hom_lista_perguntas_discipulado/', hom_lista_perguntas_discipulado),
    path('hom_lista_respostas_discipulado/', hom_lista_respostas_discipulado),
    path('hom_lista_niveis_discipulo/', hom_lista_niveis_discipulo),
    path('hom_verificar_resposta/', hom_verificar_resposta),
    path('hom_login_discipulado/', HomLoginDiscipuladoView.as_view(), name='hom_login_discipulado')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
