from datetime import datetime
from random import randrange
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from .models import UserEntity
from .repositories import UserRepository
from .serializers import UserSerializer
from .forms import UserForm, UserUpdateForm


class UserView(View):
    def get(self, request):
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
    def post(self, request):
        additional_value = request.POST.get("additional_field")
        print(additional_value)
        userRepository = UserRepository("user")
        user = userRepository.findOneById(additional_value)
        userRepository.delete(user)
        return redirect("User View")


class UserUpdate(View):
    def get(self, request, pk):
        userForm = UserUpdateForm()

        return render(
            request, "user_update_form.html", {"form": userForm, "primary_key": pk}
        )

    def post(self, request, pk):
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
    def get(self, request):
        userForm = UserForm()

        return render(request, "user_form.html", {"form": userForm})

    def post(self, request):
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
