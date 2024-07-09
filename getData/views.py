## importações do django
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


## importando classes da models
from CTO_manager.models import Splitter , CtoPrimaria, CtoSecundaria, Cliente

# Create your views here.

def pesquisa(request):
    template = loader.get_template('getData/pesquisa.html')
    clientes = Cliente.objects.all()
    ctops = CtoPrimaria.objects.all()
    ctos= CtoSecundaria.objects.all()
    context = {
        'titulo': 'Pesquisa form',
        'clientes': clientes,
        'ctops': ctops,
        'ctos': ctos,
    }

    for cto in ctos:
        print(f"CTO: {cto.numeracao}, S: {cto.splitter}")

        for cliente in cto.clientes.all():
            print(f"Cliente: {cliente.nome}, {cto} porta {cliente.porta}")
    


    return HttpResponse(template.render(context, request))


def exibicao(request):
    template = loader.get_template('getData/exibicao.html')
    ctos = CtoSecundaria.objects.all()
    cto =CtoSecundaria.objects.get(pk=1)

    print(cto.clientes.all())

    # for cto in ctos:
    #     print(cto.pk)
    context = {
        'cto':cto,
        'clientes':cto.clientes.all(),

    }



    return HttpResponse(template.render(context, request))


def getCTO_P(request):
  from CTO_manager.models import Cliente, CtoPrimaria, CtoSecundaria, Splitter

  ctos = CtoPrimaria.objects.all()
  cto = CtoSecundaria.objects.get(numeracao=1001)

  portas = {}
  clientes_associados = cto.clientes.all()

  print(f"Cto {cto.numeracao} tem {cto.clientes.count()} clientes")
  
  for cliente in clientes_associados:
    print(f"Porta: {cliente.porta} cliente {cliente.nome}, RG: {cliente.rg}")





  return HttpResponse(f"Pagina de teste {cto}")