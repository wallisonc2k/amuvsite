# noticias/management/commands/preenche_slugs.py

from django.core.management.base import BaseCommand
from noticias.models import Noticia
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Preenche o campo slug para notícias que ainda não possuem.'

    def handle(self, *args, **options):
        noticias_sem_slug = Noticia.objects.filter(slug__isnull=True) | Noticia.objects.filter(slug__exact='')
        total = noticias_sem_slug.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS('Nenhuma notícia sem slug encontrada.'))
            return

        for noticia in noticias_sem_slug:
            slug_base = slugify(noticia.titulo)
            slug = slug_base
            num = 1

            # Garante unicidade (não repete slugs iguais)
            while Noticia.objects.filter(slug=slug).exclude(id=noticia.id).exists():
                slug = f"{slug_base}-{num}"
                num += 1

            noticia.slug = slug
            noticia.save()

        self.stdout.write(self.style.SUCCESS(f'Slugs preenchidos para {total} notícia(s).'))
