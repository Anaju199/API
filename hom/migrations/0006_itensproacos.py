# Generated by Django 4.1 on 2024-10-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hom", "0005_alter_usuariopersonal_senha_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ItensProAcos",
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
                ("item", models.CharField(blank=True, max_length=30)),
                ("quant", models.IntegerField(blank=True)),
                ("datalote", models.DateField(blank=True)),
                ("datavenda", models.DateField(blank=True)),
            ],
        ),
    ]
