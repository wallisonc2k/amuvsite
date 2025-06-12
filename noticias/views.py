# noticias/views.py
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Noticia
from datetime import datetime, timedelta
import calendar


class CalendarioView(ListView):
    model = Noticia
    template_name = 'noticias/calendario.html'
    context_object_name = 'eventos'
    
    def get_queryset(self):
        # Filtra apenas eventos
        return Noticia.objects.filter(categoria='evento').order_by('data_evento')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pega o mês e ano atual ou dos parâmetros
        hoje = timezone.now()
        mes_param = self.request.GET.get('mes')
        ano_param = self.request.GET.get('ano')
        
        if mes_param and ano_param:
            try:
                mes = int(mes_param)
                ano = int(ano_param)
            except ValueError:
                mes, ano = hoje.month, hoje.year
        else:
            mes, ano = hoje.month, hoje.year
        
        # Dados do calendário
        context['mes_atual'] = mes
        context['ano_atual'] = ano
        context['nome_mes'] = calendar.month_name[mes]
        context['hoje'] = hoje.date()
        
        # Eventos do mês
        inicio_mes = datetime(ano, mes, 1).date()
        if mes == 12:
            fim_mes = datetime(ano + 1, 1, 1).date() - timedelta(days=1)
        else:
            fim_mes = datetime(ano, mes + 1, 1).date() - timedelta(days=1)
            
        eventos_mes = Noticia.objects.filter(
            categoria='evento',
            data_evento__date__range=[inicio_mes, fim_mes]
        ).order_by('data_evento')
        
        context['eventos_mes'] = eventos_mes
        
        # Breadcrumb
        context['breadcrumb_items'] = [
            {"name": "Calendário de Eventos"}
        ]
        
        return context

def calendario_api(request):
    """API para buscar eventos do calendário via AJAX"""
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')
    
    if not mes or not ano:
        return JsonResponse({'error': 'Mês e ano são obrigatórios'}, status=400)
    
    try:
        mes = int(mes)
        ano = int(ano)
    except ValueError:
        return JsonResponse({'error': 'Mês e ano devem ser números'}, status=400)
    
    # Busca eventos do mês
    inicio_mes = datetime(ano, mes, 1).date()
    if mes == 12:
        fim_mes = datetime(ano + 1, 1, 1).date() - timedelta(days=1)
    else:
        fim_mes = datetime(ano, mes + 1, 1).date() - timedelta(days=1)
    
    eventos = Noticia.objects.filter(
        categoria='evento',
        data_evento__date__range=[inicio_mes, fim_mes]
    ).values(
        'id', 'titulo', 'data_evento', 'local_evento', 'slug'
    ).order_by('data_evento')
    
    # Converte para formato JSON
    eventos_data = []
    for evento in eventos:
        eventos_data.append({
            'id': evento['id'],
            'titulo': evento['titulo'],
            'data': evento['data_evento'].strftime('%Y-%m-%d'),
            'dia': evento['data_evento'].day,
            'hora': evento['data_evento'].strftime('%H:%M'),
            'local': evento['local_evento'] or '',
            'slug': evento['slug']
        })
    
    return JsonResponse({
        'eventos': eventos_data,
        'mes': mes,
        'ano': ano,
        'nome_mes': calendar.month_name[mes]
    })

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
        
       # Próximos eventos para o widget do calendário
        proximos_eventos = Noticia.objects.filter(
            categoria='evento',
            data_evento__gte=timezone.now()
        ).order_by('data_evento')[:3]
        context['proximos_eventos'] = proximos_eventos

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
