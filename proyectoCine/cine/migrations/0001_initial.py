# Generated by Django 3.1.1 on 2020-10-10 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('duration', models.IntegerField(max_length=10)),
                ('description', models.CharField(max_length=200)),
                ('detail', models.TextField()),
                ('gender', models.CharField(max_length=100)),
                ('classification', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=15)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('status', models.CharField(max_length=15)),
                ('row', models.IntegerField()),
                ('seat', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Proyeccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('time', models.DateTimeField()),
                ('status', models.CharField(max_length=10)),
                ('Pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cine.pelicula')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cine.sala')),
            ],
        ),
        migrations.CreateModel(
            name='Butacas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('row', models.IntegerField()),
                ('seat', models.IntegerField()),
                ('proyección', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cine.proyeccion')),
            ],
        ),
    ]