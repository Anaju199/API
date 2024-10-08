# Generated by Django 4.1 on 2024-09-12 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rl", "0009_igreja"),
    ]

    operations = [
        migrations.CreateModel(
            name="EscolaDominical",
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
                ("classe", models.CharField(max_length=80, unique=True)),
                ("professores", models.CharField(max_length=80)),
            ],
        ),
        migrations.AddField(
            model_name="igreja",
            name="tipo_chave_pix",
            field=models.CharField(blank=True, default="CNPJ", max_length=20),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="agencia",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="chave_pix",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="conta_corrente",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="email",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="instagram",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="nome_banco",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="num_banco",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="igreja",
            name="youtube",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
