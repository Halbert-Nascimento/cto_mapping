
from django.urls import path
from . import views

urlpatterns = [
       path('',views.cadastro_splitter, name='cadastro_splitter' ),
       path('ctop/',views.cadastro_ctoP, name='cadastro_ctop' ),
       path('ctos/',views.cadastro_ctoS, name='cadastro_ctos' ),
]