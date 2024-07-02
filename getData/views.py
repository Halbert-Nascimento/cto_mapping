## importações do django
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


## importando classes da models
from CTO_manager.models import Splitter , CtoPrimaria, CtoSecundaria, Cliente

# Create your views here.

def pesquisa(request):
    template = loader.get_template('getData/pesquisa.html')
    context = {
        'titulo': 'Pesquisa form'
    }
    


    return HttpResponse(template.render(context, request))