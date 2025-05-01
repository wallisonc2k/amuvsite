# core/views.py
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .models import Contato
from .forms import ContatoForm
from noticias.models import Noticia
from django.shortcuts import render
from .utils import listar_imagens_estaticas, listar_imagens_com_descricao


class HomeView(TemplateView):
    template_name = 'core/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        imagens_hero_slider = listar_imagens_estaticas('shared/img/hero_slider') # Adiciona as imagens do hero Slider automaticamente
        imagens_swiper = listar_imagens_com_descricao()

        context['imagens_hero_slider'] = imagens_hero_slider
        context['imagens_swiper'] = imagens_swiper
        context['noticias'] = Noticia.objects.order_by('-publicado_em')[:2]  # últimas 3 notícias
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
