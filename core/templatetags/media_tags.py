# media_site/templatetags/media_tags.py

from django import template
from django.db.models import Q
from ..models import ImagemSite

register = template.Library()

@register.inclusion_tag('partials/hero_slider.html')
def hero_slider():
    """Renderiza o hero slider da home"""
    imagens = ImagemSite.objects.por_tipo('hero_slider')
    return {'imagens': imagens}

@register.simple_tag
def hero_slider_json():
    """Retorna as URLs das imagens do hero slider em formato JSON para Alpine.js"""
    import json
    imagens = ImagemSite.objects.por_tipo('hero_slider')
    urls = [imagem.imagem.url for imagem in imagens] if imagens.exists() else []
    return json.dumps(urls)

@register.inclusion_tag('partials/galeria_home.html')
def galeria_home():
    """Renderiza a galeria da home"""
    imagens = ImagemSite.objects.por_tipo('galeria')
    return {'imagens': imagens}

@register.simple_tag
def get_imagem_site(tipo):
    """Retorna uma imagem específica por tipo"""
    try:
        return ImagemSite.objects.por_tipo(tipo).first()
    except ImagemSite.DoesNotExist:
        return None

@register.simple_tag
def get_imagens_site(tipo):
    """Retorna múltiplas imagens por tipo"""
    return ImagemSite.objects.por_tipo(tipo)

@register.simple_tag
def logo_pequena():
    """Retorna a logo pequena"""
    return ImagemSite.objects.por_tipo('logo_pequena').first()

@register.simple_tag
def logo_grande():
    """Retorna a logo grande"""
    return ImagemSite.objects.por_tipo('logo_grande').first()

@register.filter
def get_alt_text(imagem):
    """Filtro para obter o alt text apropriado"""
    if imagem:
        return imagem.get_alt_text()
    return ""