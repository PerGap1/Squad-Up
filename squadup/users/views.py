from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *


class UserListView(ListView):
    model = User


class UserDetailView(DetailView):
    model = User