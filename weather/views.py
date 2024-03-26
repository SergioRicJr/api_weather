from datetime import datetime
from random import randrange
from django.views import View
from django.shortcuts import render, redirect
from .models import WeatherEntity
from .repositories import WeatherRepository
from .serializers import WeatherSerializer
from .forms import WeatherForm


class WeatherView(View):
    def get(self, request):
        repository = WeatherRepository(collection_name="weathers")
        weathers = list(repository.getAll())
        serializer = WeatherSerializer(data=weathers, many=True)
        if serializer.is_valid():
            modelWeather = serializer.save()
            weathers = [
                {**obj, "id": obj.pop("_id")} if "_id" in obj else obj
                for obj in weathers
            ]
        else:
            print(serializer.errors)
        return render(request, "home.html", {"weathers": weathers})


class WeatherDeleteView(View):
    def post(self, request):
        additional_value = request.POST.get("additional_field")
        print(additional_value)
        weatherRepository = WeatherRepository("weathers")
        weather = weatherRepository.findOneById(additional_value)
        print(weather)
        weatherRepository.delete(weather)
        return redirect("Weather View")


class WeatherGenerate(View):
    def get(self, request):
        repository = WeatherRepository(collection_name="weathers")
        weather = WeatherEntity(
            temperature=randrange(start=17, stop=40),
            date=datetime.now(),
            city="Sorocaba",
        )
        serializer = WeatherSerializer(data=weather.__dict__)
        if serializer.is_valid():
            repository.insert(serializer.data)
        else:
            print(serializer.errors)

        return redirect("Weather View")


class WeatherReset(View):
    def get(self, request):
        repository = WeatherRepository(collection_name="weathers")
        repository.deleteAll()

        return redirect("Weather View")


class WeatherInsert(View):
    def get(self, request):
        weatherForm = WeatherForm()

        return render(request, "form.html", {"form": weatherForm})

    def post(self, request):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            if serializer.is_valid():
                repository = WeatherRepository(collection_name="weathers")
                repository.insert(serializer.data)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect("Weather View")
