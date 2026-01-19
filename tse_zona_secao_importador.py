import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///banco.db")
engine = create_engine(DATABASE_URL)

def importar(csv):
    df = pd.read_csv(csv, sep=";", encoding="latin1")

    df = df[[
        "NM_MUNICIPIO",
        "NR_ZONA",
        "NR_SECAO",
        "QT_ELEITORES",
        "LATITUDE",
        "LONGITUDE"
    ]]

    df.columns = ["municipio", "zona", "secao", "eleitores", "lat", "lng"]

    df.to_sql("tse_zona_secao", engine, if_exists="replace", index=False)
    print("✔ Zona/Seção importadas")

if __name__ == "__main__":
    importar("zona_secao_tse.csv")
