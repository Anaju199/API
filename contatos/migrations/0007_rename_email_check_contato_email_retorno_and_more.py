# Generated by Django 5.0.3 on 2024-04-06 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contatos", "0006_contato"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contato",
            old_name="email_check",
            new_name="email_retorno",
        ),
        migrations.RenameField(
            model_name="contato",
            old_name="telefone_check",
            new_name="telefone_retorno",
        ),
    ]
