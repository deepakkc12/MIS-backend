from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = 'django-insecure-((izk5-j7+i*@y@tj81mq3qfk9pmmn4zvf_16a=^c7uk-9c_w$'

DEBUG = False  # Set default to False, override in development.py

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.29.89',
    '192.168.1.107',
    '192.168.1.105',
    '103.12.1.191',
    '192.168.1.2',
    '192.168.1.8',
    '192.168.1.106',
    '192.168.1.104',
    '192.168.1.103',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://192.168.29.89:3000",
    "http://192.168.1.107:3000",
    "http://192.168.1.105:3000",
    "http://103.12.1.191:3100",
    "http://103.12.1.191:3200",
    "http://192.168.1.2:3000",
    'http://192.168.1.8:3001',
    'http://192.168.1.8:3002',
    'http://192.168.1.106:3000',
    'http://192.168.1.7:3000',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Disabled in your config
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'api.middlewares.Logging.RequestLoggingMiddleware', 
    'api.middlewares.error_handler.ErrorHandlingMiddleware',
    'api.middlewares.auth.AuthenticationMiddleware',
]

AUTH_EXCLUDED_PATHS = [
    '/api/login/',
    '/api/register/',
    '/api/forgot-password/',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

ROOT_URLCONF = 'config.urls'  # changed to config.urls from Server.urls

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/resources/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'resources')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
