from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RelationshipForm
from django.conf import settings
from .models import Relationship , Fotos , TemporaryPageData, TemporaryPageImage

# requisicao para a API de pagamento
import requests
import json
from .chaveToken import chaveAPI # importa a chave da API do mercado pago

#modulos manuais
from .api_mercadopago import gerar_link_pagamento # importa a função que gera o link de pagamento
from .attempt_id_create import attempt_id_create # importa a função que cria um id unico para a tentativa de pagamento

import uuid # para gerar um id unico para a sessão do usuario

#para manipulação dos arquivos
import os
import mimetypes
from django.core.exceptions import ValidationError
from django.http import HttpResponse


import re # para manipulação de strings usado no link da musica



def relationship_form(request): # apagar apos implementação do restante do site
    if request.method == 'POST':
        form = RelationshipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  # Após salvar, redireciona para uma página de sucesso
    else:
        form = RelationshipForm()
    return render(request, 'index.html', {'form': form})



def index(request):
  template = loader.get_template('home.html')
  context = {
      'title': 'Love Calculator',
      'content': 'Home page'
  }

  return  HttpResponse(template.render(context, request))



def url_personalizada(request, nome):
  template = loader.get_template('pag_personalizada.html')
  relacionamento_id = 14
  user = Relationship.objects.get(id=14)
  fotos = user.fotos.all()
  
  def convert_youtube_link_to_iframe(user):
    # Tenta buscar o ID do vídeo no link do YouTube
    match = re.search(r'v=([^&]+)', user)    
    if match:
        # Extrai o ID do vídeo
        newLink = match.group(1)
        # Gera o URL do iframe com autoplay, mute e loop
        iframe_url = f"https://www.youtube.com/embed/{newLink}?autoplay=1&mute=1&loop=1&start=20&rel=0&showinfo=0&enablejsapi=1"
        return iframe_url
    else:
        return None



  iframe_url = convert_youtube_link_to_iframe(user.youtube_link)
  if iframe_url:
    urlMusica = iframe_url
  else:
    urlMusica = "O link do YouTube fornecido é inválido."


  context = {
      'title': 'Love Calculator',
      'titulo': 'Y love you!',
      'nome1': user.name1,
      'nome2': "outro",
      'data': user.relationship_start_date,
      'time': user.relationship_start_time,
      'mensagem': "mensagem",
      'urlMusica': urlMusica,
      'fotos': fotos,
      'user': user          
  }     

  return  HttpResponse(template.render(context, request))



def url_personalizadaID(request, pk):
  template = loader.get_template('pag_personalizada.html')
  user = Relationship.objects.get(id=pk)
  fotos = user.fotos.all()
  

  context = {
      'title': 'Love Calculator',
      'titulo': 'Y love you!',
      'nome1': user.name1,
      'nome2': "outro",
      'data': user.relationship_start_date,
      'time': user.relationship_start_time,
      'mensagem': "mensagem",
      'urlMusica': user.youtube_link,
      'fotos': fotos,
      'user': user          
  }   

  return  HttpResponse(template.render(context, request))




def criarSite(request):
    #pegar dados do formulario
  if request.method == 'POST':
      nome1 = request.POST['nome1']
      nome2 = request.POST['nome2']
      data = request.POST['data']
      time = request.POST['time']
      mensagem = request.POST['mensagem']
      urlMusica = request.POST['urlMusica']
      
    #   print(nome1)
    #   print(nome2)
    #   print(data)
    #   print(time)
    #   print(mensagem)
    #   print(urlMusica)

      relationship = Relationship(
            name1=nome1,
            name2=nome2,
            relationship_start_date=data,
            relationship_start_time=time,
            message=mensagem,
            youtube_link=urlMusica
        )
      relationship.save()

      #trtamento especias para os arquivos
      fotos = request.FILES.getlist('fotos')
      print(f"Total de fotos recebidas: {len(fotos)}")
      MAX_FILES = 5
      if len(fotos) > MAX_FILES:
            return HttpResponse('Limite máximo de arquivos excedido.')

      for foto in fotos:
          Fotos.objects.create(relationship=relationship, imagem=foto)       
      
      
      return HttpResponse('Sucesso!')
  return render(request, 'pag_personalizada.html')

      

# dele para armazenamento temporario dos dados ate processamento do pagamento
def saveTemporaryData(request):
    #criar pu obter  o ID da sessão do usuário
    session_id = request.session.session_key
    if not session_id:
        request.session.create() # cria uma nova sessão se não existir
        session_id = request.session.session_key

    attempt_id = attempt_id_create(session_id)    

    temporary_page_data = TemporaryPageData.objects.create(
        session_id=session_id,
        attempt_id=attempt_id,
        name1=request.POST['nome1'],
        name2=request.POST['nome2'],
        relationship_start_date=request.POST['data'],
        relationship_start_time=request.POST['time'],
        message=request.POST['mensagem'],
        youtube_link=request.POST['urlMusica']
    )

    images = request.FILES.getlist('fotos')
    print(f"Total de fotos recebidas: {len(images)}")
    MAX_FILES = 5
    if len(images) > MAX_FILES:
        return HttpResponse('Limite máximo de arquivos 5 foi excedido.')
    
    for image in images:
        TemporaryPageImage.objects.create(TemporaryPageData=temporary_page_data, image=image)

    price = 20.5
    amount = 1

    link_pagamento = gerar_link_pagamento(session_id, attempt_id, 'Site Personalizado teste', price, 'Teste de pagamento', amount)

    print(link_pagamento)
            
    return redirect(link_pagamento)


#teste de geraçã de token
def testeToken(request):    
    session_id = request.session.session_key
    if not session_id:
        request.session.create() # cria uma nova sessão se não existir
        session_id = request.session.session_key

    unique_id = attempt_id_create(session_id)

    # print(f" \nSessao do usuario e: {session_id}\n")
    # print(f" \nID unico gerado: {unique_id}")

    # print(f" unique_id tamanho {len(unique_id)}\n")

    # limparDB = TemporaryPageData.objects.all()    
    # for item in limparDB:
    #     print(f"Deletando item {item}")
    #     item.delete()



    #trasnformar o token em json para passar no metadata do pagamento
    # payment:
    # {
    #     "token": "token",
    #     "description": "description",
    #     "amount": 100,
    #     "installments": 1,
    #     "payment_method_id": "visa",
    #     "payer": {

    #     }
    # }



    # link_pagamento = gerar_link_pagamento('123456', 'Site Personalizado teste', 15.0, 'Teste de pagamento', 1)

    # print(link_pagamento)
            
    return HttpResponse(f"pagina de teste de token token:")


# pagina  para redirecionamento da API de pagamento sucess, fail, pending
# pagina de sucesso
def success(request):
    # Captura parâmetros da query string
    collection_id = request.GET.get('collection_id')
    collection_status = request.GET.get('collection_status')
    external_reference = request.GET.get('external_reference')
    payment_type = request.GET.get('payment_type')
    
    # URL da API do Mercado Pago para detalhes do pagamento
    url = f"https://api.mercadopago.com/v1/payments/{collection_id}"
    headers = {
        'Authorization': f'Bearer {chaveAPI()}'
    }

    # Requisição para obter detalhes do pagamento
    response = requests.get(url, headers=headers)
    
    # Verifica se a resposta foi bem-sucedida
    if response.status_code == 200:
        payment_data = response.json()
        # Debugging no console
        formatted_data = json.dumps(payment_data, indent=4, ensure_ascii=False)

        #pegando attempt_id do metadata
        attempt_id = payment_data['metadata']['attempt_id']
        # print(f" \nID da tentativa de pagamento: {attempt_id}\n")

        #busca no banco de dados o registro da tentativa de pagamento
        temporary_page_data = TemporaryPageData.objects.get(attempt_id=attempt_id)


        
        # Retorna os dados formatados na página
        return HttpResponse(f"<h1>{attempt_id}</h1><pre>{formatted_data}</pre>", content_type="text/html")
    else:
        return HttpResponse(f"Erro ao buscar detalhes do pagamento. Status: {response.status_code}")