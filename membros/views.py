# membros/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .models import Pagamento

class PainelMembroView(LoginRequiredMixin, TemplateView):
    template_name = 'membros/painel.html'

class HistoricoPagamentosView(LoginRequiredMixin, ListView):
    model = Pagamento
    template_name = 'membros/historico_pagamentos.html'
    context_object_name = 'pagamentos'

    def get_queryset(self):
        return Pagamento.objects.filter(membro=self.request.user).order_by('-data_pagamento')