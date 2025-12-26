import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURANÇA: Mantenha sua chave ou use variável de ambiente
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sua-chave-aqui')

DEBUG = True # Mude para False em produção

ALLOWED_HOSTS = ['*']

# --- APPS CONFIGURATION ---
INSTALLED_APPS = [
    'jazzmin',  # Visual Profissional (Deve ser o 1º)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Seus Apps
    'contas',
    'liderancas',
    'municipios',
    'campanhas',
]

# --- MIDDLEWARES (CORRIGE OS ERROS E408, E409, E410) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Para arquivos estáticos no Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# --- TEMPLATES (CORRIGE O ERRO E403) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

# --- DATABASE CONFIG ---
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    )
}

# --- AUTHENTICATION ---
AUTH_USER_MODEL = 'contas.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Belem'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- JAZZMIN SETTINGS (LUXO E MINIMALISMO) ---
JAZZMIN_SETTINGS = {
    "site_title": "Gestão Política PA",
    "site_header": "Comando Estratégico",
    "site_brand": "INTELIGÊNCIA POLÍTICA",
    "welcome_sign": "Painel de Gestão de Alta Performance",
    "copyright": "Gestão Política PA 2025",
    "icons": {
        "auth": "fas fa-users-cog",
        "contas.Usuario": "fas fa-user-shield",
        "liderancas.Lideranca": "fas fa-users",
        "municipios.Municipio": "fas fa-city",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar_fixed": True,
    "sidebar_fixed": True,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
