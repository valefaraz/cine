# Generated by Django 3.1.1 on 2020-10-10 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='duration',
            field=models.IntegerField(),
        ),
    ]