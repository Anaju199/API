# Generated by Django 4.1 on 2024-10-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hom", "0007_usuarioloja_administrador"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imagem",
            name="imagem",
            field=models.ImageField(blank=True, upload_to="pdt_imagens/"),
        ),
        migrations.AlterUniqueTogether(
            name="cor",
            unique_together={("produto", "cor")},
        ),
    ]
