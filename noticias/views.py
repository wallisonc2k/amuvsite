# noticias/views.py
from django.views.generic import ListView, DetailView
from .models import Noticia
from django.db.models import F


class ListaNoticiasView(ListView):
    model = Noticia
    template_name = 'noticias/lista.html'
    context_object_name = 'noticias'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.GET.get('categoria')
        
        if categoria and categoria != 'todos':
            queryset = queryset.filter(categoria=categoria)
            
        return queryset.order_by('-publicado_em')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria_atual = self.request.GET.get('categoria', 'todos')
        
        # Adicionando as categorias para o filtro
        context['categoria_atual'] = categoria_atual
        context['categorias'] = Noticia.get_categorias_para_filtro()
        
        # Define o breadcrumb
        context['breadcrumb_items'] = [
            {"name": "Notícias"}
        ]
        
        # Preserva o parâmetro de categoria na paginação
        if categoria_atual and categoria_atual != 'todos':
            # Se estiver em páginas posteriores, mantém a categoria na navegação
            pagination_links = context.get('page_obj', None)
            if pagination_links:
                for page_number in range(1, pagination_links.paginator.num_pages + 1):
                    pagination_links.paginator.page(page_number).categoria_param = f"?categoria={categoria_atual}"
                    if page_number != context['page_obj'].number:
                        # Mantém o parâmetro categoria nas páginas
                        pagination_links.paginator.page(page_number).url = f"?categoria={categoria_atual}&page={page_number}"
        
        return context


class DetalheNoticiaView(DetailView):
    model = Noticia
    template_name = 'noticias/detalhe.html'
    context_object_name = 'noticia'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.visualizacoes += 1
        obj.save(update_fields=['visualizacoes'])
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Outras notícias recentes, excluindo a atual
        context['outras_noticias'] = (
            Noticia.objects
            .exclude(pk=self.object.pk)
            .order_by('-publicado_em')[:4]
        )
        # Notícias mais lidas (excluindo a atual)
        context['noticias_mais_lidas'] = (
            Noticia.objects
            .exclude(pk=self.object.pk)
            .order_by('-visualizacoes')[:3]
        )
        return context



# Para listar apenas eventos
class EventosListView(ListView):
    model = Noticia
    template_name = 'eventos/lista.html'
    context_object_name = 'eventos'
    
    def get_queryset(self):
        return Noticia.objects.filter(categoria='evento')
