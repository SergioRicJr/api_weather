from datetime import datetime
from random import randrange
from typing import Any
from django.http import HttpRequest
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect

from user.authentication import getAuthenticatedUser, verifyToken
from .models import WeatherEntity
from .repositories import WeatherRepository
from .serializers import WeatherSerializer
from .forms import WeatherForm, WeatherUpdateForm


class WeatherView(View):
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        cookie_token = request.COOKIES.get("auth_token", "Cookie not found")
        error_code, _ = verifyToken(cookie_token)
        print(error_code)

        if error_code == 0:
            user = getAuthenticatedUser(cookie_token)
            self.authenticate = True

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if not self.authenticate:
            return redirect("Login")
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
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        cookie_token = request.COOKIES.get("auth_token", "Cookie not found")
        error_code, _ = verifyToken(cookie_token)
        print(error_code)

        if error_code == 0:
            user = getAuthenticatedUser(cookie_token)
            self.authenticate = True

        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if not self.authenticate:
            return redirect("Login")
        additional_value = request.POST.get("additional_field")
        weatherRepository = WeatherRepository("weathers")
        weather = weatherRepository.findOneById(additional_value)
        weatherRepository.delete(weather)
        return redirect("Weather View")


class WeatherGenerate(View):
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        cookie_token = request.COOKIES.get("auth_token", "Cookie not found")
        error_code, _ = verifyToken(cookie_token)
        print(error_code)

        if error_code == 0:
            user = getAuthenticatedUser(cookie_token)
            self.authenticate = True

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if not self.authenticate:
            return redirect("Login")
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
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        cookie_token = request.COOKIES.get("auth_token", "Cookie not found")
        error_code, _ = verifyToken(cookie_token)
        print(error_code)

        if error_code == 0:
            user = getAuthenticatedUser(cookie_token)
            self.authenticate = True

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if not self.authenticate:
            return redirect("Login")
        repository = WeatherRepository(collection_name="weathers")
        repository.deleteAll()

        return redirect("Weather View")


class WeatherUpdate(View):
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        cookie_token = request.COOKIES.get("auth_token", "Cookie not found")
        error_code, _ = verifyToken(cookie_token)
        print(error_code)

        if error_code == 0:
            user = getAuthenticatedUser(cookie_token)
            self.authenticate = True

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        if not self.authenticate:
            return redirect("Login")
        weatherForm = WeatherUpdateForm()

        return render(
            request, "update_form.html", {"form": weatherForm, "primary_key": pk}
        )

    def post(self, request, pk):
        if not self.authenticate:
            return redirect("Login")
        weatherForm = WeatherUpdateForm(request.POST)
        serializer = WeatherSerializer(data=weatherForm.data)
        serializer.is_valid(raise_exception=True)
        dados_preenchidos = {}
        for campo, valor in serializer.data.items():
            if valor is not None and valor != "":
                dados_preenchidos[campo] = valor
        repository = WeatherRepository(collection_name="weathers")
        repository.update(pk, dados_preenchidos)
        return redirect("Weather View")


class WeatherInsert(View):
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        cookie_token = request.COOKIES.get("auth_token", "Cookie not found")
        error_code, _ = verifyToken(cookie_token)
        print(error_code)

        if error_code == 0:
            user = getAuthenticatedUser(cookie_token)
            self.authenticate = True

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if not self.authenticate:
            return redirect("Login")
        weatherForm = WeatherForm()

        return render(request, "form.html", {"form": weatherForm})

    def post(self, request):
        if not self.authenticate:
            return redirect("Login")
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
