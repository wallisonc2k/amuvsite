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
    context_object_name = 'noticia'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outras_noticias = Noticia.objects.exclude(pk=self.object.pk).order_by('-publicado_em')[:4]
        context['outras_noticias'] = outras_noticias if outras_noticias.exists() else None
        return context


