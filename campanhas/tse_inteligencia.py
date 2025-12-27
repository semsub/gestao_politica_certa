import os
import django
import pandas as pd # Necessário instalar: pip install pandas

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from campanhas.models import Municipio

def importar_historico_tse(caminho_csv):
    """
    Importa dados de votação por seção para identificar 'vácuos' de votos.
    """
    df = pd.read_csv(caminho_csv, sep=';', encoding='latin-1')
    
    # Filtra apenas votos do seu partido/candidato na última eleição
    resumo = df.groupby(['MUNICIPIO', 'ZONA', 'SECAO']).agg({'VOTOS': 'sum'}).reset_index()
    
    for index, row in resumo.iterrows():
        # Lógica para marcar no mapa onde a campanha deve ser intensificada
        print(f"Analisando {row['MUNICIPIO']} - Zona {row['ZONA']}: {row['VOTOS']} votos históricos.")

# Exemplo: importar_historico_tse('votacao_secao_2022_PA.csv')
