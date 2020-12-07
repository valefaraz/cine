from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from cine.models import Pelicula, Proyeccion, Sala, Butacas
from cine.serializers import PeliculaSerializer, SalaSerializer, ProyeccionSerializer, ButacasSerializer
from rest_framework.decorators import api_view
from datetime import datetime, timedelta, date

@api_view(['GET', 'POST'])
def peliculas_list(request):
    if request.method == 'GET':
        pelicula = Pelicula.objects.all()
        name = request.GET.get('name', None)
        rango = request.GET.get('rango',None)
        if name is not None:
            pelicula = pelicula.filter(name__icontains=name)
        if rango is not None:
            pelicula = pelicula.filter(end_date__gte=(datetime.now()-timedelta(days=int(rango))),
                                       start_date__lte=(datetime.now()+timedelta(days=int(rango))))

        pelicula_serializer = PeliculaSerializer(pelicula, many=True)
        return JsonResponse(pelicula_serializer.data, safe=False)
    elif request.method == 'POST':
        pelicula_data = JSONParser().parse(request)
        pelicula_serializer = PeliculaSerializer(data=pelicula_data)
        print(pelicula_serializer)
        if pelicula_serializer.is_valid():
            pelicula_serializer.save()
            return JsonResponse(pelicula_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(pelicula_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def peliculas_detail(request, pk):
    # find tutorial by pk (id)
    try:
        pelicula = Pelicula.objects.get(pk=pk)
        inicio = datetime.strptime(request.GET.get('fecha', None), "%Y-%m-%d")
        fin = datetime.strptime(str(pelicula.end_date), "%Y-%m-%d")
    except Pelicula.DoesNotExist:
        return JsonResponse({'Message': 'The Film does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        pelicula_serializer = PeliculaSerializer(pelicula)
        lista_fechas = ["Fechas en cartelera: "]
        lista_fechas += [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((fin - inicio).days + 1)] 
        if len(lista_fechas) == 1:
            lista_fechas += ["No se encuentra disponible"]
        return JsonResponse((pelicula_serializer.data, lista_fechas), safe=False)

    elif request.method == 'PUT':
        pelicula_data = JSONParser().parse(request)
        pelicula_serializer = PeliculaSerializer(pelicula, data=pelicula_data)
        if pelicula_serializer.is_valid():
            pelicula_serializer.save()
            return JsonResponse(pelicula_serializer.data)
        return JsonResponse(pelicula_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pelicula.delete()
        return JsonResponse({'message': 'Pelicula was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
    #elif request.method == 'DELETE':
    #    count = Pelicula.objects.all().delete()
    #    return JsonResponse({'message': '{} Tutorials were deleted'
    #                        'successfully!'.format(count[0])},
    #                        status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def salas_list(request):
    if request.method == 'GET':
        sala = Sala.objects.all()
        name = request.GET.get('name', None)
        if name is not None:
            sala = sala.filter(name__icontains=name)
        sala_serializer = SalaSerializer(sala, many=True)
        return JsonResponse(sala_serializer.data, safe=False)
    
    elif request.method == 'POST':
        sala_data = JSONParser().parse(request)
        sala_serializer = SalaSerializer(data=sala_data)
        print(sala_serializer)
        if sala_serializer.is_valid():
            sala_serializer.save()
            return JsonResponse(sala_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(sala_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def salas_detail(request, pk):
    try:
        sala = Sala.objects.get(pk=pk)
    except Sala.DoesNotExist:
        return JsonResponse({'message': 'La Sala no existe'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sala_serializer = SalaSerializer(sala)
        return JsonResponse(sala_serializer.data)

    elif request.method == 'PUT':
        sala_data = JSONParser().parse(request)         #json con los datos nuevos

        sala_serializer = SalaSerializer(sala, data=sala_data)
        
        if sala_serializer.is_valid():
            sala_serializer.save()
            return JsonResponse(sala_serializer.data)
        return JsonResponse(sala_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if sala.status == "eliminada":
            sala.delete()
            return JsonResponse({'message': 'Sala was deleted successfully!'},
                    status=status.HTTP_204_NO_CONTENT)
        sala.status = "eliminada"
        sala.save()
        return JsonResponse({'message': 'La sala cambio a estado eliminada'},
                            status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST', 'DELETE'])
def proyecciones_list(request):
    
    fecha_actual = date.today()
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.all()
        proyecciones_list = []
        for proyeccion in proyecciones:
            pelicula = Pelicula.objects.get(id=proyeccion.Pelicula.pk)
            if proyeccion.status == "activa":
                if pelicula.status == "activa":
                    if proyeccion.end_date > fecha_actual >= proyeccion.start_date:
                        proyecciones_list.append(proyeccion)
        proyecciones_serializer = ProyeccionSerializer(proyecciones_list, many=True)
        return JsonResponse(proyecciones_serializer.data, safe=False, status=status.HTTP_200_OK)

    #if request.method == 'GET':
    #    proyeccion = Proyeccion.objects.all()
        #name = request.GET.get('name', None)
        #if name is not None:
        #    sala = sala.filter(name__icontains=name)
    #    proyeccion_serializer = ProyeccionSerializer(proyeccion, many=True)
    #    return JsonResponse(proyeccion_serializer.data, safe=False)
    
    elif request.method == 'POST':
        proyeccion_data = JSONParser().parse(request)
        proyeccion_serializer = ProyeccionSerializer(data=proyeccion_data)
        print(proyeccion_serializer)
        if proyeccion_serializer.is_valid():
            proyeccion_serializer.save()
            return JsonResponse(proyeccion_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(proyeccion_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def proyecciones_detail(request, pk):
    pass