# Generated by Django 4.1 on 2024-05-30 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tb", "0011_alter_endereco_complemento"),
    ]

    operations = [
        migrations.AddField(
            model_name="endereco",
            name="principal",
            field=models.BooleanField(default=False),
        ),
    ]
