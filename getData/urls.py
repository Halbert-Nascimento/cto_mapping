
from django.urls import path
from . import views

urlpatterns = [
    path('',views.pesquisa ,name='pesquisa'),
    path('exibicao/',views.exibicao ,name='exibicao'),
    
]