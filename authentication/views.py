# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth import authenticate, login
# Create your views here.
from django.shortcuts import render, redirect

from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    correct_credentials = True
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                correct_credentials = False

    return render(request, "accounts/login.html",
                  {"form": form, 'correct_credentials': correct_credentials})


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form})
