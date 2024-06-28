## importações do django
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

## importando classes da models
from .models import Splitter , CtoPrimaria, CtoSecundaria



def cadastro_splitter(request):
  """
    View para cadastrar um novo Splitter.

    Args:
        request (HttpRequest): A requisição HTTP recebida.

    Returns:
        HttpResponse: Uma resposta HTTP com o template renderizado e as mensagens de sucesso ou erro.
  """
  
  template = loader.get_template('CTO_manager/splitter_form.html')

  context = {
    'titulo' : 'Splitter form', # titulo da pagina
    'titulo_form': 'Splitter', # titulo para formulario
    }
  
  if request.method == 'POST': ## verifica se o requerimento e do tipo POST
    splitter_form = request.POST['splitter'] # Obtém o valor do campo 'splitter' do formulário
    print(f"Spliter selecionado: 1/{splitter_form}") # degub exibir no console

    if Splitter.objects.filter(splitter_tipo = splitter_form).exists(): # verifica se o splitter ja existe no banco de dados
      messages.error(request, f"Splitter 1/{splitter_form} ja esta cadastrado em nosso banco de dados!") # salva uma menagem d error temporaria para exibir que ja esta cadstrado o splitter 
      
    
    else:
      splitter = Splitter(splitter_tipo = splitter_form) # cria a instância do splitter com o valor recebido do formulario
      splitter.save() # salva no banco de dados
      messages.success(request, f"Splitter 1/{splitter_form} salvo") # cria uma mensagem temporaria para ser passada para a nova pagina com informação de sucesso
      return redirect(cadastro_splitter) # # Redireciona para a mesma página (ou para uma página de sucesso), fazendo com que a pagina do formulario seja limpa

  return HttpResponse(template.render(context, request)) # se não for post exiba a pagina sem alterações
  

def cadastro_ctop(request):

  template = loader.get_template('CTO_manager/ctop_form.html')
  splitters = Splitter.objects.all()

  context = {
    'titulo' : 'CTOP form', # titulo da pagina
    'titulo_form': 'CTO Primaria', # titulo para formulario
    'splitters': splitters,
    }
  
  if request.method == "POST":
    numeracao = int(request.POST['numeracao'])
    tipo_splitter = int(request.POST['splitter'])
    cor_fibra = request.POST['cor_fibra']
    sinal_entrada = float(request.POST['sinal_in'])
    descricao = request.POST['descicao']

    print(f"{'****DADOS SALVOS*****': ^50}")
    print(f"{'CTOP:':<15}{numeracao}")
    print(f"{'Cor fibra:':<15}{cor_fibra}")
    print(f"{'Splitter:':<15}1/{tipo_splitter}")
    print(f"{'Sinal input:':<15}{sinal_entrada}")
    print(f"{'Descrição:':<15}{descricao}")

    splitter = Splitter.objects.get(id=tipo_splitter)

    

    if CtoPrimaria.objects.filter(numeracao = numeracao).exists():
       return HttpResponse("Ctop ja cadastrada")
    else:
      splitter = Splitter.objects.get(id=tipo_splitter)    # pega o objeto do bando de dados Splitter e salva em splitter
      ctop = CtoPrimaria(numeracao=numeracao,descricao= descricao,cor_fibra_entrada= cor_fibra,sinal_entrada=sinal_entrada,splitter=splitter)

      ctop.save()
 
 

  return HttpResponse(template.render(context, request)) # se não for post exiba a pagina sem alterações

