# Generated by Django 4.1 on 2024-10-10 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hom", "0010_alter_produto_descricao"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cor",
            unique_together=set(),
        ),
    ]
