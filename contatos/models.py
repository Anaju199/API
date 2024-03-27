from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Pensamento(models.Model):
    conteudo = models.CharField(max_length=50)
    autoria = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    favorito = bool()

    def __str__(self):
        return self.autoria
