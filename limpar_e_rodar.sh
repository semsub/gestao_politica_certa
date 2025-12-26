#!/bin/bash
echo "Limpando processos antigos..."
fuser -k 8000/tcp
echo "Iniciando Servidor de Comando..."
python manage.py runserver 0.0.0.0:8000 &
sleep 3
echo "Iniciando Aplicativo de Campo..."
python main.py
