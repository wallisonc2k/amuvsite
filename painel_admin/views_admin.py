from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
from core.models import SiteConfig
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import TemplateView
from noticias.models import Noticia
from membros.models import Membro

hoje = timezone.now().date()

@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'painel_admin/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_news'] = Noticia.objects.filter(categoria="noticia").count()
        context['total_events'] = Noticia.objects.filter(categoria="evento").count()
        context['recent_news'] = Noticia.objects.filter(publicado_em__date=hoje).count()
        context['total_members'] = Membro.objects.count()
        return context


class ThemePreviewView(UserPassesTestMixin, TemplateView):
    template_name = 'painel_admin/theme_preview.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_config'] = SiteConfig.get_config()
        return context