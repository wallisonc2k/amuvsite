from django import template
from django.core.cache import cache
from ..models import SiteConfigContato

register = template.Library()

@register.simple_tag
def site_titulo():
    """{% site_titulo %}"""
    return _get_config_value('site_titulo', 'Meu Site')

@register.simple_tag  
def contato_email():
    """{% contato_email %}"""
    return _get_config_value('contato_email', '')

@register.simple_tag
def suporte_email():
    """{% suporte_email %}"""
    return _get_config_value('suporte_email', '')

@register.simple_tag
def telefone_contato():
    """{% telefone_contato %}"""
    return _get_config_value('telefone_contato', '')

@register.simple_tag
def whatsapp_numero():
    """{% whatsapp_numero %}"""
    return _get_config_value('whatsapp_numero', '')

@register.simple_tag
def chave_pix():
    """{% chave_pix %}"""
    return _get_config_value('chave_pix', '')

@register.simple_tag
def telefone_link():
    """{% telefone_link %} - Retorna tel:+5511999999999"""
    telefone = _get_config_value('telefone_contato', '')
    if telefone:
        return f"tel:{telefone}"
    return ""

@register.simple_tag
def whatsapp_link():
    """{% whatsapp_link %} - Retorna https://wa.me/5511999999999"""
    whatsapp = _get_config_value('whatsapp_numero', '')
    if whatsapp:
        numero_limpo = ''.join(filter(str.isdigit, whatsapp))
        return f"https://wa.me/+55{numero_limpo}"
    return ""

@register.simple_tag
def email_contato_link():
    """{% email_contato_link %} - Retorna mailto:contato@site.com"""
    email = _get_config_value('contato_email', '')
    if email:
        return f"mailto:{email}"
    return ""

@register.simple_tag
def email_suporte_link():
    """{% email_suporte_link %} - Retorna mailto:suporte@site.com"""
    email = _get_config_value('suporte_email', '')
    if email:
        return f"mailto:{email}"
    return ""

# Função auxiliar para cache individual
def _get_config_value(field_name, default=''):
    """Pega valor do cache ou do banco"""
    cache_key = f"config_{field_name}"
    value = cache.get(cache_key)
    
    if value is None:
        config = SiteConfigContato.get_config()
        if config:
            value = getattr(config, field_name, default)
            cache.set(cache_key, value, 300)  # 5 minutos
        else:
            value = default
    
    return value