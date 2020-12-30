from django.db import models


class Pelicula(models.Model):
    name = models.CharField(max_length=70, blank=False)  # nombre (nombre de la película)
    duration = models.IntegerField()  # duración en minutos
    description = models.CharField(max_length=200)  # descripción breve
    detail = models.TextField()  # detalle de la película como actores, director, descripción más detallada
    gender = models.CharField(max_length=100)  # género de la película
    classification = models.CharField(max_length=50)  # tipo de película ATP, PG-13, etc.
    status = models.CharField(max_length=15)  # activo o no activo
    start_date = models.DateField()  # fecha desde cuando se encontrará disponible la película
    end_date = models.DateField()  # fecha hasta cuando se encuentra disponible la película

    class Meta:
        verbose_name = "Pelicula"
        verbose_name_plural = "Peliculas"
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Sala(models.Model):
    name = models.CharField(max_length=70, blank=False)  # nombre de la sala
    status = models.CharField(max_length=15)  # habilitada, deshabilitada, eliminada
    row = models.IntegerField()  # cantidad de filas que tiene la sala
    seat = models.IntegerField()  # cantidad de asientos que hay en una fila

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Proyeccion(models.Model):
    start_date = models.DateField()  # fecha desde cuando se comienza a proyectar
    end_date = models.DateField()  # fecha hasta cuando se proyecta la pelicula
    time = models.TimeField()  # hora de proyección
    status = models.CharField(max_length=10)  # activo o no activo
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Proyeccion"
        verbose_name_plural = "Proyecciones"
        ordering = ["pk"]


    def __str__(self):
        a = str(self.pk) + "->" + str(self.pelicula.name)
        return a


class Butacas(models.Model):
    proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE)
    date = models.DateField()  # fecha de la venta/reserva de la entrada
    row = models.IntegerField()  # fila dentro de la sala
    seat = models.IntegerField()  # asiento dentro de la fila

    class Meta:
        verbose_name = "Butaca"
        verbose_name_plural = "Butacas"
        ordering = ["pk"]