from django.urls import path
from weather.views import (
    WeatherDeleteView,
    WeatherView,
    WeatherGenerate,
    WeatherReset,
    WeatherInsert,
)

urlpatterns = [
    path("", WeatherView.as_view(), name="Weather View"),
    path("insert", WeatherInsert.as_view(), name="Weather Insert"),
    path("generate", WeatherGenerate.as_view(), name="Weather Generate"),
    path("reset", WeatherReset.as_view(), name="Weather Reset"),
    path("weather/delete/", WeatherDeleteView.as_view(), name="delete_weather"),
]
