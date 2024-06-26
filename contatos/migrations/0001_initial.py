# Generated by Django 5.0.3 on 2024-03-26 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contato",
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
                ("nome", models.CharField(max_length=50)),
                ("cpf", models.CharField(max_length=11)),
                ("data_nascimento", models.DateField()),
                ("telefone", models.CharField(max_length=11)),
                ("email", models.CharField(max_length=50)),
            ],
        ),
    ]
