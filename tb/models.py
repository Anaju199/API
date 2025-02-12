from django.db import models
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator

class Contato(models.Model):
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField(default="1900-01-01", blank=True)
    telefone = models.CharField(max_length=11, blank=True)
    telefone_retorno = models.BooleanField(default=False)
    email = models.CharField(max_length=50, blank=True)
    email_retorno = models.BooleanField(default=False)
    mensagem = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.nome

    def send_email(self, **kwargs):
        email = "anajulia99pj@gmail.com"
        assunto = "Novo Contato"

        corpo = "Novo contato recebido no site.\n\n"
        for chave, valor in kwargs.items():
            corpo += f"{chave}: {valor}\n"

        mail = EmailMessage(
            subject = assunto,
            from_email = 'contato@gmail.com',
            to = [email,],
            body = corpo,
            headers = {
                'Replay-To' : 'contato@gmail.com'
            }
        )
        mail.send() #python -m pip install -U Django


class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    foto = models.ImageField(upload_to="fotos/clientes/", blank=True)
    data_inicio = models.DateField(default="1900-01-01", blank=True)
    data_prevista = models.DateField(default="1900-01-01", blank=True)
    data_fim = models.DateField(default="1900-01-01", blank=True)
    valorDominio = models.CharField(max_length=10, blank=True)
    valorSite = models.CharField(max_length=10, blank=True)
    valorMensal = models.CharField(max_length=10, blank=True)
    observacoes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nome


class Avaliacoes(models.Model):
    nome = models.CharField(max_length=50)
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.CharField(max_length=200, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, unique=True)
    celular_pais = models.CharField(max_length=3)
    celular_ddd = models.CharField(max_length=3)
    celular_numero = models.CharField(max_length=10)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
      if not self.pk or not Usuario.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Item(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    valor_pdt = models.CharField(max_length=100)
    numero_pgt = models.CharField(max_length=3)

    def __str__(self):
        return self.usuario.nome

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    itens = models.CharField(max_length=100)
    valor_pgt = models.CharField(max_length=100)
    data_pgt = models.DateField(default="1900-01-01", blank=True)
    link_pgt = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.usuario.nome

class Endereco(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
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


# class FormaPagamento(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     item = models.CharField(max_length=100)
#     valor_pgt = models.CharField(max_length=100)
#     data_pgt = models.DateField(default="1900-01-01", blank=True)
#     numero_pgt = models.CharField(max_length=3)
#     link_pgt = models.CharField(max_length=100, default='')

#     def __str__(self):
#         return self.usuario.nome
