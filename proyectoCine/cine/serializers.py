from rest_framework import serializers
from cine.models import Pelicula, Proyeccion, Sala, Butacas


class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ('id',
                  'name',
                  'duration',
                  'description',
                  'detail',
                  'gender',
                  'classification',
                  'status',
                  'start_date',
                  'end_date')


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ('id',
                  'name',
                  'status',
                  'row',
                  'seat')


class ProyeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyeccion
        fields = ('id',
                  'start_date',
                  'end_date',
                  'time',
                  'status',
                  'Pelicula',
                  'sala')


class ButacasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Butacas
        fields = ('id',
                  'date',
                  'row',
                  'seat',
                  'proyeccion')
