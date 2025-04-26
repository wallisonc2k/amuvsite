from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from membros.models import Pagamento

@method_decorator(staff_member_required, name='dispatch')
class AdminPaymentsListView(ListView):
    model = Pagamento
    template_name = 'painel_admin/pagamentos_list.html'
    context_object_name = 'pagamentos'

@method_decorator(staff_member_required, name='dispatch')
class AdminPaymentsUpdateView(UpdateView):
    model = Pagamento
    fields = ['valor', 'data_pagamento', 'status']
    template_name = 'painel_admin/pagamento_form.html'
    success_url = reverse_lazy('painel_admin:pagamentos_list')