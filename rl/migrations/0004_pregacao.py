# Generated by Django 4.1 on 2024-06-08 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rl", "0003_remove_missionario_bandeira_alter_missionario_foto"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pregacao",
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
                ("descricao", models.CharField(max_length=100, unique=True)),
                ("link", models.CharField(max_length=100)),
            ],
        ),
    ]