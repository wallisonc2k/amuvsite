from django.urls import path
from .views import ListaNoticiasView, DetalheNoticiaView, CalendarioView, calendario_api

app_name = 'noticias'

urlpatterns = [
    # URLs do calendário
    path('', ListaNoticiasView.as_view(), name='lista'),
    
    path('calendario/', CalendarioView.as_view(), name='calendario'),
    path('api/calendario/', calendario_api, name='calendario_api'),
 
    path('<slug:slug>/', DetalheNoticiaView.as_view(), name='detalhe'),
]
