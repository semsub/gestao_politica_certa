import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-sua-chave-real-de-producao-2025'
DEBUG = False # Produção
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
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
]

ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = 'contas.Usuario'

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

# INTERFACE DE LUXO JAZZMIN
JAZZMIN_SETTINGS = {
    "site_title": "SISTEMA POLÍTICO PRO",
    "site_header": "Gestão Estratégica",
    "site_brand": "INTELIGÊNCIA ELEITORAL",
    "welcome_sign": "Painel de Controle de Campanha",
    "copyright": "Gestão Política 2025",
    "search_model": ["liderancas.Lideranca"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["campanhas", "liderancas", "municipios"],
    "icons": {
        "campanhas.Candidato": "fas fa-crown",
        "liderancas.Lideranca": "fas fa-user-tie",
        "municipios.Municipio": "fas fa-city",
        "liderancas.AtendimentoSocial": "fas fa-hand-holding-heart",
    },
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
}
