# core/models.py
from django.db import models
from django.core.cache import cache
from colorfield.fields import ColorField

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True) 
    email = models.EmailField()
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.email}"


# Model para configuração das cores do site
class SiteConfig(models.Model):
    """Configurações globais de aparência do site"""
    # Cores primárias
    cor_primaria = ColorField(default='#B91C1C', verbose_name='Cor primária')
    cor_primaria_hover = ColorField(default='#991B1B', verbose_name='Cor primária (hover)')
    
    # Cores secundárias
    cor_secundaria = ColorField(default='#1F2937', verbose_name='Cor secundária')
    cor_texto = ColorField(default='#1F2937', verbose_name='Cor de texto principal')
    cor_texto_claro = ColorField(default='#6B7280', verbose_name='Cor de texto secundário')
    
    # Fundos
    cor_fundo_hero = ColorField(default='#B91C1C', verbose_name='Cor de fundo do Hero')
    cor_fundo_secoes = ColorField(default='#F3F4F6', verbose_name='Cor de fundo das seções')
    cor_fundo_cards = ColorField(default='#FFFFFF', verbose_name='Cor de fundo dos cards')
    cor_fundo_footer = ColorField(default='#1F2937', verbose_name='Cor de fundo do rodapé')
    
    # Elementos visuais
    cor_divisor = ColorField(default='#B91C1C', verbose_name='Cor dos divisores')
    cor_borda_cards = ColorField(default='#B91C1C', verbose_name='Cor da borda dos cards')
    
    # Configurações
    ativo = models.BooleanField(default=True, verbose_name='Configuração ativa')
    ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última atualização')
    
    class Meta:
        verbose_name = 'Configuração de Tema'
        verbose_name_plural = 'Configurações de Tema'
    
    def save(self, *args, **kwargs):
        # Desativa outras configurações se esta for ativada
        if self.ativo:
            SiteConfig.objects.exclude(pk=self.pk).update(ativo=False)
        
        # Limpa o cache ao salvar
        cache.delete('site_config')
        
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Obtém a configuração ativa (com cache)"""
        config = cache.get('site_config')
        if config is None:
            try:
                config = cls.objects.get(ativo=True)
                cache.set('site_config', config, 3600)  # Cache por 1 hora
            except cls.DoesNotExist:
                config = cls.objects.create()  # Cria com valores padrão
                cache.set('site_config', config, 3600)
        return config
    
    def __str__(self):
        return f"Configuração de Tema ({self.ultima_atualizacao.strftime('%d/%m/%Y %H:%M')})"


class SiteConfigContato(models.Model):
    # Contatos
    contato_email = models.EmailField("E-mail de Contato")
    suporte_email = models.EmailField("E-mail de Suporte") 
    telefone_contato = models.CharField("Telefone", max_length=20)
    whatsapp_numero = models.CharField("WhatsApp", max_length=20, blank=True)
    
    # Dados do Site
    site_titulo = models.CharField("Título do Site", max_length=100)
    chave_pix = models.CharField("Chave PIX", max_length=100)
    
    # Controle
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"

    def __str__(self):
        return f"Config - {self.site_titulo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Limpa cache
        cache.delete_many(['site_titulo', 'contato_email', 'suporte_email', 
                          'telefone_contato', 'whatsapp_numero', 'chave_pix'])

    @classmethod
    def get_config(cls):
        config = cache.get('site_config_obj')
        if not config:
            config = cls.objects.first()
            if config:
                cache.set('site_config_obj', config, 300)
        return config