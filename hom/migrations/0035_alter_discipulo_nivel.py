# Generated by Django 3.2 on 2025-04-04 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hom', '0034_auto_20250403_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipulo',
            name='nivel',
            field=models.CharField(choices=[('Iniciante', 'Iniciante'), ('Intermediario', 'Intermediario'), ('Avançado', 'Avançado')], max_length=50),
        ),
    ]
