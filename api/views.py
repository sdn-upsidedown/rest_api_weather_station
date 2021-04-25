import json
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files import File
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WeatherData
from .serializers import WeatherDataSerializer

# Create your views here.

@api_view(['GET', ])
def get_all_data(request):
    data = {}

    wheather_datas = WeatherData.objects.all().order_by('-date')
    serializer = {}

    if request.method == "GET":
        for i in range(len(wheather_datas)):
            serializer[i] = WeatherDataSerializer(wheather_datas[i]).data
        return Response(serializer, status=status.HTTP_200_OK)

    data['error'] = "Bad Request"
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def get_last_n(request):

    data = {}

    try:
        records_number = int(request.data['records_number'])
    except:
        records_number = 50

    wheather_datas = WeatherData.objects.all().order_by('-date')[:records_number]

    serializer = {}

    if request.method == "GET":
        for i in range(len(wheather_datas)):
            serializer[i] = WeatherDataSerializer(wheather_datas[i]).data
        return Response(serializer, status=status.HTTP_200_OK)

    data['error'] = "Bad Request"
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def get_timed_data(request):
    data = {}

    now = datetime.now()

    year = timedelta()

    default = timedelta(days=365*4) + timedelta(days=30)
    # default = timedelta(days=5)

    try:
        from_date = request.data['from_date']
    except:
        from_date = now - default
    
    try:
        to_date = request.data['to_date']
    except:
        to_date = now

    to_date = make_aware(to_date)
    from_date = make_aware(from_date)

    print("{} -> {}".format(from_date, to_date))

    wheather_datas = WeatherData.objects.filter(date__gte=from_date, date__lte=to_date) # date__lte=from_date, date__gte=to_date

    serializer = {}

    if request.method == "GET":
        for i in range(len(wheather_datas)):
            serializer[i] = WeatherDataSerializer(wheather_datas[i]).data
        return Response(serializer, status=status.HTTP_200_OK)

    data['error'] = "Bad Request"
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def post_base_data(request):
    data = {}

    # Ouverture des données JSON
    file_path = os.path.join(settings.STATIC_ROOT, 'base_datas.json')
    base_data = open(file_path, 'r')
    
    inc = 0

    if request.method == 'POST':
        for element in base_data:
            # On transforme l'élément en données json
            d = json.loads(element)

            data[inc] = d

            # On récupère les éléments qui nous intéresse
            try:
                humidity = d["humidity"]
            except:
                pressure = None

            try:
                pressure = d["pressure"]
            except:
                pressure = None

            try:
                light = d["light"]
            except:
                light = None

            try:
                temperature = d["temperature"]
            except:
                temperature = None

            date = d["date"]["$date"]

            # On ajoute l'occurence dans la base de données
            new_weather_data_object = WeatherData(
                humidity=humidity,
                pressure=pressure,
                temperature=temperature,
                light=light,
                date=date
            )

            new_weather_data_object.save()
            
            # print("Adding {}".format(d))

            # Tests

            # print("{} {} {} {} {}\n".format(humidity, pressure, light, temperature, date))

            inc += 1

            if inc == 1000:
                return Response(data)


    # Pour chaque ligne insertion dans la base de données
    return Response(data)

@api_view(['DELETE', ])
def delete_all(request):
    data = {"Data deleted"}

    datas = WeatherData.objects.all().delete()

    return Response(data)
