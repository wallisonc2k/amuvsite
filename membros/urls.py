from django.urls import path
from .views import PainelMembroView, HistoricoPagamentosView

app_name = 'membros'

urlpatterns = [
    path('painel/', PainelMembroView.as_view(), name='painel'),
    path('pagamentos/', HistoricoPagamentosView.as_view(), name='pagamentos'),
]
