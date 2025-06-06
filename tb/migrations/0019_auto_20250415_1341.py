# Generated by Django 3.2 on 2025-04-15 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0018_demanda_mensagemdemanda'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_vinculo', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tb.cliente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tb.usuario')),
            ],
            options={
                'unique_together': {('usuario', 'cliente')},
            },
        ),
        migrations.DeleteModel(
            name='Contato',
        ),
        migrations.AlterField(
            model_name='demanda',
            name='cliente_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tb.cliente'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuarios',
            field=models.ManyToManyField(related_name='clientes', through='tb.UsuarioCliente', to='tb.Usuario'),
        ),
    ]
