# noticias/views.py
from django.views.generic import ListView, DetailView
from .models import Noticia

class ListaNoticiasView(ListView):
    model = Noticia
    template_name = 'noticias/lista.html'
    context_object_name = 'noticias'
    ordering = ['-publicado_em']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pegando a notícia mais recente (em destaque)
        noticia_destaque = Noticia.objects.order_by('-publicado_em').first()
        # Pegando as demais notícias (exceto a notícia em destaque)
        # noticias = Noticia.objects.exclude(id=noticia_destaque.id).order_by('-publicado_em')[:6]
        
        noticias = Noticia.objects.order_by('-publicado_em')[:6]

        # Adicionando ao contexto
        context['noticia_destaque'] = noticia_destaque
        context['noticias'] = noticias
        context['breadcrumb_items'] = [
            {"name": "Noticias"}
        ]
        return context

class DetalheNoticiaView(DetailView):
    model = Noticia
    template_name = 'noticias/detalhe.html'
    context_object_name = 'noticia'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Buscar até 4 outras notícias, ignorando a atual
        context['outras_noticias'] = (
            Noticia.objects
            .exclude(pk=self.object.pk)
            .order_by('-publicado_em')[:4]
        )
        return context



