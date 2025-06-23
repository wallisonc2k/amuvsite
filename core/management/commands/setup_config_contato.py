from django.core.management.base import BaseCommand
from core.models import SiteConfigContato

class Command(BaseCommand):
    help = 'Configura dados iniciais do site'

    def handle(self, *args, **options):
        if not SiteConfigContato.objects.exists():
            SiteConfigContato.objects.create(
                site_titulo='AMUV',
                contato_email='amuv.2025@gmail.com',
                suporte_email='contato@amuvtv.com.br', 
                telefone_contato='(87) 981016448',
                whatsapp_numero='(87) 981016448',
                chave_pix='amuv.2025@gmail.com'
            )
            self.stdout.write(self.style.SUCCESS('✅ Configuração criada!'))
        else:
            config = SiteConfigContato.objects.first()
            self.stdout.write(f'⚠️  Configuração já existe: {config.site_titulo}')
