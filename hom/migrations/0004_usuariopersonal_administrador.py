# Generated by Django 4.1 on 2024-09-20 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hom", "0003_alter_usuariopersonal_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuariopersonal",
            name="administrador",
            field=models.BooleanField(default=False),
        ),
    ]