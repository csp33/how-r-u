# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from web_interface.app import views

urlpatterns = [
    # Homepage
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about_me/', views.about_me, name='about_me'),

]
