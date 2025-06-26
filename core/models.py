# core/models.py
from django.db import models
from django.core.cache import cache
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from PIL import Image
import os

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


def upload_imagem_site(instance, filename):
    """Define o caminho de upload baseado no tipo da imagem"""
    return f"site_imagens/{instance.tipo}/{filename}"


# Manager customizado para consultas otimizadas
class ImagemSiteManager(models.Manager):
    def ativas(self):
        return self.filter(ativo=True)
    
    def por_tipo(self, tipo):
        return self.ativas().filter(tipo=tipo).order_by('ordem')
    
    def hero_slider(self):
        return self.por_tipo('hero_slider')
    
    def galeria_home(self):
        return self.por_tipo('galeria')


class ImagemSite(models.Model):
    class TipoImagem(models.TextChoices):
        # Home
        HERO_SLIDER = "hero_slider", "Hero Slider (Home)"
        PATROCINADORES = "patrocinadores", "Patrocinadores"
        LOGO_PEQUENA = "logo_pequena", "Logo Pequena"
        LOGO_GRANDE = "logo_grande", "Logo Grande"
        GALERIA = "galeria", "Galeria (Home)"
        
        # Sobre
        TOPO_SOBRE = "topo_sobre", "Imagem no Topo (Sobre)"
        MEIO_SOBRE = "meio_sobre", "Imagem no Meio (Sobre)"
        
        # Contato
        TOPO_CONTATO = "topo_contato", "Imagem no Topo (Contato)"
        
        # Notícias
        TOPO_NOTICIA = "topo_noticia", "Imagem no Topo (Notícia)"
        SEM_NOTICIA = "sem_noticia", "Imagem Padrão (Sem Notícia)"

        # Doações
        QR_CODE_PIX = "qr_code_pix", "QR Code Pix"

    # Configurações de limite por tipo
    LIMITES_POR_TIPO = {
        'logo_pequena': 1,
        'logo_grande': 1,
        'topo_sobre': 1,
        'meio_sobre': 1,
        'topo_contato': 1,
        'topo_noticia': 1,
        'sem_noticia': 1,
        'qr_code_pix': 1,
        # hero_slider, galeria e patrocinadores podem ter múltiplas imagens
    }

    tipo = models.CharField(
        max_length=30,
        choices=TipoImagem.choices,
        help_text="Selecione onde esta imagem será utilizada"
    )
    imagem = models.ImageField(
        upload_to=upload_imagem_site,
        help_text="Formatos aceitos: JPG, PNG, WebP"
    )
    titulo = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Título da imagem (usado em alt text)"
    )
    descricao = models.TextField(
        blank=True,
        help_text="Descrição detalhada para acessibilidade"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Texto alternativo para acessibilidade (se vazio, usará o título)"
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Marque para exibir esta imagem no site"
    )
    ordem = models.PositiveIntegerField(
        default=0,
        help_text="Ordem de exibição (menor número aparece primeiro)"
    )
    
    # Campos para otimização
    tamanho_arquivo = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Tamanho do arquivo em bytes"
    )
    largura = models.PositiveIntegerField(null=True, blank=True)
    altura = models.PositiveIntegerField(null=True, blank=True)
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["tipo", "ordem", "-criado_em"]
        verbose_name = "Imagem do Site"
        verbose_name_plural = "Imagens do Site"
        indexes = [
            models.Index(fields=['tipo', 'ativo']),
            models.Index(fields=['ordem']),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo or f'ID {self.id}'}"

    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Verifica limites por tipo
        if self.tipo in self.LIMITES_POR_TIPO:
            limite = self.LIMITES_POR_TIPO[self.tipo]
            existing = ImagemSite.objects.filter(tipo=self.tipo, ativo=True)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            
            if existing.count() >= limite:
                raise ValidationError(
                    f"Já existe o número máximo ({limite}) de imagens ativas para '{self.get_tipo_display()}'"
                )

    def save(self, *args, **kwargs):
        # Se alt_text estiver vazio, usa o título
        if not self.alt_text and self.titulo:
            self.alt_text = self.titulo
            
        super().save(*args, **kwargs)
        
        # Atualiza informações da imagem após salvar
        if self.imagem:
            self._update_image_info()

    def _update_image_info(self):
        """Atualiza informações técnicas da imagem"""
        try:
            # Tamanho do arquivo
            self.tamanho_arquivo = self.imagem.size
            
            # Dimensões da imagem
            with Image.open(self.imagem.path) as img:
                self.largura, self.altura = img.size
                
            # Salva sem triggerar save() novamente
            ImagemSite.objects.filter(pk=self.pk).update(
                tamanho_arquivo=self.tamanho_arquivo,
                largura=self.largura,
                altura=self.altura
            )
        except Exception:
            pass  # Se der erro, ignora

    @property
    def tamanho_formatado(self):
        """Retorna o tamanho do arquivo formatado"""
        if not self.tamanho_arquivo:
            return "N/A"
        
        if self.tamanho_arquivo < 1024:
            return f"{self.tamanho_arquivo} bytes"
        elif self.tamanho_arquivo < 1024 * 1024:
            return f"{self.tamanho_arquivo / 1024:.1f} KB"
        else:
            return f"{self.tamanho_arquivo / (1024 * 1024):.1f} MB"

    @property
    def dimensoes(self):
        """Retorna as dimensões formatadas"""
        if self.largura and self.altura:
            return f"{self.largura} x {self.altura}px"
        return "N/A"

    def get_alt_text(self):
        """Retorna o texto alternativo apropriado"""
        return self.alt_text or self.titulo or f"Imagem {self.get_tipo_display()}"
    
    objects = ImagemSiteManager()