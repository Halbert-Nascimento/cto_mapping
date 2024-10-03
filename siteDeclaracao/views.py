from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RelationshipForm
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse


import shutil

from .models import Relationship , Fotos , TemporaryPageData, TemporaryPageImage, DataUserPayment, PageRelationship, PageRelationshipImage

# requisicao para a API de pagamento
import requests
from django.db import transaction
import json
from .chaveToken import chaveAPI # importa a chave da API do mercado pago

#modulos manuais
from .api_mercadopago import gerar_link_pagamento # importa a função que gera o link de pagamento
from .attempt_id_create import attempt_id_create # importa a função que cria um id unico para a tentativa de pagamento
from .create_custom_url import create_custom_url # importa a função que cria uma url personalizada para o usuario
from .convert_link_to_iframe_youtube import convert_link_to_iframe_youtube # importa a função que converte o link do youtube para o iframe
from .is_plan_expired import is_plan_expired # importa a função que verifica se o plano do usuario expirou 

import uuid # para gerar um id unico para a sessão do usuario

#para manipulação dos arquivos
import os
import mimetypes
from django.core.exceptions import ValidationError
from django.http import HttpResponse




# start log
import logging

# Obtém o caminho absoluto para o diretório "logs"
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")

logging.basicConfig(
    level=logging.DEBUG,  # Define o nível de log para DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato personalizado
    filename=os.path.join(LOGS_DIR, "log_file.log"),  # Redireciona para um arquivo 
)
# Adiciona um handler para exibir no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)

# Exemplo de uso
# logging.debug("Isso é uma mensagem de debug")
# logging.info("Isso é uma mensagem informativa")
# logging.warning("Isso é um aviso")
# logging.error("Isso é um erro")
# logging.critical("Isso é um erro crítico")

# end log



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
  termos = {
      'uso': 'http://'+request.get_host()+'/love/termosdeuso/',
      'privacidade': 'http://'+request.get_host()+'/love/termosdeuso/',
  }
  context = {
      'title': 'Love Calculator',
      'content': 'Home page',
      'termos': termos,
  }

  return  HttpResponse(template.render(context, request))



def url_personalizada(request, url):  
    template = loader.get_template('pag_personalizada.html')
    url_completa = request.build_absolute_uri()
    logging.info(f"URL completa recebida: {url_completa}")

    # Extrai o último fragmento da URL para usar como parâmetro de busca
    url_access_split = url_completa.split('/')[-1]

    # Obtém o tempo atual
    time_now = timezone.now()

    # Busca o usuário e seus relacionamentos, otimizando consultas
    user = get_object_or_404(
        PageRelationship.objects.select_related('DataUserPayment').prefetch_related('page_images'), 
        url_access_split=url_access_split
    )

    is_expired, message = is_plan_expired(user ,time_now)
    if is_expired:
        logging.warning(f"Plano expirado para o usuário {user.DataUserPayment.name}: {message}")
        return HttpResponse(f"Plano expirado: {message}")  
    
    
    
    # Coleta as fotos relacionadas (já otimizadas com prefetch_related)
    fotos = user.page_images.all()  
    



    # Conversão do link do YouTube para o formato de iframe
    iframe_url = convert_link_to_iframe_youtube(user.youtube_link)
    if not iframe_url:
        logging.error("Link do YouTube inválido.")
        iframe_url = "O link do YouTube fornecido é inválido."


    # Preparando o contexto
    context = {
        'title': 'Love Calculator',
        'titulo': 'Y love you!',
        'name1': user.name1,
        'name2': "outro",  # Você pode ajustar dinamicamente
        'data': user.relationship_start_date,
        'time': user.relationship_start_time,
        'mensagem': user.message,  # Inclui mensagem personalizada
        'urlMusica': iframe_url,
        'fotos': fotos,
        'user': user          
    }     

    logging.info(f"Página personalizada renderizada para {user.name1} e {user.name2}")
    return HttpResponse(template.render(context, request))



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
      planoInput = request.POST['planoInput']

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
    planoInput = request.POST['planoInput']

    images = request.FILES.getlist('fotos')
    print(f"Total de fotos recebidas: {len(images)}")
    MAX_FILES = 5
    if len(images) > MAX_FILES:
        return HttpResponse('Limite máximo de arquivos 5 foi excedido.')
    
    for image in images:
        TemporaryPageImage.objects.create(TemporaryPageData=temporary_page_data, image=image)

    plano = int(planoInput)
    pricePlan = {
        1: 5.0,
        6: 10.0,
        12: 20.0,
    }
    price = 20.5
    amount = 1

    link_pagamento = gerar_link_pagamento(session_id, attempt_id, "Testes pagamento "+planoInput, pricePlan[plano], 'Teste de pagamento', amount, plano)

    print(link_pagamento)
            
    return redirect(link_pagamento)
    # return HttpResponse(f"pagina de teste de token token: {link_pagamento}")



# Página de redirecionamento da API de pagamento: sucesso, falha, pendente
# pagina de sucesso
@transaction.atomic
def success(request):
    """
    Processa a resposta de sucesso da API de pagamento do Mercado Pago.
    Captura parâmetros da query string, busca detalhes do pagamento,
    cria registros no banco de dados e move imagens temporárias para o diretório definitivo.
    """

    # Captura parâmetros da query string
    collection_id = request.GET.get('collection_id')
    collection_status = request.GET.get('collection_status')
    external_reference = request.GET.get('external_reference')
    payment_type = request.GET.get('payment_type')
    
    # URL da API do Mercado Pago para detalhes do pagamento
    url = f"https://api.mercadopago.com/v1/payments/{collection_id}"
    headers = {'Authorization': f'Bearer {chaveAPI()}'}

    try:
        # Requisição para obter detalhes do pagamento
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança uma exceção para códigos de erro HTTP

        # Converte a resposta JSON para um objeto Python
        payment_data = response.json()
        
        # Formata os dados do pagamento para visualização
        formatted_data = json.dumps(payment_data, indent=4, ensure_ascii=False)
        # json.dumps: Essa função converte um objeto Python em uma string JSON.
        # payment_data: É o objeto Python que contém os dados da resposta.
        # indent=4: Especifica que queremos uma formatação com recuo (indentação) de 4 espaços. Isso torna a saída mais organizada e fácil de ler.
        # ensure_ascii=False: Isso permite que caracteres não-ASCII (como caracteres acentuados) sejam representados diretamente na saída, em vez de serem escapados como sequências de escape ASCII (\uXXXX).

        # Obtém dados do metadat
        metadata = payment_data.get('metadata', {})
        session_id = metadata.get('session_id', None)
        attempt_id = metadata.get('attempt_id', None)
        planoInput = metadata.get('plano_input', 0)

        logging.warning(f"Detalhes do pagamento metadata: {metadata}") #debug
        logging.warning(f"Detalhes do pagamento meses plano e: {planoInput}") #debug
        logging.warning(f"Detalhes do pagamento session_id: {session_id}") #debug
        logging.warning(f"Detalhes do pagamento attempt_id: {attempt_id}") #debug
        
        # Obtém dados do pagador
        payer = payment_data.get('payer', {})
        email = payer.get('email', None)
        cpf = payer.get('identification', {}).get('number', None)

         # Obtém status e valor do pagamento
        status = payment_data.get('status', None)
        status_detail = payment_data.get('status_detail', None)
        items = payment_data.get('items', [])
        # payment_value = items[0].get('unit_price', 0) if items else 0
        payment_value = payment_data.get('transaction_amount', 0)
        active_time_month = int(planoInput)
        logging.warning(f"Detalhes do plano active_time_month: {active_time_month}") #debug
        
        # Verifica se attempt_id foi encontrado
        if attempt_id is None:
            logging.error("attempt_id da tentativa de pagamento não encontrado")
            return HttpResponse("ID da tentativa de pagamento não encontrado")
        
        # Verifica se o pagamento já foi registrado ou se ja existe esse cadastro
        if DataUserPayment.objects.filter(attempt_id=attempt_id).exists():
            logging.error(f"Pagamento já registrado para attempt_id {attempt_id}.")
            return HttpResponse("Erro: duplicata. pagamento ja realizado")


        #busca no banco de dados temporaio o registro da tentativa de pagamento
        user = get_object_or_404(TemporaryPageData, attempt_id=attempt_id)

        # Cria um novo registro de pagamento no banco de dados
        new_user = DataUserPayment.objects.create(
            session_id = session_id,
            attempt_id = attempt_id,
            name=user.name1,
            email= email,
            cpf = cpf,
            payment_status = status,
            payment_status_detail = status_detail,
            payment_value = payment_value,
            active_time_month = active_time_month,            
        )        

        # Cria um novo registro de relacionamento no banco de dados
        page_new_user = PageRelationship.objects.create(
            DataUserPayment = new_user,
            name1 = user.name1,
            name2 = user.name2,
            status = status,
            relationship_start_date = user.relationship_start_date,
            relationship_start_time = user.relationship_start_time,
            message = user.message,
            youtube_link = user.youtube_link,
        )
        # Cria a url personalizada para o usuario
        url_access = create_custom_url(page_new_user.name1, page_new_user.name2 ,page_new_user.id)

        # Salva a url personalizada no registro do relacionamento
        page_new_user.url_access = url_access
        page_new_user.url_access_split = url_access.split('/')[-1]
        page_new_user.save()

        
        # Busca as imagens temporárias relacionadas ao usuário
        images = TemporaryPageImage.objects.filter(TemporaryPageData=user)
        if not images.exists():
            logging.warning(f"Nenhuma imagem encontrada para o usuário com attempt_id {attempt_id}.")
        
        # Cria o diretório de imagens definitivo, se não existir
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'relationship_files')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'relationship_files'))

        # Move as imagens temporárias para o diretório definitivo
        for image in images:
            # Define o caminho do arquivo de imagem temporário
            temp_image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
            # Define o novo caminho no diretório definitivo
            new_image_path = os.path.join(settings.MEDIA_ROOT, 'relationship_files', os.path.basename(image.image.name))

            try:
                # Move o arquivo de imagem do diretório temporário para o definitivo
                shutil.move(temp_image_path, new_image_path)

                # Cria a nova entrada no modelo PageRelationshipImage com o caminho atualizado
                PageRelationshipImage.objects.create(
                    PageRelationship=page_new_user,
                    image=f'relationship_files/{os.path.basename(image.image.name)}'  # Define o novo caminho no campo de imagem
                )
            except FileNotFoundError as e:
                logging.error(f"Erro ao mover o arquivo de imagem: {e}")
                return HttpResponse("Erro ao processar as imagens")

        # Deleta o registro temporário de dados do usuário
        user.delete()

        # log de sucesso 
        logging.info(f"Pagamento com attempt_id {attempt_id} salvo com sucesso. Dados: {formatted_data}")

        periodo = '1 mes' if active_time_month == 1 else f"{active_time_month} meses"        

        data = {
            'periodo': periodo,
            'url_access' : url_access.split('/')[-1],
            'payment_value': payment_value,
        }
        #salva os dados na sessão do usuario em formato json
        request.session['data'] = json.dumps(data)

        
        #teste retonar a pagina de sucesso
        return redirect(confirmacao)

        # Retorna os dados formatados na página
        return redirect(url_access)
        # return HttpResponse(f"<h1>{attempt_id}</h1><pre>{formatted_data}</pre>", content_type="text/html")
    
    # Trata exceções de requisição
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de requisição ao Mercado Pago: {e}")
        return HttpResponse(f"Erro ao buscar detalhes do pagamento: {e}")
    

def fail(request):
    """
    Página de falha de pagamento.
    """
    return HttpResponse("Falha no pagamento.")

def pending(request):
    data_json = request.session.get('data')

    url_access = ''
    periodo = 'N/D'
    payment_value = "N/D"
    new_link_pagamento = ''
    collection_id = request.GET.get('collection_id', None)
    pending = 'pending - ' #debug de pagina pendente
    if collection_id:
        url = f"https://api.mercadopago.com/v1/payments/{collection_id}"
        headers = {'Authorization': f'Bearer {chaveAPI()}'}

        try:
            # Requisição para obter detalhes do pagamento
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Lança uma exceção para códigos de erro HTTP

            # Converte a resposta JSON para um objeto Python
            payment_data = response.json()
        
            # Formata os dados do pagamento para visualização
            formatted_data = json.dumps(payment_data, indent=4, ensure_ascii=False)
            # json.dumps: Essa função converte um objeto Python em uma string JSON.
            # payment_data: É o objeto Python que contém os dados da resposta.
            # indent=4: Especifica que queremos uma formatação com recuo (indentação) de 4 espaços. Isso torna a saída mais organizada e fácil de ler.
            # ensure_ascii=False: Isso permite que caracteres não-ASCII (como caracteres acentuados) sejam representados diretamente na saída, em vez de serem escapados como sequências de escape ASCII (\uXXXX).

            # Obtém dados do metadat
            metadata = payment_data.get('metadata', {})
            session_id = metadata.get('session_id', None)
            attempt_id = metadata.get('attempt_id', None)
            planoInput = metadata.get('plano_input', 0)
        
            # items = payment_data.get('items', [])
            description  = 'siteDeclaracao'
            payment_value = payment_data.get('transaction_amount', 0)
            active_time_month = int(planoInput)

            
            logging.warning(f"{pending}Detalhes do pagamento metadata: {metadata}") #debug
            logging.warning(f"{pending}Detalhes do pagamento meses plano e: {planoInput}") #debug
            logging.warning(f"{pending}Detalhes do pagamento session_id: {session_id}") #debug
            logging.warning(f"{pending}Detalhes do pagamento attempt_id: {attempt_id}") #debug

            # caso acesso a pagina de pagamento pendente depois de pagado redireciona para outra pag em desenvolvimento
            if DataUserPayment.objects.filter(attempt_id=attempt_id).exists():
                logging.error(f"{pending}Pagamento já registrado para attempt_id {attempt_id}.")
                return HttpResponse("Erro: duplicata. pagamento ja realizado")

            if TemporaryPageData.objects.filter(attempt_id=attempt_id).exists():
                pagar_nova = TemporaryPageData.objects.get(attempt_id=attempt_id)
                new_link_pagamento = gerar_link_pagamento(pagar_nova.session_id, pagar_nova.attempt_id, description, payment_value, 'Teste de pagamento', 1, active_time_month)

        except requests.exceptions.RequestException as e:
            logging.error(f"{pending}Erro de requisição ao Mercado Pago: {e}")
            return HttpResponse(f"Erro ao buscar detalhes do pagamento: {e}")


    #obtem host da requisição
    host = request.get_host()
    if not host:
        logging.error("Host não encontrado na requisição.")
        return HttpResponse("Erro ao obter informações do host", status=500)

            
    #cria as urls com as verificacoes apropiadas
    url = {
        'cadastro': 'http://' + host + '/love/home/',
        'url_access': 'http://' + host +'/love/post/' +url_access if url_access else '',
        'new_link_pagamento': new_link_pagamento,
    }

    #carrega o template e o contexto
    template = loader.get_template('pending_pagamento.html')
    context = {
        'title': 'confimacao_pagamento',
        'content': 'Página de confirmação',
        'url': url,
        'periodo': periodo,
        'payment_value': payment_value,
    }

    
    #renderiza a pagina
    return HttpResponse(template.render(context, request))

def confirmacao(request):
    #obtem os dados json da sessão do usuario
    data_json = request.session.get('data')
    
    #inicializa as variaveis com valores padrão para evitar erros
    url_access = ''
    periodo = 'Error ao obter periodo'
    payment_value = 'Err'


    #verifica se os dados foram obtidos
    if data_json:
        try:
            data = json.loads(data_json)
            #verifica se as chave existem
            url_access = data.get('url_access', '') # se não existir retorna ''
            periodo = data.get('periodo', 'Error ao obter periodo') # se não existir erro
            payment_value = data.get('payment_value', 'Error') # se não existir erro
            
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON: {e}")
            return HttpResponse("Erro ao decodificar JSON.")

    #obtem host da requisição
    host = request.get_host()
    if not host:
        logging.error("Host não encontrado na requisição.")
        return HttpResponse("Erro ao obter informações do host", status=500)

            
    #cria as urls com as verificacoes apropiadas
    url = {
        'cadastro': 'http://' + host + '/love/home/',
        'url_access': 'http://' + host +'/love/post/' +url_access if url_access else '',
    }

    #carrega o template e o contexto
    template = loader.get_template('confimacao_pagamento.html')
    context = {
        'title': 'confimacao_pagamento',
        'content': 'Página de confirmação',
        'url': url,
        'periodo': periodo,
        'payment_value': payment_value,
    }
    #renderiza a pagina
    return HttpResponse(template.render(context, request))



def termosDeUso(request):
    template = loader.get_template('termos_de_uso.html')
    context = {
        'title': 'Termos de Uso',
        'content': 'Termos de Uso',
        'home': 'http://'+request.get_host()+'/love/home/',
        
    }
    return HttpResponse(template.render(context, request))