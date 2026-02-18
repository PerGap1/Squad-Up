from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Schedule


class ScheduleView:
    model = Schedule


class ScheduleListView(ScheduleView, ListView): pass


class ScheduleDetailView(ScheduleView, DetailView): pass


class ScheduleCreateView(ScheduleView, CreateView):
    fields = []


class ScheduleUpdateView(ScheduleView, UpdateView): pass


class ScheduleDeleteView(ScheduleView, DeleteView): pass