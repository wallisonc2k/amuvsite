# membros/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView
from .models import Pagamento
from django.shortcuts import redirect
from .forms import MembroForm
from .models import Membro
from django.urls import reverse_lazy
from django.contrib import messages


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
    

class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = Membro
    form_class = MembroForm
    template_name = 'membros/editar_perfil.html'
    success_url = reverse_lazy('membros:painel')
    
    def get_object(self):
        # Retorna o usuário atualmente logado
        return self.request.user
    
    def form_valid(self, form):
        # Processa os interesses (checkboxes)
        interesses = self.request.POST.getlist('interesses')
        form.instance.interesses = interesses
        
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user  # Para compatibilidade com seu template
        return context