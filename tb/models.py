from django.db import models
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator

# class Contato(models.Model):
#     nome = models.CharField(max_length=50)
#     data_nascimento = models.DateField(default="1900-01-01", blank=True)
#     telefone = models.CharField(max_length=11, blank=True)
#     telefone_retorno = models.BooleanField(default=False)
#     email = models.CharField(max_length=50, blank=True)
#     email_retorno = models.BooleanField(default=False)
#     mensagem = models.CharField(max_length=300, default="")

#     def __str__(self):
#         return self.nome

#     def send_email(self, **kwargs):
#         email = "anajulia99pj@gmail.com"
#         assunto = "Novo Contato"

#         corpo = "Novo contato recebido no site.\n\n"
#         for chave, valor in kwargs.items():
#             corpo += f"{chave}: {valor}\n"

#         mail = EmailMessage(
#             subject = assunto,
#             from_email = 'contato@gmail.com',
#             to = [email,],
#             body = corpo,
#             headers = {
#                 'Replay-To' : 'contato@gmail.com'
#             }
#         )
#         mail.send() #python -m pip install -U Django

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
    usuarios = models.ManyToManyField(Usuario, through='UsuarioCliente', related_name='clientes')

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new instance
        super().save(*args, **kwargs)  # Save the cliente first
        
        if is_new:  # Only create UsuarioCliente for new clients
            from .models import UsuarioCliente  # Import here to avoid circular import
            try:
                admin_user = Usuario.objects.get(id=1)
                UsuarioCliente.objects.create(
                    usuario=admin_user,
                    cliente=self,
                    is_admin=True
                )
            except Usuario.DoesNotExist:
                pass  # Handle the case where user 1 doesn't exist

class UsuarioCliente(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_vinculo = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)  # Indicates if the user is an admin for this client

    class Meta:
        unique_together = ('usuario', 'cliente')  # Prevents duplicate relationships

    def __str__(self):
        return f"{self.usuario.nome} - {self.cliente.nome}"

class Avaliacoes(models.Model):
    nome = models.CharField(max_length=50)
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.CharField(max_length=200, blank=True)
    data = models.DateTimeField(auto_now_add=True)

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

class Demanda(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em-andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
        ('precisa-info', 'Precisa de Informação'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo

class MensagemDemanda(models.Model):
    TIPO_AUTOR_CHOICES = [
        ('cliente', 'Cliente'),
        ('admin', 'Admin'),
    ]

    demanda = models.ForeignKey(Demanda, related_name='mensagens', on_delete=models.CASCADE)
    conteudo = models.TextField()
    autor_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_autor = models.CharField(max_length=10, choices=TIPO_AUTOR_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)
    anexos = models.FileField(upload_to='demandas/', null=True, blank=True)

    class Meta:
        ordering = ['criado_em']

    def __str__(self):
        return f"Mensagem de {self.tipo_autor} em {self.criado_em}"



class FotosAmor(models.Model):
    foto = models.ImageField(upload_to='fotosAmor/', blank=True)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    capa = models.BooleanField(default=True)
    data = models.DateField(default="1900-01-01", blank=True)

    def __str__(self):
        return self.descricao
