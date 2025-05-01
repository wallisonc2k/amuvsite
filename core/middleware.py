from .models import SiteConfig

class SiteConfigMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Código executado em cada requisição
        response = self.get_response(request)
        return response
    
    def process_template_response(self, request, response):
        # Adiciona contexto de configuração em todas as respostas com template
        if hasattr(response, 'context_data'):
            response.context_data['site_config'] = SiteConfig.get_config()
        return response