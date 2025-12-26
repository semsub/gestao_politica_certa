import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-chave-viva-pa-2025')
DEBUG = False # Mantenha False para produção no Render
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',  # Essencial ser o primeiro para o visual
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contas',
    'liderancas',
    'municipios',
    'campanhas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Serve o CSS no celular/Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    )
}

AUTH_USER_MODEL = 'contas.Usuario'

# Idioma e Hora local do Pará
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Belem'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- CONFIGURAÇÃO JAZZMIN (INTERFACE DE APLICATIVO) ---
JAZZMIN_SETTINGS = {
    "site_title": "Gestão Política PA",
    "site_header": "Comando PA",
    "site_brand": "GESTOR PRO",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Painel Estratégico Pará",
    "copyright": "Gestão Política 2025",
    "search_model": ["liderancas.Lideranca"],
    "show_sidebar": True,
    "navigation_expanded": False, # Melhora visual no celular
    "icons": {
        "auth": "fas fa-users-cog",
        "contas.Usuario": "fas fa-user-shield",
        "liderancas.Lideranca": "fas fa-user-tie",
        "liderancas.AtendimentoSocial": "fas fa-hand-holding-heart",
        "municipios.Municipio": "fas fa-map-marked-alt",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lumen", # Tema limpo, branco e profissional
    "dark_mode_theme": None,
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
