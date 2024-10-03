from django.db import models
from django.contrib.auth.hashers import make_password

class UsuarioLoja(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, unique=True)
    celular_pais = models.CharField(max_length=3)
    celular_ddd = models.CharField(max_length=3)
    celular_numero = models.CharField(max_length=10)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
      if not self.pk or not UsuarioLoja.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'hom'



class Produto(models.Model):
    descricao = models.TextField()
    valor = models.CharField(max_length=100)
    palavras_chave = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.descricao

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

class Imagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imagens/', blank=True)
    inicial = models.BooleanField(default=False)

    def __str__(self):
        return self.imagem.name

    def save(self, *args, **kwargs):
        # Verifica se a cor pertence ao produto antes de salvar
        if self.cor.produto != self.produto:
            raise ValueError("A cor selecionada não pertence ao produto.")

        if self.inicial:
            # Desmarcar outras imagens principais do mesmo produto
            Imagem.objects.filter(produto=self.produto, inicial=True).update(inicial=False)
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

class Categoria(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria

    class Meta:
        app_label = 'hom'

class Disponibilidade(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    quantidade_disponivel = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produto.descricao} - {self.tamanho.tamanho}"

    class Meta:
        app_label = 'hom'

# ---------------------------------PERSONAL---------------------------------------------------------

class UsuarioPersonal(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=50, blank=True)
    celular = models.CharField(max_length=15, blank=True)
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
