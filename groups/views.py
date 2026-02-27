from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.http.response import HttpResponseRedirect

from .models import *

"""Squads"""
# Reutilização de código
class SquadView: model = Squad

class SquadUrl(SquadView):
    success_url = reverse_lazy('groups:squad-list')

class SquadForm(SquadUrl): 
    fields = ['name', 'privacy', 'image', 'games', 'creator', 'host', 'members']


# Views genéricas
class SquadListView(SquadView, ListView): pass

class SquadDetailView(SquadView, DetailView): pass

class SquadCreateView(SquadForm, CreateView):

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('groups:squad-list'))

class SquadUpdateView(SquadForm, UpdateView): pass

class SquadDeleteView(SquadUrl, DeleteView): pass


"""Events"""
# Reutilização de código
class EventView: model = Event

class EventUrl(EventView):
    success_url = reverse_lazy('groups:event-list')

class EventForm(EventUrl): 
    fields = ['name', 'privacy', 'image', 'games', 'creator', 'host', 'members']


# Views genéricas
class EventListView(EventView, ListView): pass

class EventDetailView(EventView, DetailView): pass

class EventCreateView(EventForm, CreateView):

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('groups:event-list'))

class EventUpdateView(EventForm, UpdateView): pass

class EventDeleteView(EventUrl, DeleteView): pass