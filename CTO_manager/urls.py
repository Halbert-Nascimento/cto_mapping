
from django.urls import path
from . import views

urlpatterns = [
       path('',views.cadastro_splitter, name='cadastro_splitter' ),
       path('ctop/',views.cadastro_ctop, name='cadastro_ctop' ),
]