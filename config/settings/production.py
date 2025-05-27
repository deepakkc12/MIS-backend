from .base import *
from ..logCof.logging import LOGGING  # Import the LOGGING configuration

DEBUG = False

ALLOWED_HOSTS = [
    '103.12.1.191','localhost', '127.0.0.1' 
]

# You should tighten CORS in production:
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://103.12.1.191:3100",
]

# Example of database config override for production
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': os.getenv('DB_NAME'),
#     'USER': os.getenv('DB_USER'),
#     'PASSWORD': os.getenv('DB_PASSWORD'),
#     'HOST': os.getenv('DB_HOST'),
#     'PORT': os.getenv('DB_PORT'),
# }

# Security settings for production (optional)

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
