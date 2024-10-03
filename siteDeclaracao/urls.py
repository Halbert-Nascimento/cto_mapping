from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.relationship_form, name='index'),
    path('home/', views.index, name='index'),
    path('criarSite/', views.criarSite, name='criarSite'),
    path('saveTemporaryData/', views.saveTemporaryData, name='saveTemporaryData'),
    path('post/<str:url>', views.url_personalizada, name='url_personalizada'),
    path('home/<str:pk>', views.url_personalizadaID, name='url_personalizadaID'),
    path('termosdeuso/', views.termosDeUso, name='termosDeUso'),
        
    #pagina  para redirecionamento da API de pagamento sucess, fail, pending
    path('success/', views.success, name='success'), #pagina de sucesso
    path('fail/', views.fail, name='fail'), #pagina de falha
    path('pending/', views.pending, name='pending'), #pagina de pendente
    path('confirmacao/', views.confirmacao, name='confirmacao'), #pagina de feedback de pagamento em caso de sucesso
] 
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)