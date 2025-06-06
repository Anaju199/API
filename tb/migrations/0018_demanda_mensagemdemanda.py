# Generated by Django 3.2 on 2025-04-15 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0017_avaliacoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('status', models.CharField(choices=[('aberto', 'Aberto'), ('em-andamento', 'Em Andamento'), ('resolvido', 'Resolvido'), ('precisa-info', 'Precisa de Informação')], default='aberto', max_length=20)),
                ('cliente_id', models.CharField(max_length=255)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tb.usuario')),
            ],
            options={
                'ordering': ['-criado_em'],
            },
        ),
        migrations.CreateModel(
            name='MensagemDemanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('autor_id', models.CharField(max_length=255)),
                ('tipo_autor', models.CharField(choices=[('cliente', 'Cliente'), ('admin', 'Admin')], max_length=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('anexos', models.JSONField(blank=True, null=True)),
                ('demanda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensagens', to='tb.demanda')),
            ],
            options={
                'ordering': ['criado_em'],
            },
        ),
    ]
