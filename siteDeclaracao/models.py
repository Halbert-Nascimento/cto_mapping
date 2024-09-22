from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import uuid

# Modelo Relationship representa um relacionamento entre duas pessoas.
# Ele contém informações como nomes, data e hora de início do relacionamento, 
# uma mensagem personalizada, um link para o YouTube, e campos opcionais para upload de fotos e arquivos.

class Relationship(models.Model):
    name1 = models.CharField(max_length=100)  # Nome da primeira pessoa no relacionamento
    name2 = models.CharField(max_length=100)  # Nome da segunda pessoa no relacionamento
    relationship_start_date = models.DateField()  # Data de início do relacionamento
    relationship_start_time = models.TimeField()  # Hora de início do relacionamento
    message = models.TextField()  # Mensagem personalizada sobre o relacionamento
    youtube_link = models.URLField()  # Link do YouTube associado ao relacionamento
    photos = models.ImageField(upload_to='relationship_photos/', blank=True, null=True)  # Upload de fotos, opcional
    arquivos = models.FileField(upload_to='relationship_files/', blank=True, null=True)  # Upload de arquivos, opcional

    def __str__(self):
        # Representação em string do modelo: retorna os nomes das duas pessoas
        return f"{self.name1} & {self.name2}, id: {self.id}"

# Modelo Fotos representa as fotos associadas a um Relationship.
# Cada instância de Fotos está vinculada a um Relationship através de uma ForeignKey.
class Fotos(models.Model):
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, related_name='fotos')  
    # Chave estrangeira para o relacionamento. Quando o Relationship for deletado, as fotos também serão deletadas.
    name = models.CharField(max_length=100, default='Fotos')  # Nome da foto, com valor padrão 'Fotos'
    imagem = models.ImageField(upload_to='relationship_files/', blank=True, null=True)  # Upload de imagem, opcional

    def __str__(self):
        # Representação em string do modelo: retorna o nome da foto
        return self.name

# Sinal post_delete que é disparado após a exclusão de uma instância do modelo Fotos.
# Sua função é remover o arquivo de imagem do sistema de arquivos após a exclusão do registro de Fotos no banco de dados.
@receiver(post_delete, sender=Fotos)
def delete_imagem_on_delete(sender, instance, **kwargs):
    """
    Função de sinal que remove o arquivo de imagem do sistema de arquivos
    quando uma instância do modelo Fotos é deletada do banco de dados.
    """
    if instance.imagem:
        # Verifica se a imagem existe no sistema de arquivos e se é um arquivo
        if os.path.isfile(instance.imagem.path):
            # Remove a imagem do sistema de arquivos
            os.remove(instance.imagem.path)

# Sinal post_delete que é disparado após a exclusão de uma instância do modelo Relationship.
# Sua função é remover o arquivo associado ao campo 'arquivos' do sistema de arquivos 
# após a exclusão do registro de Relationship no banco de dados.
@receiver(post_delete, sender=Relationship)
def delete_arquivos_on_delete(sender, instance, **kwargs):
    """
    Função de sinal que remove o arquivo do sistema de arquivos 
    quando uma instância do modelo Relationship é deletada do banco de dados.
    """
    if instance.arquivos:
        # Verifica se o arquivo existe no sistema de arquivos e se é um arquivo
        if os.path.isfile(instance.arquivos.path):
            # Remove o arquivo do sistema de arquivos
            os.remove(instance.arquivos.path)



## MODELOS PARA APLICATIVO DE CRIAÇÃO DE PÁGINAS TEMPORÁRIAS
class TemporaryPageData(models.Model):
    session_id = models.CharField(max_length=100)
    attempt_id = models.CharField(max_length=200, unique=True, default=(uuid.uuid4()))
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    relationship_start_date = models.DateField()
    relationship_start_time = models.TimeField()
    message = models.TextField()
    youtube_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name1}&{self.name2}: TemporaryPageData for session {self.session_id} "
    

class TemporaryPageImage(models.Model):
    TemporaryPageData = models.ForeignKey(TemporaryPageData, on_delete=models.CASCADE, related_name='temporary_images')
    image = models.ImageField(upload_to='temporary_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temporary_Image for {self.image}"
    
@receiver(post_delete, sender=TemporaryPageImage)
def delete_imagem_on_delete(sender, instance, **kwargs):
    """
    Função de sinal que remove o arquivo de imagem do sistema de arquivos
    quando uma instância do modelo Fotos é deletada do banco de dados.
    """
    if instance.image:
        # Verifica se a imagem existe no sistema de arquivos e se é um arquivo
        if os.path.isfile(instance.image.path):
            # Remove a imagem do sistema de arquivos
            os.remove(instance.image.path)


## MODELOS PARA APLICATIVO DE PAGAMENTO
class DataUserPayment(models.Model):
    session_id = models.CharField(max_length=100)
    attempt_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField( blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    payment_status = models.CharField(max_length=100,)
    payment_status_detail = models.CharField(max_length=100, blank=True, null=True)
    payment_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    active_time_month = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: plano de {self.active_time_month} mes(es)"

class PageRelationship(models.Model):
    DataUserPayment = models.OneToOneField(DataUserPayment, on_delete=models.CASCADE, related_name='page_relationship')
    url_access = models.URLField(max_length=150, unique=True)
    url_access_split = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, default='pending')
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    relationship_start_date = models.DateField()
    relationship_start_time = models.TimeField()
    message = models.TextField()
    youtube_link = models.URLField(blank=True, null=True)   


    def __str__(self):
        return f"URL: {self.url_access}"


class PageRelationshipImage(models.Model):
    PageRelationship = models.ForeignKey(PageRelationship, on_delete=models.CASCADE, related_name='page_images')
    image_title = models.CharField(max_length=100 , default='image')
    image = models.ImageField(upload_to='relationship_files/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.image}"

@receiver(post_delete, sender=PageRelationshipImage)
def delete_imagem_on_delete(sender, instance, **kwargs):
    """
    Função de sinal que remove o arquivo de imagem do sistema de arquivos
    quando uma instância do modelo Fotos é deletada do banco de dados.
    """
    if instance.image:
        # Verifica se a imagem existe no sistema de arquivos e se é um arquivo
        if os.path.isfile(instance.image.path):
            # Remove a imagem do sistema de arquivos
            os.remove(instance.image.path)