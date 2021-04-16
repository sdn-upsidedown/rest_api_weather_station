from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import api_view

from .models import WeatherData
from .serializers import WeatherDataSerializer

from django.core.files import File

import os

from django.conf import settings

import json

# Create your views here.

@api_view(['GET', ])
def get_all_data(request):
    data = {}

    wheather_datas = WeatherData.objects.all()
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
