# Generated by Django 4.1 on 2024-10-10 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hom", "0008_alter_imagem_imagem_alter_produto_descricao_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="descricao",
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
