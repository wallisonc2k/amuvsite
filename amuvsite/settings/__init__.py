import os
from dotenv import load_dotenv
load_dotenv()

env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
else:
    from .development import *
