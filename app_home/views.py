from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import os


# Create your views here.

def home(request):
  template = loader.get_template('app_home/index.html')
  context = {
        
    }

  return HttpResponse(template.render(context, request))


def sobre(request):

  template = loader.get_template('app_home/sobre.html')
  context = {
        
    }

  return HttpResponse(template.render(context, request))

def teste(request):
  template = loader.get_template('app_home/teste.html')
  context = {
        
    }

  return HttpResponse(template.render(context, request))

  