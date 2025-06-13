from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configurações de e-mail (console para testes locais)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
