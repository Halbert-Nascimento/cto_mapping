from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse("Bem vindo a pagina inicial, pag app: /ctomanager")