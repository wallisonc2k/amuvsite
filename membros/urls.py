from django.urls import path
from .views import PainelMembroView, HistoricoPagamentosView, EditarPerfilView

app_name = 'membros'

urlpatterns = [
    path('painel/', PainelMembroView.as_view(), name='painel'),
    path('pagamentos/', HistoricoPagamentosView.as_view(), name='pagamentos'),
    path('editar-perfil/', EditarPerfilView.as_view(), name='editar_perfil'),
]