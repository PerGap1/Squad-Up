from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *


class UserView:
    model = User

class UserListView(UserView, ListView): pass


class UserDetailView(UserView, DetailView): pass


class UserCreateView(UserView, CreateView): pass


class UserUpdateView(UserView, UpdateView): pass


class UserDeleteView(UserView, DeleteView): pass