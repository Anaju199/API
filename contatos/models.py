from django.db import models
from django.core.mail import EmailMessage

class Contato(models.Model):
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField(default="1900-01-01")
    telefone = models.CharField(max_length=11)
    telefone_retorno = models.BooleanField(default=False)
    email = models.CharField(max_length=50)
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
        mail.send()


class Pensamento(models.Model):
    conteudo = models.CharField(max_length=50)
    autoria = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    favorito = bool()

    def __str__(self):
        return self.autoria
