from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import SiteConfig, SiteConfigContato, ImagemSite

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': ('ativo', 'ultima_atualizacao'),
        }),
        ('Cores Principais', {
            'fields': ('cor_primaria', 'cor_primaria_hover', 'cor_secundaria'),
        }),
        ('Cores de Texto', {
            'fields': ('cor_texto', 'cor_texto_claro'),
        }),
        ('Cores de Fundo', {
            'fields': ('cor_fundo_hero', 'cor_fundo_secoes', 'cor_fundo_cards', 'cor_fundo_footer'),
        }),
        ('Elementos Visuais', {
            'fields': ('cor_divisor', 'cor_borda_cards'),
        }),
    )
    readonly_fields = ('ultima_atualizacao',)
    list_display = ('__str__', 'ativo', 'cor_primaria', 'cor_secundaria', 'ultima_atualizacao')
    list_filter = ('ativo',)
    
    def has_delete_permission(self, request, obj=None):
        # Impede a exclusão da última configuração ativa
        if obj and obj.ativo and SiteConfig.objects.filter(ativo=True).count() <= 1:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(SiteConfigContato)
class SiteConfigContatoAdmin(admin.ModelAdmin):
    list_display = ('site_titulo', 'contato_email', 'updated_at')
    
    def has_add_permission(self, request):
        return not SiteConfigContato.objects.exists()


@admin.register(ImagemSite)
class ImagemSiteAdmin(admin.ModelAdmin):
    list_display = [
        'preview_thumbnail', 'tipo', 'titulo', 'dimensoes_info', 
        'tamanho_info', 'ativo', 'ordem', 'atualizado_em'
    ]
    list_filter = ['tipo', 'ativo', 'criado_em']
    search_fields = ['titulo', 'descricao', 'alt_text']
    list_editable = ['ativo', 'ordem']
    readonly_fields = ['preview_image', 'tamanho_arquivo', 'largura', 'altura', 'criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'titulo', 'descricao', 'ativo', 'ordem')
        }),
        ('Imagem', {
            'fields': ('imagem', 'preview_image', 'alt_text')
        }),
        ('Informações Técnicas', {
            'fields': ('tamanho_arquivo', 'largura', 'altura'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_thumbnail(self, obj):
        """Miniatura na lista"""
        if obj.imagem:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.imagem.url
            )
        return "Sem imagem"
    preview_thumbnail.short_description = "Preview"
    
    def preview_image(self, obj):
        """Preview maior na edição"""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: contain;" />',
                obj.imagem.url
            )
        return "Nenhuma imagem"
    preview_image.short_description = "Preview da Imagem"
    
    def dimensoes_info(self, obj):
        """Exibe dimensões formatadas"""
        return obj.dimensoes
    dimensoes_info.short_description = "Dimensões"
    
    def tamanho_info(self, obj):
        """Exibe tamanho formatado"""
        return obj.tamanho_formatado
    tamanho_info.short_description = "Tamanho"
    
    def get_queryset(self, request):
        """Otimiza consultas"""
        return super().get_queryset(request).select_related()
    
    actions = ['ativar_imagens', 'desativar_imagens']
    
    def ativar_imagens(self, request, queryset):
        """Ação para ativar múltiplas imagens"""
        updated = queryset.update(ativo=True)
        self.message_user(request, f"{updated} imagem(ns) ativada(s) com sucesso.")
    ativar_imagens.short_description = "Ativar imagens selecionadas"
    
    def desativar_imagens(self, request, queryset):
        """Ação para desativar múltiplas imagens"""
        updated = queryset.update(ativo=False)
        self.message_user(request, f"{updated} imagem(ns) desativada(s) com sucesso.")
    desativar_imagens.short_description = "Desativar imagens selecionadas"


# Admin customizado para diferentes tipos (opcional)
class HeroSliderAdmin(ImagemSiteAdmin):
    """Admin específico para Hero Slider"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(tipo='hero_slider')

class GaleriaAdmin(ImagemSiteAdmin):
    """Admin específico para Galeria"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(tipo='galeria')

# Registra admins específicos se necessário
# admin.site.register(ImagemSite, HeroSliderAdmin)