from django.http.response import HttpResponse
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.teste, name='teste')
]