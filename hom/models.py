from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Max

class UsuarioLoja(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, unique=True)
    celular_pais = models.CharField(max_length=3)
    celular_ddd = models.CharField(max_length=3)
    celular_numero = models.CharField(max_length=10)
    senha = models.CharField(max_length=128)
    administrador = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
      if not self.pk or not UsuarioLoja.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'


class Endereco(models.Model):
    usuario = models.ForeignKey(UsuarioLoja, on_delete=models.CASCADE)
    rua = models.CharField(max_length=30)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=20, default="-", blank=True)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=20)
    pais = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)
    principal = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.nome

    def save(self, *args, **kwargs):
        if self.principal:
            # Desmarcar outros endereços principais do mesmo usuário
            Endereco.objects.filter(usuario=self.usuario, principal=True).update(principal=False)
        super(Endereco, self).save(*args, **kwargs)


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria

    class Meta:
        app_label = 'hom'


class Produto(models.Model):
    descricao = models.CharField(max_length=200, unique=True)
    valor = models.CharField(max_length=100)
    palavras_chave = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = 'hom'

class CategoriaProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.categoria

    class Meta:
        app_label = 'hom'

class Cor(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cor = models.CharField(max_length=50)
    inicial = models.BooleanField(default=False)

    def __str__(self):
        return self.cor

    def save(self, *args, **kwargs):
        if self.inicial:
            # Desmarcar outros principais do mesmo usuário
            Cor.objects.filter(produto=self.produto, inicial=True).update(inicial=False)
        super(Cor, self).save(*args, **kwargs)

    class Meta:
        app_label = 'hom'
        unique_together = ['produto', 'cor']

class Imagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='pdt_imagens/', blank=True)
    inicial = models.BooleanField(default=False)

    def __str__(self):
        return self.imagem.name

    def save(self, *args, **kwargs):
        # Verifica se a cor pertence ao produto antes de salvar
        if self.cor.produto != self.produto:
            raise ValueError("A cor selecionada não pertence ao produto.")

        if self.inicial:
            # Desmarcar outras imagens principais do mesmo produto e mesma cor
            Imagem.objects.filter(produto=self.produto, cor=self.cor, inicial=True).update(inicial=False)
            
        super(Imagem, self).save(*args, **kwargs)

    class Meta:
        app_label = 'hom'

class Tamanho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tamanho = models.CharField(max_length=50)

    def __str__(self):
        return self.tamanho

    class Meta:
        app_label = 'hom'

class Disponibilidade(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    quantidade_disponivel = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produto.descricao} - {self.tamanho.tamanho} - {self.cor.cor}"

    class Meta:
        app_label = 'hom'
        unique_together = ['produto', 'tamanho', 'cor']

class Favoritos(models.Model):
    cliente = models.ForeignKey(UsuarioLoja, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cliente.nome} favoritou {self.produto.descricao}"

    class Meta:
        app_label = 'hom'

class Carrinho(models.Model):
    cliente = models.ForeignKey(UsuarioLoja, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no {self.carrinho}"

    class Meta:
        app_label = 'hom'

class Pedido(models.Model):
  OPCOES_STATUS = [
      ("Aberto", "Aberto"),
      ("Pagamento Pendente", "Pagamento Pendente"),
      ("Em andamento", "Em andamento"),
      ("Finalizado", "Finalizado")
  ]

  cliente = models.ForeignKey(UsuarioLoja, on_delete=models.CASCADE)
  status = models.CharField(max_length=50, choices=OPCOES_STATUS)
  data_pedido = models.DateTimeField(auto_now_add=True)
  atualizado_em = models.DateTimeField(auto_now=True)
  quant_itens = models.CharField(max_length=100)
  valor = models.CharField(max_length=100)
  data_pgt = models.DateField(default="1900-01-01", blank=True)
  numero_pedido = models.IntegerField(null=True, blank=True)

  def __str__(self):
      return f"Pedido de {self.cliente.nome}"

  class Meta:
      app_label = 'hom'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE) 
    produto_id = models.CharField(max_length=20)
    descricao = models.CharField(max_length=200)
    valor = models.CharField(max_length=100)
    cor = models.CharField(max_length=50)
    tamanho = models.CharField(max_length=50)
    quantidade = models.PositiveIntegerField(default=1)
    foto = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return f"{self.quantidade}x {self.produto_id} no pedido {self.pedido_id}"

    class Meta:
        app_label = 'hom'

@receiver(pre_save, sender=Pedido)
def set_numero_pedido(sender, instance, **kwargs):
    if instance.numero_pedido is None:  # Verifica se o número já foi atribuído
        ultimo_pedido = Pedido.objects.filter(cliente=instance.cliente).order_by('-numero_pedido').first()
        if ultimo_pedido:
            instance.numero_pedido = ultimo_pedido.numero_pedido + 1
        else:
            instance.numero_pedido = 1       
# ---------------------------------PERSONAL---------------------------------------------------------

class UsuarioPersonal(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=50, blank=True)
    celular_pais = models.CharField(max_length=3)
    celular_ddd = models.CharField(max_length=3)
    celular_numero = models.CharField(max_length=10)
    senha = models.CharField(max_length=128)
    cliente = models.BooleanField(default=False)
    administrador = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
      if not self.pk or not UsuarioPersonal.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'


class Perguntas(models.Model):
    pergunta = models.TextField()

    def __str__(self):
        return self.pergunta

    class Meta:
        app_label = 'hom'


class Respostas(models.Model):
    usuario = models.ForeignKey(UsuarioPersonal, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Perguntas, on_delete=models.CASCADE)
    resposta = models.TextField()

    def __str__(self):
        return self.resposta

    class Meta:
        app_label = 'hom'
        unique_together = ['usuario', 'pergunta']

class Translation(models.Model):
    key = models.CharField(max_length=255, unique=True)  # A chave deve ser única
    pt = models.TextField(blank=True, null=True)  # Português
    en = models.TextField(blank=True, null=True)  # Inglês
    es = models.TextField(blank=True, null=True)  # Espanhol

    def __str__(self):
        return self.key

    class Meta:
        app_label = 'hom'
# ---------------------------------PRO ACOS---------------------------------------------------------

class ItensProAcos(models.Model):
    item = models.CharField(max_length=30, blank=True)
    quant = models.IntegerField(blank=True)
    datalote = models.DateField(blank=True)
    datavenda = models.DateField(blank=True)

    def __str__(self):
        return self.item

    class Meta:
        app_label = 'hom'

# ---------------------------------Discipulados---------------------------------------------------------

class UsuarioDiscipulado(models.Model):
    NIVEIS = [
        ("Iniciante", "Iniciante"),
        ("Intermediario", "Intermediario"),
        ("Avançado", "Avançado")
    ]

    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=50, blank=True, unique=True)
    telefone = models.CharField(max_length=2022, blank=True, null=True)
    igreja = models.ForeignKey('IgrejaParceira', on_delete=models.CASCADE, related_name='master')
    senha = models.CharField(max_length=128)
    nivel = models.CharField(max_length=50, choices=NIVEIS)
    discipulador = models.BooleanField(default=False)
    administrador = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk or not type(self).objects.filter(pk=self.pk, senha=self.senha).exists():
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'hom'

    def __str__(self):
        return self.nome


class TurmaDiscipulado(models.Model):
    nome_turma = models.CharField(max_length=100)
    discipulador = models.ForeignKey(UsuarioDiscipulado, on_delete=models.CASCADE, related_name='discipulador_de')
    discipulado = models.ForeignKey('Discipulados', on_delete=models.CASCADE, related_name='discipulado')
    data_inicio = models.DateField(default="1900-01-01", blank=True)
    data_fim = models.DateField(default="1900-01-01", blank=True)

    class Meta:
        unique_together = ('nome_turma', 'discipulador') 
        app_label = 'hom'

    def __str__(self):
        return f"{self.nome_turma}"
    
class AlunoTurmaDiscipulado(models.Model):
    turma = models.ForeignKey(TurmaDiscipulado, on_delete=models.CASCADE)
    discipulo =  models.ForeignKey(UsuarioDiscipulado, on_delete=models.CASCADE, related_name='discipulo_de')

    class Meta:
        unique_together = ('turma', 'discipulo') 
        app_label = 'hom'

class IgrejaParceira(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'

class Discipulados(models.Model):
    NIVEIS = [
        ("Iniciante", "Iniciante"),
        ("Intermediario", "Intermediario"),
        ("Avançado", "Avançado")
    ]
    
    nome = models.TextField()
    licao = models.TextField(blank=True, null=True)
    nivel = models.CharField(max_length=50, choices=NIVEIS, default='Iniciante')
    proximoEstudo = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='discipulado/', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'


class PerguntasDiscipulado(models.Model):
    discipulado = models.ForeignKey(Discipulados, on_delete=models.CASCADE)
    pergunta = models.TextField()

    def __str__(self):
        return self.pergunta

    class Meta:
        app_label = 'hom'


class RespostasDiscipulado(models.Model):
    usuario = models.ForeignKey(UsuarioDiscipulado, on_delete=models.CASCADE)
    turma = models.ForeignKey(TurmaDiscipulado, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(PerguntasDiscipulado, on_delete=models.CASCADE)
    resposta = models.TextField()

    def __str__(self):
        return self.resposta

    class Meta:
        app_label = 'hom'
        unique_together = ['usuario', 'pergunta']


# ---------------------------------PIB São João Betim---------------------------------------------------------

class UsuarioSjb(models.Model):

    login = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
      if not self.pk or not UsuarioSjb.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.login

    class Meta:
        app_label = 'hom'



class Igreja(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    lema = models.CharField(max_length=80)
    logo = models.ImageField(upload_to='imagens_igreja/', blank=True)
    endereco = models.CharField(max_length=80)
    instagram = models.CharField(max_length=50, blank=True)
    youtube = models.CharField(max_length=80, blank=True)
    email = models.CharField(max_length=50, blank=True)
    nome_banco = models.CharField(max_length=10, blank=True)
    num_banco = models.CharField(max_length=10, blank=True)
    agencia = models.CharField(max_length=50, blank=True)
    conta_corrente = models.CharField(max_length=50, blank=True)
    chave_pix = models.CharField(max_length=50, blank=True)
    tipo_chave_pix =  models.CharField(max_length=20, default='CNPJ', blank=True)
    qr_code_pix = models.ImageField(upload_to='imagens_igreja/', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'


class Pastor(models.Model):
    OPCOES_CARGO = [
        ("Pastor", "Pastor"),
        ("Seminarista", "Seminarista")
    ]

    nome = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50, choices=OPCOES_CARGO, default='')
    foto = models.ImageField(upload_to="lideranca/", blank=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=11, blank=True)
    youtube = models.CharField(max_length=80, blank=True)
    email = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'
        unique_together = ['nome', 'cargo']


class Pregacao(models.Model):
    descricao = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=100)
    data = models.DateField(default="1900-01-01", blank=True)

    def save(self, *args, **kwargs):
        # Converter a URL para o formato embed antes de salvar
        if 'youtu.be' in self.link:
            video_id = self.link.split('/')[-1].split('?')[0]
            self.link = f'https://www.youtube.com/embed/{video_id}'
        elif 'youtube.com' in self.link and 'watch?v=' in self.link:
            video_id = self.link.split('watch?v=')[-1].split('&')[0]
            self.link = f'https://www.youtube.com/embed/{video_id}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = 'hom'


class Devocional(models.Model):
    titulo = models.CharField(max_length=80, unique=True)
    devocional = models.TextField()
    data = models.DateField(default="1900-01-01", blank=True)

    def __str__(self):
        return self.titulo

    class Meta:
        app_label = 'hom'


class Membros(models.Model):
    # OPCOES_SOCIEDADE = [
    #     ("UCP", "UCP"),
    #     ("UPA", "UPA"),
    #     ("UMP", "UMP"),
    #     ("SAF", "SAF"),
    #     ("UPH", "UPH")
    # ]

    # OPCOES_ESTADO_CIVIL = [
    #     ("SOLTEIRO", "Solteiro(a)"),
    #     ("CASADO", "Casado(a)"),
    #     ("DIVORCIADO", "Divorciado(a)"),
    #     ("VIÚVO", "Viúvo(a)"),
    #     ("SEPARADO", "Separado(a)"),
    #     ("UNIÃO ESTÁVEL", "União Estável"),
    # ]

    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1)
    # sociedade = models.CharField(max_length=3, choices=OPCOES_SOCIEDADE, default='', blank=True)
    status = models.CharField(max_length=20, default='', blank=True)
    numero_membro = models.CharField(max_length=10, default='', blank=True)  
    ativo = models.BooleanField(default=True)
    observacoes = models.CharField(max_length=300, default='', blank=True)  

    # # Endereço
    # rua = models.CharField(max_length=100, default='', blank=True)  
    # numero = models.CharField(max_length=10, default='', blank=True)  
    # bairro = models.CharField(max_length=50, default='', blank=True)  
    # cep = models.CharField(max_length=15, default='', blank=True)  
    # telefone = models.CharField(max_length=25, default='', blank=True)  

    # # Informações pessoais
    # nacionalidade = models.CharField(max_length=30, default='', blank=True)  
    # naturalidade = models.CharField(max_length=30, default='', blank=True)  
    # alfabetizado = models.BooleanField(default=True)
    # estado_civil = models.CharField(max_length=20, choices=OPCOES_ESTADO_CIVIL, default='', blank=True)
    # religiao_conjuge = models.CharField(max_length=50, default='', blank=True)  
    # ocupacao = models.CharField(max_length=50, default='', blank=True)  

    # cpf = models.CharField(max_length=11, default='', blank=True)  
    # identidade = models.CharField(max_length=20, default='', blank=True)  

    # # Opção de pai/mãe como membro
    # pai = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='filhos_do_pai')
    # mae = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='filhos_da_mae')
    # conjuge = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='conjuge_de')

    # # Opção de pai/mãe como texto
    # pai_nome = models.CharField(max_length=50, blank=True, null=True)
    # mae_nome = models.CharField(max_length=50, blank=True, null=True)
    # conjuge_nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'


class Download(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    arquivo = models.FileField(upload_to='downloads/')

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'



# ---------------------------------Site de treinos---------------------------------------------------------


class UsuarioTreinos(models.Model):

    login = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
      if not self.pk or not UsuarioTreinos.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.login

    class Meta:
        app_label = 'hom'



class Exercicio(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    foto = models.ImageField(upload_to="treino/", blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'



class Treino(models.Model):
    nome = models.CharField(max_length=50)
    usuario = models.ForeignKey(UsuarioTreinos, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'
        unique_together = ['nome', 'usuario']



class ExercicioTreino(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    series = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'
        unique_together = ['treino', 'exercicio']        



class TreinoExecutado(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UsuarioTreinos, on_delete=models.CASCADE)
    data_execucao = models.DateField(auto_now_add=True)
    tempo_treino = models.PositiveIntegerField(null=True, blank=True)

    def copiar_cargas_ultimo_treino(self):
        exercicios_treino = self.treino.exerciciotreino_set.all()

        for et in exercicios_treino:
            ultimo = (
                ExercicioExecutado.objects
                .filter(
                    treino_executado__treino=self.treino,
                    exercicio=et.exercicio,
                    treino_executado__usuario=self.usuario
                )
                .exclude(treino_executado=self)
                .order_by('-treino_executado_id')
                .first()
            )

            print("EXERCICIO:", et.exercicio.id)
            print("ULTIMO:", ultimo)

            ExercicioExecutado.objects.create(
                treino_executado=self,
                exercicio=et.exercicio,
                carga=ultimo.carga if ultimo else 0
            )

    def __str__(self):
        return f"{self.treino.nome} - {self.data_execucao}"



class ExercicioExecutado(models.Model):
    treino_executado = models.ForeignKey(TreinoExecutado, on_delete=models.CASCADE, related_name="exercicios")
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    carga = models.DecimalField(max_digits=6, decimal_places=2)
    realizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.exercicio.nome} - {self.carga} kg"

    class Meta:
        app_label = 'hom'
        unique_together = ['treino_executado', 'exercicio']


