# Generated by Django 4.1 on 2024-05-29 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tb", "0005_remove_cliente_foto_mobile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                ("cpf", models.CharField(max_length=11)),
                ("email", models.CharField(max_length=100)),
                ("celular_pais", models.CharField(max_length=3)),
                ("celular_ddd", models.CharField(max_length=3)),
                ("celular_numero", models.CharField(max_length=10)),
                ("senha", models.CharField(max_length=128)),
            ],
        ),
    ]