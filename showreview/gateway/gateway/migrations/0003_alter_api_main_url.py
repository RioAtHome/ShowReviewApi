# Generated by Django 4.0.6 on 2022-07-24 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0002_alter_api_main_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='main_url',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]