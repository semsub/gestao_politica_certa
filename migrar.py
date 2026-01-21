import sqlite3
import os

# Define o caminho do banco (Render ou Local)
if os.path.exists('/data'):
    db_path = '/data/junior_araujo_sistemas.db'
else:
    db_path = 'junior_araujo_sistemas.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Iniciando atualização do banco em: {db_path}")

# 1. Adicionar novas colunas na tabela Eleitor (se não existirem)
colunas_novas = [
    ('titulo_eleitoral', 'TEXT'),
    ('zona', 'TEXT'),
    ('secao', 'TEXT')
]

for nome, tipo in colunas_novas:
    try:
        cursor.execute(f"ALTER TABLE eleitor ADD COLUMN {nome} {tipo}")
        print(f"Coluna {nome} adicionada com sucesso.")
    except sqlite3.OperationalError:
        print(f"Coluna {nome} já existe, pulando...")

# 2. Criar tabela AcaoSocial (se não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS acao_social (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eleitor_id INTEGER NOT NULL,
    tipo TEXT,
    servico TEXT,
    descricao TEXT,
    status TEXT DEFAULT 'Aguardando',
    documento TEXT,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (eleitor_id) REFERENCES eleitor (id)
)
''')
print("Tabela acao_social verificada/criada.")

conn.commit()
conn.close()
print("Sincronização concluída! Seus dados antigos estão salvos.")
