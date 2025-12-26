import os
from pathlib import Path

# ... (mantenha suas configurações de banco de dados e SECRET_KEY)

INSTALLED_APPS = [
    'jazzmin',  # DEVE ser o primeiro
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

# Configuração de Luxo do Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Gestão Política PA",
    "site_header": "Gestão Política",
    "site_brand": "COMANDO ESTRATÉGICO",
    "welcome_sign": "Painel de Controle de Inteligência Política",
    "copyright": "Gestão Política PA 2025",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Início", "url": "admin:index"},
        {"name": "Suporte", "url": "https://wa.me/seu-numero", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "contas.Usuario": "fas fa-user-tie",
        "liderancas.Lideranca": "fas fa-bullhorn",
        "municipios.Municipio": "fas fa-map-marked-alt",
    },
    "order_with_respect_to": ["liderancas", "municipios", "contas"],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",  # Tema minimalista e profissional
    "dark_mode_theme": "darkly",
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
}

AUTH_USER_MODEL = 'contas.Usuario'
