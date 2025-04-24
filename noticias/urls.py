from django.urls import path
from .views import ListaNoticiasView, DetalheNoticiaView

app_name = 'noticias'

urlpatterns = [
    path('', ListaNoticiasView.as_view(), name='lista'),
    path('<int:pk>/', DetalheNoticiaView.as_view(), name='detalhe'),
]
