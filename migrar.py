import sqlite3
import os

# Define o caminho do banco (Prioridade para o Render)
db_path = '/data/junior_araujo_sistemas.db' if os.path.exists('/data') else 'junior_araujo_sistemas.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Sincronizando estrutura do banco: {db_path}")

# --- 1. ATUALIZAR TABELA USUARIO ---
colunas_usuario = [
    ('meta_cadastros', 'INTEGER DEFAULT 0'),
    ('foto_perfil', "TEXT DEFAULT 'logo_default.png'"),
    ('fundo_login', "TEXT DEFAULT 'default_bg.jpg'")
]

for nome, tipo in colunas_usuario:
    try:
        cursor.execute(f"ALTER TABLE usuario ADD COLUMN {nome} {tipo}")
        print(f"Tabela Usuario: Coluna {nome} adicionada.")
    except:
        print(f"Tabela Usuario: Coluna {nome} já existe.")

# --- 2. ATUALIZAR TABELA ELEITOR ---
colunas_eleitor = [
    ('titulo_eleitoral', 'TEXT'),
    ('zona', 'TEXT'),
    ('secao', 'TEXT')
]

for nome, tipo in colunas_eleitor:
    try:
        cursor.execute(f"ALTER TABLE eleitor ADD COLUMN {nome} {tipo}")
        print(f"Tabela Eleitor: Coluna {nome} adicionada.")
    except:
        print(f"Tabela Eleitor: Coluna {nome} já existe.")

# --- 3. CRIAR TABELA ACAO_SOCIAL (Antiga acao_saude) ---
# Criamos com o nome exato que o seu app.py atual pede: acao_social
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
print("Tabela acao_social verificada.")

conn.commit()
conn.close()
print("BANCO ATUALIZADO COM SUCESSO! DADOS ANTIGOS PRESERVADOS.")
