from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse

from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Game

# template_name = ''

# Reutilização de código
class GameView: model = Game

class GameUrl(GameView):
    success_url = reverse_lazy('games:game-list')

class GameForm(GameUrl): 
    fields = ['name', 'description', 'released', 'creator']     # 'artwork',

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return HttpResponseRedirect(reverse('games:game-list'))


# Views genéricas
class GameListView(GameView, ListView): pass
class GameDetailView(GameView, DetailView): pass
class GameCreateView(GameForm, CreateView): pass
class GameUpdateView(GameForm, UpdateView): pass
class GameDeleteView(GameUrl, DeleteView): pass

'''
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm


class MyFormView(View):
    form_class = MyForm
    initial = {"key": "value"}
    template_name = "form_template.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect("/success/")

        return render(request, self.template_name, {"form": form})'''