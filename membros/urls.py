from django.urls import path
from .views import PainelMembroView, HistoricoPagamentosView, EditPerfilView

app_name = 'membros'

urlpatterns = [
    path('painel/', PainelMembroView.as_view(), name='painel'),
    path('pagamentos/', HistoricoPagamentosView.as_view(), name='pagamentos'),
    path('editar_perfil/', EditPerfilView.as_view(), name='editar_perfil'),
]
