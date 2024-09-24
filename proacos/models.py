from django.db import models

class ItensProAcos(models.Model):
    item = models.CharField(max_length=30, blank=True)
    quant = models.IntegerField(blank=True)
    datalote = models.DateField(blank=True)
    datavenda = models.DateField(blank=True)

    def __str__(self):
        return self.item

    class Meta:
        app_label = 'proacos'
        managed = False
        db_table = 'itens'

