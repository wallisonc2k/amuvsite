# core/utils.py
import os
from django.conf import settings
from django.templatetags.static import static

def listar_imagens_estaticas(subpasta, extensoes_permitidas=None, ordenar=True):
    """
    Retorna uma lista de URLs para imagens dentro da pasta estática especificada.
    
    Args:
        subpasta (str): Caminho relativo dentro da pasta static (ex: 'img/banners').
        extensoes_permitidas (list): Lista de extensões válidas. Ex: ['.jpg', '.png']
        ordenar (bool): Se deve ordenar alfabeticamente os arquivos.
        
    Returns:
        list: Lista de URLs para os arquivos encontrados.
    """
    if extensoes_permitidas is None:
        extensoes_permitidas = ['.jpg', '.jpeg', '.png', '.webp']

    caminho_absoluto = os.path.join(settings.BASE_DIR, 'static', subpasta)
    caminho_url = f'/static/{subpasta}/'

    imagens = []
    if os.path.exists(caminho_absoluto):
        arquivos = os.listdir(caminho_absoluto)
        if ordenar:
            arquivos.sort()
        for nome in arquivos:
            if any(nome.lower().endswith(ext) for ext in extensoes_permitidas):
                imagens.append(os.path.join(caminho_url, nome))
    
    return imagens


def listar_imagens_com_descricao(subpasta='img/galeria'):
    caminho_absoluto = os.path.join('static', subpasta)
    try:
        arquivos = os.listdir(caminho_absoluto)
    except FileNotFoundError:
        return []

    imagens = []
    for nome_arquivo in arquivos:
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            descricao = gerar_descricao_legivel(nome_arquivo)
            imagens.append({
                'url': static(f'{subpasta}/{nome_arquivo}'),
                'descricao': descricao
            })

    return imagens

def gerar_descricao_legivel(nome_arquivo):
    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
    nome_legivel = nome_sem_extensao.replace('_', ' ').replace('-', ' ')
    return nome_legivel.capitalize()
