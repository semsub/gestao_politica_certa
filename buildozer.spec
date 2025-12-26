[app]
# (str) Título do seu aplicativo
title = Gestao Politica PA

# (str) Nome do pacote (identificador único)
package.name = gestao_politica_certa

# (str) Domínio do pacote
package.domain = com.junioraraujo

# (str) Caminho para os arquivos fonte
source.dir = .

# (list) Extensões de arquivos a serem incluídas
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Versão do App
version = 1.0.0

# (list) Requisitos do App (Bibliotecas que ele usa)
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,urllib3,certifi,idna,charset-normalizer,plyer

# (str) Ícone do App (Coloque um arquivo icon.png na pasta se tiver)
# icon.filename = %(source.dir)s/icon.png

# (str) Orientação da tela
orientation = portrait

# (list) Permissões do Android (VITAL PARA GPS E INTERNET)
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, WRITE_EXTERNAL_STORAGE

# (int) API mínima do Android (Compatibilidade)
android.minapi = 21

# (int) API alvo do Android (Requisito da Play Store)
android.sdk = 33

# (str) Nome da atividade principal
android.entrypoint = org.kivy.android.PythonActivity

# (bool) Se o app deve rodar em tela cheia
fullscreen = 0

# (list) Arquivos de suporte (Service para rodar em background se necessário)
# services = Sincronizador:service.py

[buildozer]
# (int) Nível de log (2 para ver erros durante a compilação)
log_level = 2

# (str) Caminho para os binários gerados
bin_dir = ./bin
