from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Game


class GameView:
    model = Game


class GameListView(GameView, ListView): pass


class GameDetailView(GameView, DetailView): pass


class GameCreateView(GameView, CreateView): 
    fields = ['name', 'artwork', 'description', 'released', 'creator']


class GameUpdateView(GameView, UpdateView): pass


class GameDeleteView(GameView, DeleteView): pass