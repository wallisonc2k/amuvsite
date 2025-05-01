from django.contrib import admin
from .models import SiteConfig

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