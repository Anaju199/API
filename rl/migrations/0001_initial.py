# Generated by Django 4.1 on 2024-05-20 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ministerio",
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
                ("nome", models.CharField(max_length=50, unique=True)),
                ("lideres", models.CharField(max_length=100)),
                ("ano", models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name="Missionario",
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
                ("nome", models.CharField(max_length=50, unique=True)),
                ("campo", models.CharField(max_length=50)),
                ("familia", models.CharField(blank=True, max_length=200)),
                ("foto", models.ImageField(blank=True, upload_to="missionarios/")),
                ("bandeira", models.ImageField(blank=True, upload_to="missionarios/")),
            ],
        ),
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
                ("login", models.CharField(max_length=100, unique=True)),
                ("senha", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Programacao",
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
                ("dia", models.CharField(max_length=2)),
                ("mes", models.CharField(max_length=2)),
                ("ano", models.CharField(max_length=4)),
                ("descricao", models.CharField(max_length=100, unique=True)),
                (
                    "sociedade",
                    models.CharField(
                        choices=[
                            ("UCP", "UCP"),
                            ("UPA", "UPA"),
                            ("UMP", "UMP"),
                            ("SAF", "SAF"),
                            ("UPH", "UPH"),
                            ("Igreja", "Igreja"),
                        ],
                        default="",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "unique_together": {("dia", "mes", "ano", "descricao", "sociedade")},
            },
        ),
        migrations.CreateModel(
            name="Lideranca",
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
                (
                    "cargo",
                    models.CharField(
                        choices=[
                            ("Diacono", "Diacono"),
                            ("Presbitero", "Presbitero"),
                            ("Pastor", "Pastor"),
                            ("Seminarista", "Seminarista"),
                        ],
                        default="",
                        max_length=50,
                    ),
                ),
                ("ano", models.CharField(max_length=4)),
                ("foto", models.ImageField(blank=True, upload_to="lideranca/")),
            ],
            options={
                "unique_together": {("nome", "cargo", "ano")},
            },
        ),
        migrations.CreateModel(
            name="FotosMinisterios",
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
                ("foto", models.ImageField(blank=True, upload_to="fotos_ministerios/")),
                (
                    "ministerio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rl.ministerio"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Diretoria",
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
                (
                    "sociedade",
                    models.CharField(
                        choices=[
                            ("UCP", "UCP"),
                            ("UPA", "UPA"),
                            ("UMP", "UMP"),
                            ("SAF", "SAF"),
                            ("UPH", "UPH"),
                        ],
                        default="",
                        max_length=3,
                    ),
                ),
                ("presidente", models.CharField(max_length=50)),
                ("vice_presidente", models.CharField(max_length=50)),
                ("pri_secretario", models.CharField(max_length=50)),
                ("seg_secretario", models.CharField(max_length=50)),
                ("tesoureiro", models.CharField(max_length=50)),
                ("ano", models.CharField(max_length=4)),
            ],
            options={
                "unique_together": {("sociedade", "ano")},
            },
        ),
    ]