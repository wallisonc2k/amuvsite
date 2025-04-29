# membros/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_staff:
            return reverse('painel_admin:admin_dashboard')
        return reverse('membros:painel')
    
    
    def save_user(self, request, user, form, commit=True):
        """
        Este método é chamado quando um novo usuário se registra através do AllAuth
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Personalize aqui se necessário
        
        if commit:
            user.save()
        return user