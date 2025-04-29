from django.db import models
from django.contrib.auth.hashers import make_password

class UsuarioCasaRohr(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
      if not self.pk or not UsuarioCasaRohr.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'ch'

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
        app_label = 'ch'
        
class Catalogos(models.Model):
    descricao = models.CharField(max_length=80, unique=True)
    arquivo = models.FileField(upload_to='casaRohr/catalogos/')

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = 'ch'