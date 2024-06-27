from django.db import models


# class para definir tipo do splinter 1/8 ou 1/16 etc.., nessa classe sera assumido que a entrada sempre se 1 o que muda sao 
# as saida, 8, 16 pernas
class Splitter(models.Model):
  splitter_tipo = models.IntegerField()

# Saida padrao da classer sera txto formatado 'splitter: 1/8 etc...
  def __str__(self):
    return f"Splitter: 1/{self.splitter_tipo}"




  
# Classe para CTO primaria, onde o pre-requisito e o cadastro do splitter para definir a quantidade de saidas (CTOs secundarias) que ela pode ter.
class CtoPrimaria(models.Model):
  numercao = models.IntegerField() # Numero de identificacao da CTO primaria
  descricao = models.TextField(blank=True, null=True, verbose_name='Descricao detalhada') # Informacoes detalhadas e observacoes sobre a CTO
  cor_fibra_entrada = models.CharField(max_length=20) # Cor da fibra de entrada para futuras manutencoes na caixa p
  sinal_entrada = models.FloatField() # Referencia para o sinal que esta chegando na caixa (futura implementacao para verificar atenuacoes na rota)
  Splitter = models.ForeignKey(Splitter, on_delete=models.CASCADE) # Pre-requisito: cadastro do splitter; o tamanho do splitter define quantas CTOs secundarias a CTO primaria pode ter

  def __str__(self):
    return f"CTO_P: {self.numercao}" # Retorna uma representacao em texto formatado com a numeracao da CTO primaria




class Cliente(models.Model):
  nome = models.CharField(max_length=100) # identificação do cliente pelo nome
  rg = models.IntegerField(blank=True) # identificao do cliente RG
  status = models.CharField(max_length=15, default='ATIVO') # identificação do status do cliente  ativo, cancelado, bloqueado, se nada for atribuido inicialmente começa como 'ativo'
  porta = models.PositiveIntegerField(blank=True) # salvar a numeracao da porta que o cliente esta associado a cto, somente numeros positivos
  numeracao_cto = models.IntegerField(blank=True, null=True) # deixar salva a numeracao da cto
  metragem = models.IntegerField(default=0) # tamanho do cabo que foi utilizado para instalacao









# Classe para CTO primaria, onde o pre-requisito e o cadastro da CTO primaria e splitter para definir a quantidade de saídas 'clientes' que ela pode ter.
class CtoSecundaria(models.Model):
  numeracao = models.IntegerField() # Numero de identificacao da CTO secundaria
  descricao = models.TextField(blank=True, null=True, verbose_name='Descricao detalhada') # Informacoes detalhadas e observacoes sobre a CTO
  sinal_entrada = models.FloatField() # Referencia para o sinal que esta chegando na caixa (futura implementacao para verificar atenuacoes na rota)
  splitter = models.ForeignKey(Splitter, on_delete=models.CASCADE) # Pre-requisito: cadastro do splitter; o tamanho do splitter define quantos cliente a caixa pode ter 
  derivacao_ctoPrimaria = models.ForeignKey(CtoPrimaria, on_delete=models.CASCADE) # Pre-requisito: cadastro da cto primaria. buscar caixar com identificador da ctop
  metragem = models.IntegerField(default=0) # tamanho do cabo que foi utilizado para instalacao

  clientes = models.ManyToManyField(Cliente, blank=True) # Este e o tipo de campo que define uma relacao de muitos-para-muitos com o modelo Cliente.

  # funcao para salvar o cliente e porta da cto, e definir o max de cliente que a cto aceita
  # recebe como parametro a instacia do cliente e a numeracao da porta 
  def adicionar_cliente(self, cliente, porta): # recebe instancia cliente , e numeracao da porta
        if self.clientes.count() < self.splitter.tamanho: # verifica se a quantidade de cliente e menor que o tamanho do splitter, que e oque define a quantidade
            cliente.porta = porta # salva a numeracao da porta na instancia do cliente.porta
            cliente.numeracao_cto = self.numeracao # salva a numeracao da cto na instancia do cliente.numeracao_cto
            cliente.save() # salva no banco de dados
            self.clientes.add(cliente) # adiciona a instancia do cliente a os clientes da cto
        else:
            raise ValueError(f"Limite de clientes atingido para esta CTO secundaria. max: {self.splitter}") # retonar um erro se tentar cadastrar mais cliente que a cto comporta
        

  # portas = models.ManyToManyField(Cliente, blank=True) # Este e o tipo de campo que define uma relacao de muitos-para-muitos com o modelo Cliente.
  # funcao para salvar o cliente na porta expecifica da cto texte
  # def adicionar_cliente_a_porta(self, cliente, porta): # recebe instancia cliente , e numeracao da porta
  #       if self.portas.count() < self.splitter.tamanho: # verifica se as portas ocupadas e menor que o tamanho do splitter, que e oque define a quantidade de cliente na caixa
  #           cliente.porta = porta # salva a numeracao da porta na instancia do cliente.porta
  #           cliente.numeracao_cto = self.numeracao # salva a numeracao da cto na instancia do cliente.numeracao_cto
  #           cliente.save() # salva no banco de dados
  #           self.portas.add(cliente) # adiciona a instancia do cliente a porta da cto
  #       else:
  #           raise ValueError(f"Limite de clientes atingido para esta CTO secundaria. max: {self.splitter}")


  def __str__(self):
    return f'CTO: {self.numeracao}'


