from django.db import models
from django.conf import settings  # Importa as configurações do projeto

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=255, blank=True)
    conteudo = models.TextField()
    imagem_capa = models.ImageField(upload_to='noticias/capas/', blank=True, null=True)
    publicado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    # Usa o modelo de usuário definido em AUTH_USER_MODEL
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo
