# noticias/views.py
from django.views.generic import ListView, DetailView
from .models import Noticia

class ListaNoticiasView(ListView):
    model = Noticia
    template_name = 'noticias/lista.html'
    context_object_name = 'noticias'
    ordering = ['-publicado_em']

class DetalheNoticiaView(DetailView):
    model = Noticia
    template_name = 'noticias/detalhe.html'
