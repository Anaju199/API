from rest_framework import serializers
from proacos.models import ItensProAcos

class ItensProAcosSerializer(serializers.ModelSerializer):
    class Meta:
      model = ItensProAcos
      fields = ('id', 'item','quant', 'datalote','datavenda')
