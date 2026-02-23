from django.shortcuts import render
from django.urls import reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django import forms
from django.urls import reverse

from .models import Game


# Reutilização de código
class GameView: model = Game

class GameUrl(GameView):
    success_url = reverse_lazy('games:game-list')

class GameForm(GameUrl): 
    fields = ['name', 'description', 'released', 'creator']     # 'artwork',


# Views genéricas
class GameListView(GameView, ListView): pass
    # template_name = ''


class GameDetailView(GameView, DetailView): pass


class GameCreateView(GameForm, CreateView):

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('games:game-list'))


class GameUpdateView(GameForm, UpdateView): pass


# class GameForm(forms.Form):
#     name = forms.CharField()
#     description = forms.TextInput()
# class GameFormView(FormView):
    

class GameDeleteView(GameUrl, DeleteView): pass