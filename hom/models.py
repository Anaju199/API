from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver

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

# ---------------------------------CASA ROHR---------------------------------------------------------
class UsuarioCasaRohr(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
      if not self.pk or not UsuarioLoja.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'

class Fotos(models.Model):
    OPCOES_CATEGORIA = [
        ("Moveis", "Moveis"),
        ("Supermercado", "Supermercado"),
        ("Construcao", "Construcao"),
        ("Magazine", "Magazine")
    ]

    categoria = models.CharField(max_length=50, choices=OPCOES_CATEGORIA)
    foto = models.ImageField(upload_to='casaRohr/fotosCasaRohr/', blank=True)
    descricao = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.ministerio.nome if self.ministerio else ''} {self.programacao.nome if self.programacao else ''}".strip()

    class Meta:
        app_label = 'hom'
        
class Catalogos(models.Model):
    descricao = models.CharField(max_length=80, unique=True)
    arquivo = models.FileField(upload_to='casaRohr/catalogos/')

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = 'hom'