from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('noticias/', include('noticias.urls')),
    path('membros/', include('membros.urls', namespace='membros')),
    path('accounts/', include('allauth.urls')),  # login/registro
    
    # Seu painel administrativo customizado:
    path('painel_admin/', include('painel_admin.urls', namespace='painel_admin')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)