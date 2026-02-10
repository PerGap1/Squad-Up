from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def teste(request):
    return HttpResponse('<h1>Teste</h1>')