from django.db import models
from django.conf import settings  # Importa as configurações do projeto
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Noticia(models.Model):
    CATEGORIA_CHOICES = [
        ('noticia', 'Notícia'),
        ('evento', 'Evento'),
        # Adicione outras categorias conforme necessário
    ]
    

    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=255, blank=True)
    conteudo = RichTextUploadingField()
    resumo = models.TextField(default='', blank=True)
    imagem_capa = models.ImageField(upload_to='noticias/capas/', blank=True, null=True)
    publicado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='noticia')
    
    # Campos específicos para eventos
    data_evento = models.DateTimeField(blank=True, null=True)
    local_evento = models.CharField(max_length=200, blank=True, null=True)

    # Usa o modelo de usuário definido em AUTH_USER_MODEL
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    @classmethod
    def get_categorias_para_filtro(cls):
        # Começa com "Todos"
        categorias = [{'valor': 'todos', 'nome': 'Todos'}]
        # Adiciona todas as categorias do modelo
        for valor, nome in cls.CATEGORIA_CHOICES:
            categorias.append({'valor': valor, 'nome': nome})
        return categorias

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.titulo
