# ia_randomforest_tse.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

MODEL_FILE = "modelo_randomforest.pkl"

def treinar_modelo(df):
    if df.empty: return None
    X = df[['idade','zona','secao']].values
    y = df['voto'].values
    clf = RandomForestClassifier(n_estimators=100,random_state=42)
    clf.fit(X,y)
    joblib.dump(clf,MODEL_FILE)
    return clf

def carregar_modelo():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    return None

def prever_votos(lista_cadastros):
    previsoes=[]
    for c in lista_cadastros:
        previsoes.append({
            "nome":c["nome"],
            "titulo":c.get("titulo",""),
            "voto_previsto":"N/A"
        })
    return previsoes
