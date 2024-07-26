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

def teste_remover(request):
  def pl(qt):
    print("\n"*qt)

  def removercl(cto):
    clientes = cto.clientes.all()
    if clientes:  
      for cliente in clientes:
        cto.remover_cliente(cliente)
      print(f'TODOS CLIENTES DA CTO:{cto} FORAM REMOVIDOS')
    else:
      print(f"Sem clientes na CTO {cto}")


  from django.shortcuts import redirect
  from CTO_manager.models import Splitter , CtoPrimaria, CtoSecundaria, Cliente
  os.system('cls') # limpar tela windows
  os.system('clear') # limpar tela linux

  todasCTOS = CtoSecundaria.objects.all()
  print("#"*10)
  for cto in todasCTOS:
    print(cto)
  print("#"*20,"\n")

  ########## query ctos
  cto1001 = CtoSecundaria.objects.get(numeracao = 1001)
  cto1002 = CtoSecundaria.objects.get(numeracao = 1002)
  cto1101 = CtoSecundaria.objects.get(numeracao = 1101)
  cto1103 = CtoSecundaria.objects.get(numeracao = 1103)

  #### query clientes das ctos
  cliente_cto1001 = cto1001.clientes.all()
  cliente_cto1002 = cto1002.clientes.all()
  cliente_cto1101 = cto1101.clientes.all()
  cliente_cto1103 = cto1103.clientes.all()


  ###### print dos clientes de cada cto
  print(cto1001)
  for cliente in cliente_cto1001:
    print(cliente)
    removercl(cto1001)

  pl(2)
  print(cto1002)
  for cliente in cliente_cto1002:
    print(cliente)
    removercl(cto1002)

  pl(2)
  print(cto1101)
  for cliente in cliente_cto1101:
    print(cliente)
    removercl(cto1101)
  
  pl(2)
  print(cto1103)
  for cliente in cliente_cto1103:
    print(cliente)
    removercl(cto1103)

  

  splitter = Splitter.objects.all()
  ctoP =CtoPrimaria.objects.all()
  # clientes = cto1001.clientes.all()

  

 

  # for cliente in clientes:
  #   print(f"cliente {cliente} REMOVIDO")
  #   cto1001.remover_cliente(cliente)



  

  print("\n" * 5)
  return HttpResponse()
  