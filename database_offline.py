import sqlite3
import requests

class OfflineManager:
    def __init__(self):
        self.conn = sqlite3.connect('base_local.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS votos_offline 
            (id INTEGER PRIMARY KEY, nome TEXT, votos INTEGER, demanda TEXT, lat REAL, lon REAL)''')
        self.conn.commit()

    def salvar_voto(self, nome, votos, demanda, lat, lon):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO votos_offline (nome, votos, demanda, lat, lon) VALUES (?,?,?,?,?)",
                       (nome, votos, demanda, lat, lon))
        self.conn.commit()

    def sincronizar(self, api_url):
        cursor = self.conn.cursor()
        pendentes = cursor.execute("SELECT * FROM votos_offline").fetchall()
        for p in pendentes:
            try:
                res = requests.post(api_url, json={"nome": p[1], "votos": p[2], "demanda": p[3]})
                if res.status_code == 201:
                    cursor.execute("DELETE FROM votos_offline WHERE id=?", (p[0],))
            except:
                return "Servidor indisponível. Dados seguros no celular."
        self.conn.commit()
        return "Sincronização concluída!"
