# Generated by Django 3.2 on 2025-01-08 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rl', '0024_delete_aniversariantes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='programacao',
            unique_together={('data', 'nome', 'sociedade')},
        ),
        migrations.RemoveField(
            model_name='programacao',
            name='ano',
        ),
        migrations.RemoveField(
            model_name='programacao',
            name='dia',
        ),
        migrations.RemoveField(
            model_name='programacao',
            name='mes',
        ),
    ]
