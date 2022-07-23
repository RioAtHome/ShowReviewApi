# Generated by Django 4.0.6 on 2022-07-23 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('rel_url', models.CharField(max_length=255)),
                ('main_url', models.CharField(max_length=255)),
            ],
        ),
    ]
