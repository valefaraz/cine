from django.contrib import admin
from cine.models import *

# Register your models here.

#admin.site.register(Pelicula)
#admin.site.register(Sala)
#admin.site.register(Proyeccion)
#admin.site.register(Butacas)
#admin.site.register(ButacasAdmin)



class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('pk','name','start_date', 'end_date', 'status')
    list_filter = ('status','start_date')


class SalaAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'row', 'seat')
    list_filter = ('status',)



class ProyeccionAdmin(admin.ModelAdmin):
    list_display = ('pk','sala','pelicula','start_date', 'end_date', 'status')
    list_filter = ('status', 'pelicula')



class ButacasAdmin(admin.ModelAdmin):
    list_display = ('pk','proyeccion','date', 'row', 'seat')
    list_filter = ('date', 'proyeccion')


admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Proyeccion, ProyeccionAdmin)
admin.site.register(Butacas, ButacasAdmin)
