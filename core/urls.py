from django.urls import path
from .views import HomeView, SobreView, ContatoView, DoacaoView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('doacao/', DoacaoView.as_view(), name='doacao'),
]
