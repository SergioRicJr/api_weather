from django.urls import path
from weather.views import (
    WeatherDeleteView,
    WeatherView,
    WeatherGenerate,
    WeatherReset,
    WeatherInsert,
    WeatherUpdate,
)
from user.views import UserDeleteView, UserInsert, UserLogin, UserUpdate, UserView

urlpatterns = [
    path("", WeatherView.as_view(), name="Weather View"),
    path("insert", WeatherInsert.as_view(), name="Weather Insert"),
    path("generate", WeatherGenerate.as_view(), name="Weather Generate"),
    path("reset", WeatherReset.as_view(), name="Weather Reset"),
    path("weather/delete/", WeatherDeleteView.as_view(), name="delete_weather"),
    path("update/<pk>", WeatherUpdate.as_view(), name="Weather Update"),
    path("user_insert", UserInsert.as_view(), name="User Insert"),
    path("users", UserView.as_view(), name="User View"),
    path("user/delete/", UserDeleteView.as_view(), name="User Delete View"),
    path("user_update/<pk>", UserUpdate.as_view(), name="User Update"),
    path("login", UserLogin.as_view(), name="Login")
]
