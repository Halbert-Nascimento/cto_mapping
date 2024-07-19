## importações do django
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

## importando classes da models
from .models import Splitter , CtoPrimaria, CtoSecundaria, Cliente



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
  

def cadastro_ctoP(request):
  """
    View para cadastrar uma CTO Primária (CTOP).

    Quando o usuário acessa a página de cadastro, essa função carrega o template
    'CTO_manager/ctop_form.html' e exibe o formulário. Ela também recupera todos
    os objetos do modelo 'Splitter' do banco de dados para exibi-los no formulário.

    Se o método da requisição for POST (ou seja, o formulário foi enviado), a função
    extrai os dados do formulário (número de CTO, tipo de splitter, cor da fibra,
    sinal de entrada e descrição). Em seguida, verifica se um objeto 'CtoPrimaria'
    com o mesmo número de CTO já existe no banco de dados. Se existir, retorna uma
    mensagem informando que a CTOP já está cadastrada. Caso contrário, cria uma nova
    instância de 'CtoPrimaria' com os dados fornecidos e salva no banco de dados.

    Args:
        request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
        HttpResponse: Renderiza o template com o contexto atualizado ou exibe uma
        mensagem de erro se a CTOP já estiver cadastrada.

  """

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
    descricao = request.POST['descricao']

    print(f"{'****DADOS SALVOS*****': ^50}")
    print(f"{'CTOP:':<15}{numeracao}")
    print(f"{'Cor fibra:':<15}{cor_fibra}")
    print(f"{'Splitter id:':<15}{tipo_splitter}")
    print(f"{'Sinal input:':<15}{sinal_entrada}")
    print(f"{'Descrição:':<15}{descricao}")

       

    if CtoPrimaria.objects.filter(numeracao = numeracao).exists(): # verifica se a numeração da cto ja existe
       messages.error(request,f"Cto Primaria {numeracao}' ja cadastrada no sistema!")

      
       return redirect(cadastro_ctoP)
    else:
      splitter = Splitter.objects.get(id=tipo_splitter)    # pega o objeto do bando de dados Splitter e salva em splitter
      ctop = CtoPrimaria(numeracao=numeracao,descricao= descricao,cor_fibra_entrada= cor_fibra,sinal_entrada=sinal_entrada,splitter=splitter) # cria o objeto cto com seus parametros

      ctop.save() #salva no banco de dados
      messages.success(request, f"Cto Primaria '{numeracao}' cadastrada com sucesso!")
 
 

  return HttpResponse(template.render(context, request)) # se não for post exiba a pagina sem alterações


def cadastro_ctoS(request):
  """
  Função de visualização para lidar com o formulário de cadastro de CTO (Central Telefônica de Operação).

    Args:
        request (HttpRequest): O objeto de requisição HTTP contendo os dados do formulário.

    Returns:
        HttpResponse: Uma resposta contendo o template renderizado ou uma resposta de redirecionamento.

    Notas:
        - Esta função lida com requisições GET e POST.
        - Se o método da requisição for POST, ela processa os dados do formulário e salva uma nova instância de CTO Secundaria.
        - Se o CTO com a numeracao fornecida já existir, exibe uma mensagem de erro.
        - Caso contrário, cria e salva um novo CTO Secundaria.
        - A função também fornece dados de contexto para renderizar o template.

    Campos do Formulário (esperados na requisição POST):
        - 'num_ctop': ID da Derivação CTOP (CTO Primaria) (inteiro)
        - 'numeracao': Numeracao do CTO (CTO Secundaria) (inteiro)
        - 'metragem': Metragem (inteiro)
        - 'sinal_in': Sinal de entrada (float)
        - 'splitter': ID do Splitter (inteiro)
        - 'descricao': Descrição (string)

    Contexto do Template:
        - 'titulo': Título da página
        - 'titulo_form': Título para o formulário
        - 'splitters': QuerySet de todos os objetos Splitter
        - 'ctops': QuerySet de todos os objetos CtoPrimaria

    Exemplo de Uso (no template):
        {% for splitter in splitters %}
            {{ splitter.id }}: {{ splitter.name }}
        {% endfor %}  
  """


  template = loader.get_template('CTO_manager/ctos_form.html')
  splitters = Splitter.objects.all()
  ctops = CtoPrimaria.objects.all()

  context = {
    'titulo' : 'CTOP form', # titulo da pagina
    'titulo_form': 'CTO Primaria', # titulo para formulario
    'splitters': splitters, # QuerySet de todos os objetos Splitter
    'ctops': ctops, # QuerySet de todos os objetos CtoPrimaria
    }
  
  if request.method == 'POST': # verifica se a requisição e posta para pegar os dados do formulario
    # Processa os dados do formulário
    numeracao_ctop = int(request.POST['num_ctop']) # pegando dados da numeração da cto do formulario
    numeracao = int(request.POST['numeracao'])
    metragem = int(request.POST['metragem'])
    sinal_entrada = float(request.POST['sinal_in'])
    splitter_form = int(request.POST['splitter'])
    descricao = request.POST['descricao']


    print(f"{'****DADOS SALVOS*****': ^50}")
    print(f"{'Derivação CTOP:':<15}{numeracao_ctop}")
    print(f"{'CTO:':<15}{numeracao}")
    print(f"{'Metragem:':<15}{metragem}")
    print(f"{'Splitter id:':<15}{splitter_form}")
    print(f"{'Sinal input:':<15}{sinal_entrada}")
    print(f"{'Descrição:':<15}{descricao}")

    # Verifica se o CTO com a numeracao fornecida já existe
    if CtoSecundaria.objects.filter(numeracao=numeracao).exists():
      messages.error(request, f"CTO {numeracao} ja existe!")

      return redirect(cadastro_ctoS)

    else:
      # Obtém as instâncias de CtoPrimaria e Splitter
      ctop = CtoPrimaria.objects.get(id=numeracao_ctop)
      splitter = Splitter.objects.get(id=splitter_form)

      # upgrade implementar função no models e aqui para verificar a capacidade da ctop, se a
      # capacidade d P pelo splitter tiver atingido não e possivel realizar a instalação da secundaria

      #objects.create() é um atalho conveniente fornecido pelo Django para criar e salvar uma instância de modelo em uma única etapa.
      cto = CtoSecundaria.objects.create(numeracao=numeracao, metragem=metragem, sinal_entrada=sinal_entrada, splitter=splitter, derivacao_ctoPrimaria=ctop, descricao=descricao) 

      messages.success(request, f"CTO {numeracao} cadastrada com sucesso!")    
    

  
  return HttpResponse(template.render(context, request))


def instalacao(request):
  template = loader.get_template('CTO_manager/instalacao.html')
  ctos = CtoSecundaria.objects.all()

  context = {
    'titulo' : 'Instalação', # titulo da pagina
    'ctos':ctos,
    'range': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
  }

  if request.method == 'POST':
    # pegando as informações do formulario
    nome = request.POST['nome']
    rg = int(request.POST['rg'])
    status = request.POST['status']
    porta_cto = int(request.POST['porta'])
    numeracao_cto = int(request.POST['numeracao_cto'])
    metragem = float(request.POST['metragem'])

    # realizando o tratamento das informações
    # verificar se o cliente ja existe no DB, verificando o nome e rg
    if Cliente.objects.filter(rg = rg).exists(): # verifica se o splitter ja existe no banco de dados
      messages.error(request, f"{nome} ja esta cadastrado em nosso banco de dados!") # salva uma menagem d error temporaria para exibir que ja esta cadstrado o splitter 
      
      cliente = Cliente.objects.get(rg=rg)

      return redirect(f'/ctomanager/atualizar_cliente/{cliente.pk}')
      
    else:
      cto_secundaria = CtoSecundaria.objects.get(pk=numeracao_cto)

      if cto_secundaria.clientes.filter(porta = porta_cto).exists():
        
        context['nome'] = nome
        context['rg'] = rg
        context['status'] = status
        context['numeracao_cto'] = numeracao_cto
        context['metragem'] = metragem
        
        messages.warning(request, f"Porta {porta_cto} da CTO ocupada! Conferir porta!")

      else:
        print(f"porta {porta_cto} livre, salvando cliente")


        cliente = Cliente.objects.create(nome=nome, rg=rg, status=status, porta=porta_cto, numeracao_cto= cto_secundaria.numeracao, metragem=metragem)

        #Nome da class. função adc_cliente(cto_secundaria que vai receber as informações, o cliente e a porta)
        CtoSecundaria.adicionar_cliente(cto_secundaria, cliente=cliente, porta=porta_cto)

        messages.success(request, f"Cliente {nome} cadastrado na CTO {cto_secundaria.numeracao} porta {porta_cto}")

    # esta salvando mais que a capacidade da cto, verificar erro e arrumar


  return HttpResponse(template.render(context, request))

def atualizar_cliente(request, pk):
  template = loader.get_template('CTO_manager/atualizar_cliente.html') ## carregando locla do arquivo html

  cliente = Cliente.objects.get(pk=pk)
  ctos = CtoSecundaria.objects.all()

  context = {
    'titulo' : 'Atualiza dados', # titulo da pagina
    'ctos':ctos,
    'range': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'nome': cliente.nome,
    'rg': cliente.rg,
    'cto': cliente.numeracao_cto,
    'porta': cliente.porta,
    'status': cliente.status,
    'metragem': cliente.metragem,
    'pk': cliente.pk,    
  }



  if request.method == 'POST':
    rg = int(request.POST['rg'])    
    nome = request.POST['nome']
    status = request.POST['status']
    porta_cto = int(request.POST['porta'])
    numeracao_cto = int(request.POST['numeracao_cto'])
    metragem = float(request.POST['metragem'])


    cto_secundaria = CtoSecundaria.objects.get(numeracao = numeracao_cto)

    

    if cliente.porta != porta_cto and  cto_secundaria.clientes.filter(porta = porta_cto).exists():
        
      messages.warning(request, f"Porta {porta_cto} da CTO ocupada! Conferir porta!")

    else:
      if cliente.numeracao_cto != numeracao_cto:
        cto_cliente = CtoSecundaria.objects.get(numeracao = cliente.numeracao_cto)
        CtoSecundaria.remover_cliente(cto_cliente, cliente=cliente)
        
      CtoSecundaria.adicionar_cliente(cto_secundaria, cliente=cliente, porta=porta_cto)

      cliente.nome = nome
      cliente.status = status 
      cliente.numeracao_cto = numeracao_cto
      cliente. porta = porta_cto
      cliente.metragem = metragem

      cliente.save()
      messages.success(request, 'Dados atualizados!')

      return redirect(f'/ctomanager/atualizar_cliente/{cliente.pk}')

  
  return HttpResponse(template.render(context, request))


def mudanca_endereco(request):
  template = loader.get_template('CTO_manager/mudanca_endereco.html')
  ctos = CtoSecundaria.objects.all()

  context = {
    'titulo' : 'Mudança endereço', # titulo da pagina
    'ctos':ctos,
    'range': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
  }
  pk = request.GET.get('pk')
  if pk:   # verifica se pk não e none
    cliente = Cliente.objects.get(pk=pk)
    context['nome'] = cliente.nome
    context['rg'] = cliente.rg
    context['status'] = cliente.status
    context['porta'] = cliente.porta
    context['numeracao_cto'] = cliente.numeracao_cto
    print(cliente.numeracao_cto)
    context['metragem'] = cliente.metragem

  if request.method =="POST":
    nome = request.POST['nome']
    rg = int(request.POST['rg'])
    status = request.POST['status']
    porta_cto = int(request.POST['porta'])
    numeracao_cto = int(request.POST['numeracao_cto'])
    metragem = float(request.POST['metragem'])

    cliente = Cliente.objects.get(rg=rg)
    cliente.nome = nome
    cliente.rg = rg
    cliente.status = status
    cliente.porta = porta_cto
    cliente.numeracao_cto = numeracao_cto
    cliente.metragem = metragem

    cliente.save()

      


  return HttpResponse(template.render(context, request))


