from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *


class UserView:
    model = User


class UserListView(UserView, ListView): pass
    # template_name = ''


class UserDetailView(UserView, DetailView): pass


class UserCreateView(UserView, CreateView):
    # User registration form
    fields = ['email', 'username', 'password', 'country', 'profile_picture', 'dark_mode', 'discord', 'plan', 'games', 'friends']

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('users:user-list'))


class UserUpdateView(UserView, UpdateView):
    fields = ['email', 'username', 'password', 'country', 'profile_picture', 'dark_mode', 'discord', 'plan', 'games', 'friends']


class UserDeleteView(UserView, DeleteView): pass