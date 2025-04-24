from django.urls import path
from .views import HomeView, SobreView, ContatoView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
]
