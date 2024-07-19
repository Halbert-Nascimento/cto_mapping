
from django.urls import path
from . import views

urlpatterns = [
    path('',views.pesquisa ,name='pesquisa'),
    path('exibicao/',views.exibicao ,name='exibicao'),
    path('test/', views.getCTO_P, name='testeCTOP'),
    path('pesquisa_cliente/', views.pesquisa_cliente, name='pesquisa_cliente'),
    path('pesquisa_cto/', views.pesquisa_cto, name='pesquisa_cto'),
    path('pesquisa_cto/<int:pk>', views.info_cto, name='info_cto'),
    
]