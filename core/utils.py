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


def listar_imagens_com_descricao(subpasta='shared/img/galeria', resolucoes=('640px', '1024px', 'original')):
    base_path = os.path.join('static', subpasta)
    try:
        arquivos = os.listdir(os.path.join(base_path, resolucoes[-1]))  # usa a pasta 'original' como base
    except FileNotFoundError:
        return []

    imagens = []
    for nome_arquivo in arquivos:
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            descricao = gerar_descricao_legivel(nome_arquivo)
            fontes = {}
            for res in resolucoes:
                caminho_arquivo = f'{subpasta}/{res}/{nome_arquivo}'
                fontes[res] = static(caminho_arquivo)

            imagens.append({
                'descricao': descricao,
                'fontes': fontes  # dict com cada resolução
            })

    return imagens


def gerar_descricao_legivel(nome_arquivo):
    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
    nome_legivel = nome_sem_extensao.replace('_', ' ').replace('-', ' ')
    return nome_legivel.capitalize()
