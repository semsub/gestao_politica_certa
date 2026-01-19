import pandas as pd
import os, json

DB_FILE = "banco_dados.json"

def carregar_db():
    if not os.path.exists(DB_FILE):
        return {"candidatos": [], "eleitores": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_db(d):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=4, ensure_ascii=False)

def importar_candidatos(csv_file):
    d = carregar_db()
    df = pd.read_csv(csv_file, sep=';', encoding='latin1')
    for _, row in df.iterrows():
        d["candidatos"].append({
            "id": row["SQ_CANDIDATO"],
            "nome": row["NM_URNA_CANDIDATO"],
            "cargo": row["DS_CARGO"],
            "estado": row["SG_UF"],
            "municipio": row["NM_MUNICIPIO"]
        })
    salvar_db(d)

def importar_eleitores(csv_file):
    d = carregar_db()
    df = pd.read_csv(csv_file, sep=';', encoding='latin1')
    for _, row in df.iterrows():
        d["eleitores"].append({
            "id": row["ID_ELEITOR"],
            "nome": row["NM_ELEITOR"],
            "titulo": row["NR_TITULO_ELEITOR"],
            "zona": row["NR_ZONA"],
            "secao": row["NR_SECAO"],
            "municipio": row["NM_MUNICIPIO"],
            "estado": row["SG_UF"]
        })
    salvar_db(d)
