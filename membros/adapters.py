# membros/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_staff:
            return reverse('painel_admin:admin_dashboard')
        return reverse('membros:painel')
