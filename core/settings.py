import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-sua-chave-real-2025'
DEBUG = True 
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin', # Deve vir antes do admin
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = 'contas.Usuario'

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
    'default': dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3")
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Belem'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# INTERFACE EXTRAORDINÁRIA JAZZMIN
JAZZMIN_SETTINGS = {
    "site_title": "GESTÃO POLÍTICA PRO",
    "site_header": "Comando Estratégico",
    "site_brand": "POLÍTICA PRO",
    "welcome_sign": "Painel de Inteligência Eleitoral",
    "copyright": "Gestão Política PA",
    "search_model": ["liderancas.Lideranca"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "campanhas.Candidato": "fas fa-crown",
        "liderancas.Lideranca": "fas fa-star",
        "municipios.Municipio": "fas fa-map-marker-alt",
        "liderancas.AtendimentoSocial": "fas fa-hand-holding-heart",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly", # Minimalista e profissional
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
}
