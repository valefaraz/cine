# Generated by Django 3.1.1 on 2020-12-11 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cine', '0004_auto_20201209_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proyeccion',
            old_name='Pelicula',
            new_name='pelicula',
        ),
    ]
