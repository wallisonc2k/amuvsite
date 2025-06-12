from .models import Noticia

def common_context(request):
    """
    Fornece um contexto comum para todos os templates,
    incluindo as notícias mais lidas.
    """
    noticias_mais_lidas = Noticia.objects.order_by('-visualizacoes')[:5] # Pega as 5 mais lidas

    return {
        'noticias_mais_lidas': noticias_mais_lidas,
    }