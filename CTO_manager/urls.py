
from django.urls import path
from . import views

urlpatterns = [
       path('',views.index, name='homes' ),
       path('pag/',views.pag, name='pag' ),
]