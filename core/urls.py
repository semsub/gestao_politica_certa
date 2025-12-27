from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Painel Administrativo do Dono do Sistema (Você)
    path('admin/', admin.site.urls),

    # 2. Rotas do App de Campanhas (Onde está a lógica de Vereador a Presidente)
    # Certifique-se de que o seu app se chama 'campanhas'
    path('api/v1/', include('campanhas.urls')), 

]

# 3. CONFIGURAÇÃO PARA AMBIENTE DE DESENVOLVIMENTO E PRODUÇÃO (RENDER)
# Esta lógica permite que o Django sirva as fotos dos recibos e documentos
# que as lideranças enviarem pelo celular.
if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalização do Painel Administrativo para sua marca
admin.site.site_header = "Gestão Política Certa - Júnior Araújo"
admin.site.site_title = "Painel de Controle - Base Salinas"
admin.site.index_title = "Bem-vindo ao Comando Estratégico do Pará"
