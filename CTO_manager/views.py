from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):

  return HttpResponse("Home page, seja vem vindo, teste django, foi um sucesso!")

def pag(request):

  return HttpResponse("Segunda pagina teste!")