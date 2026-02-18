from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

"""Squads"""
class SquadView:
    model = Squad


class SquadListView(SquadView, ListView): pass


class SquadDetailView(SquadView, DetailView): pass


class SquadCreateView(SquadView, CreateView): 
    fields = ['name', 'privacy', 'image', 'games', 'creator', 'host', 'members']


class SquadUpdateView(SquadView, UpdateView): pass


class SquadDeleteView(SquadView, DeleteView): pass

"""Events"""
class EventView:
    model = Event


class EventListView(EventView, ListView): pass


class EventDetailView(EventView, DetailView): pass


class EventCreateView(EventView, CreateView):
    fields = ['name', 'privacy', 'image', 'games', 'creator', 'host', 'members']


class EventUpdateView(EventView, UpdateView): pass


class EventDeleteView(EventView, DeleteView): pass