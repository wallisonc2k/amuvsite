# membros/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .models import Pagamento
from django.shortcuts import redirect

class PainelMembroView(LoginRequiredMixin, TemplateView):
    template_name = 'membros/painel.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("painel_admin:admin_dashboard")
        return super().dispatch(request, *args, **kwargs) 

class HistoricoPagamentosView(LoginRequiredMixin, ListView):
    model = Pagamento
    template_name = 'membros/historico_pagamentos.html'
    context_object_name = 'pagamentos'

    def get_queryset(self):
        return Pagamento.objects.filter(membro=self.request.user).order_by('-data_pagamento')
    

class EditPerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'membros/editar_perfil.html'