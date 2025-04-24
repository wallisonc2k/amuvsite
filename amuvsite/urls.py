from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('noticias/', include('noticias.urls')),
    path('membros/', include('membros.urls')),
    path('accounts/', include('allauth.urls')),  # login/registro
]
