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
    fields = ['name', 'privacy', 'image', 'games', 'host', 'members']

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('groups:squad-list'))


# Views genéricas
class SquadListView(SquadView, ListView): pass
class SquadDetailView(SquadView, DetailView): pass
class SquadCreateView(SquadForm, CreateView): pass
class SquadUpdateView(SquadForm, UpdateView): pass
class SquadDeleteView(SquadUrl, DeleteView): pass


"""Events"""
# Reutilização de código
class EventView: model = Event

class EventUrl(EventView):
    success_url = reverse_lazy('groups:event-list')

class EventForm(EventUrl): 
    fields = ['name', 'privacy', 'image', 'games', 'host', 'members', 'squad']

    def form_valid(self, form:EventForm):
        # Todos os jogadores do squad serem adicionados no evento...?
        # form.fields['creator'] = form.fields['host']
        # Ajustar os forms, para que alguns campos não sejam obrigatórios
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('groups:event-list'))


# Views genéricas
class EventListView(EventView, ListView): pass
class EventDetailView(EventView, DetailView): pass
class EventCreateView(EventForm, CreateView): pass
class EventUpdateView(EventForm, UpdateView): pass
class EventDeleteView(EventUrl, DeleteView): pass