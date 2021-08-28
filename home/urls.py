# Author: Chenchen
from django.contrib import admin
from django.urls import path, include
from home import views
urlpatterns = [
    path('data/', views.Data.as_view() ),
    path('multidata/', views.Multidata.as_view() ),
]
