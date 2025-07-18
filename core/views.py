# core/views.py
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from .models import Contato, ImagemSite
from .forms import ContatoForm
from .utils import listar_imagens_estaticas, listar_imagens_com_descricao
from noticias.models import Noticia


class HomeView(TemplateView):
    template_name = 'core/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        imagens_swiper = listar_imagens_com_descricao()

        context['imagens_swiper'] = imagens_swiper
        context['noticias'] = Noticia.objects.filter(categoria='noticia').order_by('-publicado_em')[:2]  # últimas 3 notícias
        context['eventos'] = Noticia.objects.filter(categoria='evento',
                                                    data_evento__gte=timezone.now()
                                                    ).order_by('data_evento')[:2]  # últimos 3 eventos

        return context

class SobreView(TemplateView):
    template_name = 'core/sobre.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb_items'] = [
            {"name": "Sobre"}
        ]
        return context

class ContatoView(FormView):
    template_name = 'core/contato.html'
    form_class = ContatoForm
    success_url = reverse_lazy('core:contato')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb_items'] = [
            {"name": "Contato"}
        ]
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class DoacaoView(TemplateView):
    template_name = "core/doacao.html"


def error_404_view(request, exception):
    return render(request, 'erro/404.html', status=404)
