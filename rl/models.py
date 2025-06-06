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

    nome = models.CharField(max_length=100)
    data = models.DateField()
    descricao = models.CharField(max_length=300)
    sociedade = models.CharField(max_length=10, choices=OPCOES_SOCIEDADE, default='')

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = 'rl'
        unique_together = ['data', 'nome', 'sociedade']


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
    conselheiro = models.CharField(max_length=50)

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
        ("Presbitero","Presbitero")
    ]

    nome = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50, choices=OPCOES_CARGO, default='')
    ano_inicio = models.CharField(max_length=4, default='2024')
    ano_fim = models.CharField(max_length=4, default='2028')
    foto = models.ImageField(upload_to="lideranca/", blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'
        unique_together = ['nome', 'cargo', 'ano_inicio']



class Ministerio(models.Model):
    nome = models.CharField(max_length=50)
    lideres = models.CharField(max_length=100)
    ano = models.CharField(max_length=4)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'
        unique_together = ['nome', 'ano']


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
        ("UCP", "UCP"),
        ("UPA", "UPA"),
        ("UMP", "UMP"),
        ("SAF", "SAF"),
        ("UPH", "UPH")
    ]

    OPCOES_ESTADO_CIVIL = [
        ("SOLTEIRO", "Solteiro(a)"),
        ("CASADO", "Casado(a)"),
        ("DIVORCIADO", "Divorciado(a)"),
        ("VIÚVO", "Viúvo(a)"),
        ("SEPARADO", "Separado(a)"),
        ("UNIÃO ESTÁVEL", "União Estável"),
    ]

    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1)
    sociedade = models.CharField(max_length=3, choices=OPCOES_SOCIEDADE, default='', blank=True)
    status = models.CharField(max_length=20, default='', blank=True)
    numero_membro = models.CharField(max_length=10, default='', blank=True)  
    ativo = models.BooleanField(default=True)
    observacoes = models.CharField(max_length=300, default='', blank=True)  

    # Endereço
    rua = models.CharField(max_length=100, default='', blank=True)  
    numero = models.CharField(max_length=10, default='', blank=True)  
    bairro = models.CharField(max_length=50, default='', blank=True)  
    cep = models.CharField(max_length=15, default='', blank=True)  
    telefone = models.CharField(max_length=25, default='', blank=True)  

    # Informações pessoais
    nacionalidade = models.CharField(max_length=30, default='', blank=True)  
    naturalidade = models.CharField(max_length=30, default='', blank=True)  
    alfabetizado = models.BooleanField(default=True)
    estado_civil = models.CharField(max_length=20, choices=OPCOES_ESTADO_CIVIL, default='', blank=True)
    religiao_conjuge = models.CharField(max_length=50, default='', blank=True)  
    ocupacao = models.CharField(max_length=50, default='', blank=True)  

    cpf = models.CharField(max_length=11, default='', blank=True)  
    identidade = models.CharField(max_length=20, default='', blank=True)  

    # Opção de pai/mãe como membro
    pai = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='filhos_do_pai')
    mae = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='filhos_da_mae')
    conjuge = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='conjuge_de')

    # Opção de pai/mãe como texto
    pai_nome = models.CharField(max_length=50, blank=True, null=True)
    mae_nome = models.CharField(max_length=50, blank=True, null=True)
    conjuge_nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'



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
        app_label = 'rl'


class EscolaDominical(models.Model):
    classe = models.CharField(max_length=80, unique=True)
    professores = models.CharField(max_length=80)

    def __str__(self):
        return self.classe

    class Meta:
        app_label = 'rl'


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
        app_label = 'rl'
        unique_together = ['nome', 'cargo']

class RedesSociais(models.Model):
    OPCOES_REDE = [
        ("Instagram", "Instagram"),
        ("Facebook", "Facebook"),
        ("Whatsapp", "Whatsapp"),
        ("Youtube", "Youtube")
    ]

    responsavel = models.CharField(max_length=50)
    rede_social = models.CharField(max_length=50, choices=OPCOES_REDE)
    link = models.CharField(max_length=50)

    def __str__(self):
        return self.responsavel

    class Meta:
        app_label = 'rl'
        unique_together = ['responsavel', 'rede_social', 'link']


class Download(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    arquivo = models.FileField(upload_to='downloads/')

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'rl'


class Fotos(models.Model):
    ministerio = models.ForeignKey(Ministerio, on_delete=models.CASCADE, null=True, blank=True)
    programacao = models.ForeignKey(Programacao, on_delete=models.CASCADE, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos/', blank=True)
    descricao = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return f"{self.ministerio.nome if self.ministerio else ''} {self.programacao.nome if self.programacao else ''}".strip()

    class Meta:
        app_label = 'rl'