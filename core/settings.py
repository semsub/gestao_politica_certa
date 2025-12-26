import os
import dj_database_url

# Segurança
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-padrao-muito-segura')
DEBUG = False
ALLOWED_HOSTS = ['*'] # Depois coloque o seu domínio do Render

# Configuração de Base de Dados para o Render (PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Ficheiros Estáticos (Essencial para o Dashboard de Mapas)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Adicione o WhiteNoise no topo dos Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # DEVE SER O SEGUNDO
    'corsheaders.middleware.CorsMiddleware',
    # ... os restantes ...
]
