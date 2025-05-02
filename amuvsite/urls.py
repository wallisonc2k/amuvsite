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

    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# È PARA COMEMTAR QUANDO ESTIVER EM PRODUÇÃO
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Define o manipulador de erro 404
handler404 = 'core.views.error_404_view'