from django.db import models
from django.contrib.auth.hashers import make_password

class Programacao(models.Model):
    OPCOES_SOCIEDADE = [
        ("UCP","UCP"),
        ("UPA","UPA"),
        ("UMP", "UMP"),
        ("SAF","SAF"),
        ("UPH","UPH"),
        ("Igreja","Igreja")
    ]

    dia = models.CharField(max_length=2)
    mes = models.CharField(max_length=2)
    ano = models.CharField(max_length=4)
    descricao = models.CharField(max_length=100, unique=True)
    sociedade = models.CharField(max_length=10, choices=OPCOES_SOCIEDADE, default='')

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = 'rl'
        unique_together = ['dia', 'mes', 'ano', 'descricao', 'sociedade']


class Diretoria(models.Model):
    OPCOES_SOCIEDADE = [
        ("UCP","UCP"),
        ("UPA","UPA"),
        ("UMP", "UMP"),
        ("SAF","SAF"),
        ("UPH","UPH")
    ]

    sociedade = models.CharField(max_length=3, choices=OPCOES_SOCIEDADE, default='')
    presidente = models.CharField(max_length=50)
    vice_presidente = models.CharField(max_length=50)
    pri_secretario = models.CharField(max_length=50)
    seg_secretario = models.CharField(max_length=50)
    tesoureiro = models.CharField(max_length=50)
    ano = models.CharField(max_length=4)

    def __str__(self):
        return self.sociedade

    class Meta:
        app_label = 'rl'
        unique_together = ['sociedade', 'ano']


class Missionario(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    campo = models.CharField(max_length=50)
    familia = models.CharField(max_length=200, blank=True)
    foto = models.ImageField(upload_to="missionarios_fotos/", blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'


class Lideranca(models.Model):
    OPCOES_CARGO = [
        ("Diacono","Diacono"),
        ("Presbitero","Presbitero"),
        ("Pastor", "Pastor"),
        ("Seminarista", "Seminarista")
    ]

    nome = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50, choices=OPCOES_CARGO, default='')
    ano = models.CharField(max_length=4)
    foto = models.ImageField(upload_to="lideranca/", blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'
        unique_together = ['nome', 'cargo', 'ano']



class Ministerio(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    lideres = models.CharField(max_length=100)
    ano = models.CharField(max_length=4)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'


class FotosMinisterios(models.Model):
    ministerio = models.ForeignKey(Ministerio, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_ministerios/', blank=True)

    def __str__(self):
        return self.ministerio.nome

    class Meta:
        app_label = 'rl'


class Usuario(models.Model):

    login = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
      if not self.pk or not Usuario.objects.filter(pk=self.pk, senha=self.senha).exists():
          self.senha = make_password(self.senha)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.login

    class Meta:
        app_label = 'rl'


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
        app_label = 'rl'


class Membros(models.Model):
    OPCOES_SOCIEDADE = [
        ("UCP","UCP"),
        ("UPA","UPA"),
        ("UMP", "UMP"),
        ("SAF","SAF"),
        ("UPH","UPH")
    ]

    nome = models.CharField(max_length=50, unique=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1)
    sociedade = models.CharField(max_length=3, choices=OPCOES_SOCIEDADE, default='', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'
