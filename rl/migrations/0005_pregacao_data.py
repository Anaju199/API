# Generated by Django 4.1 on 2024-06-08 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rl", "0004_pregacao"),
    ]

    operations = [
        migrations.AddField(
            model_name="pregacao",
            name="data",
            field=models.DateField(blank=True, default="1900-01-01"),
        ),
    ]