# Generated by Django 5.0.3 on 2024-04-02 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contatos", "0004_alter_contato_data_nascimento"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Contato",
        ),
    ]
