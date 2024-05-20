from datetime import datetime
from random import randrange
from typing import Any
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from user.authentication import (
    authenticate,
    generateToken,
    getAuthenticatedUser,
    verifyToken,
)
from .models import UserEntity
from .repositories import UserRepository
from .serializers import UserSerializer
from .forms import UserForm, UserLoginForm, UserUpdateForm


class UserView(View):
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
        repository = UserRepository(collection_name="user")
        users = list(repository.getAll())
        serializer = UserSerializer(data=users, many=True)
        if serializer.is_valid():
            userModel = serializer.save()
            users = [
                {**obj, "id": obj.pop("_id")} if "_id" in obj else obj for obj in users
            ]
            for i in users:
                print(i["id"])
        else:
            print(serializer.errors)
        return render(request, "user_home.html", {"users": users})


class UserDeleteView(View):
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
        print(additional_value)
        userRepository = UserRepository("user")
        user = userRepository.findOneById(additional_value)
        userRepository.delete(user)
        return redirect("User View")


class UserUpdate(View):
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
        userForm = UserUpdateForm()

        return render(
            request, "user_update_form.html", {"form": userForm, "primary_key": pk}
        )

    def post(self, request, pk):
        if not self.authenticate:
            return redirect("Login")
        userForm = UserUpdateForm(request.POST)
        serializer = UserSerializer(data=userForm.data)
        serializer.is_valid(raise_exception=True)
        dados_preenchidos = {}
        for campo, valor in serializer.data.items():
            if valor is not None and valor != "":
                dados_preenchidos[campo] = valor
        repository = UserRepository(collection_name="user")
        repository.update(pk, dados_preenchidos)
        return redirect("User View")


class UserInsert(View):
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
        userForm = UserForm()

        return render(request, "user_form.html", {"form": userForm})

    def post(self, request):
        if not self.authenticate:
            return redirect("Login")
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            serializer = UserSerializer(data=userForm.data)
            if serializer.is_valid():
                repository = UserRepository(collection_name="user")
                repository.insert(serializer.data)
            else:
                print(serializer.errors)
        else:
            print(userForm.errors)

        return redirect("User View")


class UserLogin(View):
    def get(self, request):
        user_login_form = UserLoginForm()
        return render(request, "login.html", {"form": user_login_form})

    def post(self, request):
        userForm = UserForm(request.POST)
        data = userForm.data
        if userForm.is_valid():
            auth = authenticate(data["username"], data["password"])
            if auth:
                token = generateToken(str(auth["_id"]), auth["username"])
                response = redirect("Weather View")
                response.set_cookie("auth_token", token, max_age=3600)
            else:
                print("not")
        else:
            print(userForm.errors)
        return response
