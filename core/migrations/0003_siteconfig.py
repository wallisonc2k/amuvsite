# Generated by Django 5.2 on 2025-04-30 00:30

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contato_telefone'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cor_primaria', colorfield.fields.ColorField(default='#B91C1C', image_field=None, max_length=25, samples=None, verbose_name='Cor primária')),
                ('cor_primaria_hover', colorfield.fields.ColorField(default='#991B1B', image_field=None, max_length=25, samples=None, verbose_name='Cor primária (hover)')),
                ('cor_secundaria', colorfield.fields.ColorField(default='#1F2937', image_field=None, max_length=25, samples=None, verbose_name='Cor secundária')),
                ('cor_texto', colorfield.fields.ColorField(default='#1F2937', image_field=None, max_length=25, samples=None, verbose_name='Cor de texto principal')),
                ('cor_texto_claro', colorfield.fields.ColorField(default='#6B7280', image_field=None, max_length=25, samples=None, verbose_name='Cor de texto secundário')),
                ('cor_fundo_hero', colorfield.fields.ColorField(default='#B91C1C', image_field=None, max_length=25, samples=None, verbose_name='Cor de fundo do Hero')),
                ('cor_fundo_secoes', colorfield.fields.ColorField(default='#F3F4F6', image_field=None, max_length=25, samples=None, verbose_name='Cor de fundo das seções')),
                ('cor_fundo_cards', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None, verbose_name='Cor de fundo dos cards')),
                ('cor_fundo_footer', colorfield.fields.ColorField(default='#1F2937', image_field=None, max_length=25, samples=None, verbose_name='Cor de fundo do rodapé')),
                ('cor_divisor', colorfield.fields.ColorField(default='#B91C1C', image_field=None, max_length=25, samples=None, verbose_name='Cor dos divisores')),
                ('cor_borda_cards', colorfield.fields.ColorField(default='#B91C1C', image_field=None, max_length=25, samples=None, verbose_name='Cor da borda dos cards')),
                ('ativo', models.BooleanField(default=True, verbose_name='Configuração ativa')),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Última atualização')),
            ],
            options={
                'verbose_name': 'Configuração de Tema',
                'verbose_name_plural': 'Configurações de Tema',
            },
        ),
    ]
