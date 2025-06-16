# amuvsite/settings/__init__.py

import os

# Define o ambiente padrão como 'production' se não for especificado.
# Isso garante que o Docker sempre rode com as configurações de produção.
env = os.getenv('DJANGO_ENV', 'production')

# O python-dotenv só é necessário e carregado para desenvolvimento local.
# No build do Docker ou em produção, as variáveis virão diretamente do ambiente.
if env == 'development':
    from dotenv import load_dotenv
    load_dotenv()
    from .development import *
else: # 'production'
    from .production import *
