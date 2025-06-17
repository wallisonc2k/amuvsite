from .base import *
import dj_database_url
import dj_email_url
from decouple import config

DEBUG = False

# === Banco de dados ===
DATABASE_URL = config("DATABASE_URL", default=None)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definida no ambiente.")

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
}

# === E-mail ===
EMAIL_URL = config("EMAIL_URL", default=None)
if not EMAIL_URL:
    raise ValueError("EMAIL_URL não está definida no ambiente.")

EMAIL_CONFIG = dj_email_url.config(env="EMAIL_URL")
vars().update(EMAIL_CONFIG)

# Fallback opcional se você quiser garantir que DEFAULT_FROM_EMAIL seja o mesmo que USER
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)
