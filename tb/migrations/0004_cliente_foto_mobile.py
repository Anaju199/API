# Generated by Django 4.1 on 2024-05-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tb", "0003_alter_cliente_foto"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="foto_mobile",
            field=models.ImageField(blank=True, upload_to="fotos/clientes/"),
        ),
    ]