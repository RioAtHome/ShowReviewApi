# Generated by Django 4.0.6 on 2022-07-24 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gateway", "0003_alter_api_main_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="api",
            name="main_url",
            field=models.URLField(max_length=255, unique=True),
        ),
    ]
