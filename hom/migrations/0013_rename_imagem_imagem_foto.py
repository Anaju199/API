# Generated by Django 4.1 on 2024-10-10 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hom", "0012_alter_produto_descricao_alter_cor_unique_together"),
    ]

    operations = [
        migrations.RenameField(
            model_name="imagem",
            old_name="imagem",
            new_name="foto",
        ),
    ]