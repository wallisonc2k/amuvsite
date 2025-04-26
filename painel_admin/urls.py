from django.urls import path
from .views_admin import AdminDashboardView
from .views_news import (AdminNewsListView, AdminNewsCreateView, AdminNewsUpdateView, AdminNewsDeleteView)
from .views_payments import (AdminPaymentsListView, AdminPaymentsUpdateView)

app_name = 'painel_admin'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),

    # Notícias
    path('noticias/', AdminNewsListView.as_view(), name='news_list'),
    path('noticias/nova/', AdminNewsCreateView.as_view(), name='news_create'),
    path('noticias/<int:pk>/editar/', AdminNewsUpdateView.as_view(), name='news_edit'),
    path('noticias/<int:pk>/remover/', AdminNewsDeleteView.as_view(), name='news_delete'),

    # Pagamentos
    path('pagamentos/', AdminPaymentsListView.as_view(), name='payments_list'),
    path('pagamentos/<int:pk>/editar/', AdminPaymentsUpdateView.as_view(), name='payments_edit'),
]