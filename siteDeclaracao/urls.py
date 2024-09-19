from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.relationship_form, name='index'),
    path('home/', views.index, name='index'),
    path('criarSite/', views.criarSite, name='criarSite'),
    path('saveTemporaryData/', views.saveTemporaryData, name='saveTemporaryData'),
    path('page/<str:nome>', views.url_personalizada, name='url_personalizada'),
    path('home/<str:pk>', views.url_personalizadaID, name='url_personalizadaID'), 
    #pagina de teste token
    path('testeToken/', views.testeToken, name='testeToken'),

    #pagina  para redirecionamento da API de pagamento sucess, fail, pending
    path('success/', views.success, name='success'),
    path('fail/', views.success, name='success'),
    path('pending/', views.success, name='success'),

#     path('fail/', views.fail, name='fail'),
#     path('pending/', views.pending, name='pending'),
] 
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)