from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('teste/', views.teste_remover, name='teste_remover'),
]