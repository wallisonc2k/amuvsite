from django import template
from ..models import SiteConfig

register = template.Library()

@register.simple_tag
def get_site_config():
    """Retorna o objeto de configuração do site"""
    return SiteConfig.get_config()