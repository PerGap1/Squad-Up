from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *


class UserView:
    model = User


class UserListView(UserView, ListView): pass
    # template_name = ''


class UserDetailView(UserView, DetailView): pass


class UserCreateView(UserView, CreateView):
    fields = ['email', 'username', 'country', 'profile_picture', 'dark_mode', 'discord', 'plan', 'games', 'friends']


class UserUpdateView(UserView, UpdateView):
    fields = ['email', 'username', 'country', 'profile_picture', 'dark_mode', 'discord', 'plan', 'games', 'friends']


class UserDeleteView(UserView, DeleteView): pass