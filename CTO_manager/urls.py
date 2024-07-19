
from django.urls import path
from . import views

urlpatterns = [
       path('',views.cadastro_splitter, name='cadastro_splitter' ),
       path('ctop/',views.cadastro_ctoP, name='cadastro_ctop' ),
       path('ctos/',views.cadastro_ctoS, name='cadastro_ctos' ),
       path('instalacao/',views.instalacao, name='instalacao'),
       path('atualizarendereco/', views.mudanca_endereco, name='atualizarendereco'),
       path('atualizar_cliente/<int:pk>/', views.atualizar_cliente, name='atualizar_cliente'),
       
]