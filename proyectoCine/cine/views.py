from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from cine.models import Pelicula, Proyeccion, Sala, Butacas
from cine.serializers import PeliculaSerializer, SalaSerializer, ProyeccionSerializer, ButacasSerializer
from rest_framework.decorators import api_view
from datetime import datetime, timedelta, date
import operator


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
    try:
        pelicula = Pelicula.objects.get(pk=pk)
        inicio = request.GET.get('fecha', None)
        fin = datetime.strptime(str(pelicula.end_date), "%Y-%m-%d")

    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'La pelicula no existe'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        if inicio is not None:
            inicio = datetime.strptime(inicio, "%Y-%m-%d")
            pelicula_serializer = PeliculaSerializer(pelicula)
            lista_fechas = ["Fechas en cartelera: "]
            lista_fechas += [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((fin - inicio).days + 1)] 
            if len(lista_fechas) == 1:
                lista_fechas += ["No se encuentra disponible"]
            return JsonResponse((pelicula_serializer.data, lista_fechas), safe=False)
        else:
            pelicula_serializer = PeliculaSerializer(pelicula)
            return JsonResponse(pelicula_serializer.data, safe=False)
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
        return JsonResponse({'Mensaje': 'La Pelicula fue borrada con exito'},
                            status=status.HTTP_204_NO_CONTENT)

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



@api_view(['GET','POST'])
def proyecciones_list(request):
    try:
        inicio_in = request.GET.get('inicio', None)
        fin_in = request.GET.get('fin', None)
        dia = request.GET.get('dia', None)
        name = request.GET.get('name', None)
    except ValueError:
        pass

    fecha_actual = date.today()
    proyecciones = Proyeccion.objects.all()
    
    if request.method == 'GET':
        if dia is not None and name is not None:
            peliculas = Pelicula.objects.all()
            proyecciones_list = []
            sala_list = []
            pelicula_list=[]
            butaca_list = []
            for proyeccion in proyecciones:
                lista_fechas = [(proyeccion.start_date + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((proyeccion.end_date - proyeccion.start_date).days + 1)]
                pelicula = Pelicula.objects.get(id=proyeccion.pelicula.pk)
                sala = Sala.objects.get(id=proyeccion.sala.pk)
                butacas = Butacas.objects.filter(proyeccion=proyeccion.pk)
                if dia in lista_fechas:
                    if proyeccion.status == "activa":
                        if pelicula.status == "activa":
                            if sala.status == "habilitada":
                                if pelicula.name == name:
                                    proyecciones_list.append(proyeccion)
                                    sala_list.append(sala)
                                    pelicula_list.append(pelicula)
                                    for butaca in butacas:
                                        if str(butaca.date) == dia:
                                            butaca_list.append(butaca)

            proyecciones_serializer = ProyeccionSerializer(proyecciones_list, many=True)
            sala_serializer = SalaSerializer(sala_list, many=True)
            pelicula_serializer = PeliculaSerializer(pelicula_list, many=True)
            butacas_serializer = ButacasSerializer(butaca_list, many=True)
            if len(proyecciones_list) == 0:
                proyecciones_list= ["No existe proyeccion de esa pelicula para el dia seleccionado",]
                return JsonResponse(proyecciones_list, safe=False, status=status.HTTP_200_OK)
            return JsonResponse((proyecciones_serializer.data,sala_serializer.data,
                                pelicula_serializer.data,["Butacas Reservadas:"]+butacas_serializer.data), safe=False, status=status.HTTP_200_OK)


        elif inicio_in is not None and fin_in is not None:
            inicio = datetime.strptime(inicio_in,"%Y-%m-%d")
            fin = datetime.strptime(fin_in,"%Y-%m-%d")
            proyecciones_list = []
            for proyeccion in proyecciones:
                lista_fechas_ingresadas = [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((fin - inicio).days + 1)]
                lista_fechas = [(proyeccion.start_date + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((proyeccion.end_date - proyeccion.start_date).days + 1)]
                pelicula = Pelicula.objects.get(id=proyeccion.pelicula.pk)
                sala = Sala.objects.get(id=proyeccion.sala.pk)
                
                if len(lista_fechas) > len(lista_fechas_ingresadas):
                    a=inicio_in
                    b=fin_in
                    x=lista_fechas
                if len(lista_fechas) <= len(lista_fechas_ingresadas):
                    a=proyeccion.start_date
                    b=proyeccion.end_date
                    x=lista_fechas_ingresadas
                if str(a) in x or str(b) in x:
                    if proyeccion.status == "activa":
                        if pelicula.status == "activa":                    
                            if sala.status == "habilitada":
                                proyecciones_list.append(proyeccion)
        else:
            proyecciones_list = []
            for proyeccion in proyecciones:
                lista_fechas = [(proyeccion.start_date + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((proyeccion.end_date - proyeccion.start_date).days + 1)]
                pelicula = Pelicula.objects.get(id=proyeccion.pelicula.pk)
                sala = Sala.objects.get(id=proyeccion.sala.pk)
                if str(fecha_actual) in lista_fechas:
                    if proyeccion.status == "activa":
                        if pelicula.status == "activa":
                            if sala.status == "habilitada":
                                #if proyeccion.end_date > fecha_actual >= proyeccion.start_date:
                                proyecciones_list.append(proyeccion)

        proyecciones_serializer = ProyeccionSerializer(proyecciones_list, many=True)
        return JsonResponse(proyecciones_serializer.data, safe=False, status=status.HTTP_200_OK)

    
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
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La proyeccion no existe'},
                            status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        proyeccion_serializer = ProyeccionSerializer(proyeccion)
        return JsonResponse(proyeccion_serializer.data)

    elif request.method == 'PUT':
        proyeccion_data = JSONParser().parse(request)         #json con los datos nuevos
        proyeccion_serializer = ProyeccionSerializer(proyeccion, data=proyeccion_data)
        if proyeccion_serializer.is_valid():
            proyeccion_serializer.save()
            return JsonResponse(proyeccion_serializer.data)
        return JsonResponse(proyeccion_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        proyeccion.delete()
        return JsonResponse({'Mensaje': 'La Proyeccion fue borrada con exito'},
                            status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def butacas_list(request):

    if request.method == 'GET':
        butacas = Butacas.objects.all()
        butacas_serializer = ButacasSerializer(butacas, many=True)
        return JsonResponse(butacas_serializer.data, safe=False, status=status.HTTP_200_OK)

    if request.method == "POST":
        butaca_data = JSONParser().parse(request)
        butacas_serializer = ButacasSerializer(data=butaca_data)
        return posteo(butaca_data, butacas_serializer)
        

@api_view(['GET', 'PUT','DELETE'])
def butacas_detail(request, pk):
    try:
        butaca = Butacas.objects.get(pk=pk)
    except Butacas.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Butaca especificada no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        butaca_serializer = ButacasSerializer(butaca)
        return JsonResponse(butaca_serializer.data, safe=False, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        butaca_data = JSONParser().parse(request)         #json con los datos nuevos
        butacas_serializer = ButacasSerializer(butaca, data=butaca_data)
        return posteo(butaca_data, butacas_serializer)

    elif request.method == 'DELETE':
        butaca.delete()
        return JsonResponse({'Mensaje': 'La Butaca fue borrada con exito'},
                            status=status.HTTP_204_NO_CONTENT)


def posteo(butaca_data, butacas_serializer):
    if butacas_serializer.is_valid():
        proyeccion = Proyeccion.objects.get(pk=butaca_data["proyeccion"])
        sala = Proyeccion.objects.get(pk=butaca_data["proyeccion"]).sala
        if int(butaca_data["row"]) <= int(sala.row) and int(butaca_data["seat"]) <= int(sala.seat):
            if proyeccion.status == 'activa':
                if (datetime.strptime(str(proyeccion.end_date),"%Y-%m-%d") > 
                    datetime.strptime(butaca_data["date"],"%Y-%m-%d") >= 
                    datetime.strptime(str(proyeccion.start_date),"%Y-%m-%d")):
                    num_vendidas = contador = 0
                    vendidas = Butacas.objects.filter(proyeccion=butaca_data["proyeccion"])
                    for butacas in vendidas:
                        num_vendidas = len(vendidas)
                        if butacas.row == butaca_data["row"] and butacas.seat != butaca_data["seat"]:
                            contador += 1
                        if butacas.row != butaca_data["row"] and butacas.seat == butaca_data["seat"]:
                            contador += 1
                        if butacas.row != butaca_data["row"] and butacas.seat != butaca_data["seat"]:
                            contador += 1
                        if butacas.row == butaca_data["row"] and butacas.seat == butaca_data["seat"] and str(butacas.date) != butaca_data["date"]:
                            contador += 1
                    if contador == num_vendidas:
                        butacas_serializer.save()
                        return JsonResponse(butacas_serializer.data,
                                                status=status.HTTP_201_CREATED)
                    else:
                        return JsonResponse({'Mensaje': 'La Butaca ya fue vendida'}, 
                                            status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'Mensaje': 'No hay proyeccion para ese dia'}, 
                                        status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({'Mensaje': 'La proyeccion no esta activa'}, 
                                    status=status.HTTP_404_NOT_FOUND)
    return JsonResponse(butacas_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def reporte_vendidas(request, pk=0):

    butacas = Butacas.objects.all()
    butacas_list = []
    
    try:

        inicio = datetime.strptime(request.GET.get('inicio', None), "%Y-%m-%d")
        fin = datetime.strptime(request.GET.get('fin', None), "%Y-%m-%d")
        lista_fechas_u = [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((fin - inicio).days + 1)]
    except TypeError:
        return JsonResponse({'Message': 'The query is wrong'}, status=status.HTTP_404_NOT_FOUND)

    if inicio is not None and fin is not None and pk == 0:
        for butaca in butacas:
            if str(butaca.date) in lista_fechas_u:
                butacas_list.append(butaca)

    if pk != 0:
        try:
            butacas = Butacas.objects.filter(proyeccion=pk)
            for butaca in butacas:
                if str(butaca.date) in lista_fechas_u:
                    butacas_list.append(butaca)
        except Butacas.DoesNotExist:
            return JsonResponse({'Mensaje': 'La proyeccion no vendio butacas'}, status=status.HTTP_404_NOT_FOUND)

    if len(butacas_list) == 0:
        butacas_list = ["No hubo venta de butacas en ese rango"]
        return JsonResponse(butacas_list, safe=False, status=status.HTTP_200_OK)

    butacas_serializer = ButacasSerializer(butacas_list, many=True)
    return JsonResponse(["Entradas vendidas:",len(butacas_list)]+butacas_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def reporte_peliculas(request):
    peliculas = Pelicula.objects.all()
    butacas = Butacas.objects.all()
    butacas_dic={}
    entradas_list=[]
    contador = 0
    x=0

    for butaca in butacas:
        proyeccion = butaca.proyeccion
        pelicula = Pelicula.objects.get(pk=proyeccion.pelicula.pk)
        print(pelicula.name, pelicula.status)

        if pelicula.status == "activa":    
            if proyeccion.pk != x and pelicula.name not in butacas_dic:
                contador = 1
                butacas_dic[pelicula.name] = contador
                x = proyeccion.pk
            else:
                butacas_dic[pelicula.name] += contador

    return JsonResponse(butacas_dic, safe=False, status=status.HTTP_200_OK)
        

@api_view(['GET'])
def reportes_top_5(request):
    butacas = Butacas.objects.all()
    butacas_fecha = []
    butacas_dic = {}
    x = 0
    contador = 0

    try:
        inicio = datetime.strptime(request.GET.get('inicio', None), "%Y-%m-%d")
        fin = datetime.strptime(request.GET.get('fin', None), "%Y-%m-%d")
        lista_fechas_u = [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((fin - inicio).days + 1)]
    except TypeError:
        return JsonResponse({'Message': 'The query is wrong'}, status=status.HTTP_404_NOT_FOUND)

    # Filtrado por fechas:
    if inicio is not None and fin is not None:
        for butaca in butacas:
            if str(butaca.date) in lista_fechas_u:
                butacas_fecha.append(butaca)

        for butaca in butacas_fecha:
            proyeccion = butaca.proyeccion
            pelicula = Pelicula.objects.get(pk=proyeccion.pelicula.pk)

            if proyeccion.pk != x and pelicula.name not in butacas_dic:
                butacas_dic[pelicula.name] = 1
                x = proyeccion.pk
            else:
                butacas_dic[pelicula.name] += 1

        butacas_ord = dict(sorted(butacas_dic.items(), key=operator.itemgetter(1), reverse=True))
        butacas_fecha = {}
        for elemento in butacas_ord.items():
            contador += 1
            if contador <= 5:
                butacas_fecha[elemento[0]] = elemento[1]

        d3 = {**{"Ranking de proyecciones":"5"}, **butacas_fecha}
    return JsonResponse(d3, safe=False, status=status.HTTP_200_OK)