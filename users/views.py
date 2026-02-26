from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http.request import HttpRequest
from django.contrib import messages

from .forms import UserRegistrationForm
from .models import User

# template_name = ''

# Reutilização de código
class UserView: model = User

class UserUrl(UserView):
    success_url = reverse_lazy('users:user-list')

class UserForm(UserUrl): 
    fields = ['email', 'username', 'password', 'country', 'profile_picture', 'dark_mode', 'discord', 'plan', 'games', 'friends']


# Views genéricas
class UserListView(UserView, ListView): pass

class UserDetailView(UserView, DetailView): pass

class UserCreateView(UserForm, CreateView):

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('users:user-list'))

class UserUpdateView(UserForm, UpdateView): pass

class UserDeleteView(UserUrl, DeleteView): pass


def register(request:HttpRequest):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created!")

            return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})