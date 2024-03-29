from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField(default="1900-01-01")
    telefone = models.CharField(max_length=11)
    telefone_check = models.BooleanField(default=False)
    email = models.CharField(max_length=50)
    email_check = models.BooleanField(default=False)
    mensagem = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.nome


class Pensamento(models.Model):
    conteudo = models.CharField(max_length=50)
    autoria = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    favorito = bool()

    def __str__(self):
        return self.autoria
