# Generated by Django 4.1 on 2024-10-08 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hom", "0006_itensproacos"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuarioloja",
            name="administrador",
            field=models.BooleanField(default=False),
        ),
    ]
