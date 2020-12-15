from django.conf.urls import url
from cine import views

urlpatterns = [
    url(r'^api/peliculas$', views.peliculas_list),
    url(r'^api/peliculas/(?P<pk>[0-9]+)$', views.peliculas_detail),

    url(r'^api/salas$', views.salas_list),
    url(r'^api/salas/(?P<pk>[0-9]+)$', views.salas_detail),

    url(r'^api/proyecciones$', views.proyecciones_list),
    url(r'^api/proyecciones/(?P<pk>[0-9]+)$', views.proyecciones_detail),

    url(r'^api/butacas$', views.butacas_list),
    url(r'^api/butacas/(?P<pk>[0-9]+)$', views.butacas_detail),

    url(r'^api/reportes$', views.reporte_vendidas),
    url(r'^api/reportes/(?P<pk>[0-9]+)$', views.reporte_vendidas),
    url(r'^api/reportes/peliculas$', views.reporte_peliculas),
    url(r'^api/reportes/ranking$', views.reportes_top_5)




]
