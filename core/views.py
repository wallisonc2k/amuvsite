# core/views.py
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .models import Contato
from .forms import ContatoForm

class HomeView(TemplateView):
    template_name = 'core/home.html'

class SobreView(TemplateView):
    template_name = 'core/sobre.html'

class ContatoView(FormView):
    template_name = 'core/contato.html'
    form_class = ContatoForm
    success_url = reverse_lazy('core:contato')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class DoacaoView(TemplateView):
    template_name = "core/doacao.html"
