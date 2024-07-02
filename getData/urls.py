
from django.urls import path
from . import views

urlpatterns = [
    path('',views.pesquisa ,name='teste'),
    
]