from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


# Create your views here.

def index(request):
  template = loader.get_template('CTO_manager/splitter_form.html')
  context = {
    'titulo' : 'Splitter form',
    'titulo_form': 'Splitter',        
    }
  if request.method == 'POST':
    splitter = request.POST['splitter']

    print(f"Spliter selecionado: 1/{splitter}")

  return HttpResponse(template.render(context, request))
  

def pag(request):

  return HttpResponse("Segunda pagina teste!")