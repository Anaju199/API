from rest_framework import serializers
from rl.models import Programacao, Diretoria, Ministerio, Missionario, Lideranca, FotosMinisterios, Usuario, Pregacao, Membros

class ProgramacaoSerializer(serializers.ModelSerializer):
    class Meta:
      model = Programacao
      fields = ('id', 'dia', 'mes','ano','descricao','sociedade')

class DiretoriaSerializer(serializers.ModelSerializer):
   class Meta:
      model = Diretoria
      fields = ('id','sociedade','presidente','vice_presidente','pri_secretario', 'seg_secretario', 'tesoureiro','ano','instagram')

class MissionarioSerializer(serializers.ModelSerializer):
   class Meta:
      model = Missionario
      fields = ('id','nome','campo','familia','foto')

class LiderancaSerializer(serializers.ModelSerializer):
   class Meta:
      model = Lideranca
      fields = ('id','nome','cargo','ano', 'foto')

class MinisterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministerio
        fields = ('id', 'nome', 'lideres', 'ano')

class FotosMinisteriosSerializer(serializers.ModelSerializer):
    # Adicione um campo de leitura para mostrar o nome do ministério
    ministerio_nome = serializers.ReadOnlyField(source='ministerio.nome')

    class Meta:
        model = FotosMinisterios
        fields = ('id', 'ministerio', 'ministerio_nome', 'foto')

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'login', 'senha')

class PregacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregacao
        fields = ('id', 'descricao', 'link','data')

class MembrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membros
        fields = ('id', 'nome', 'data_nascimento','sexo','sociedade', 'status')
