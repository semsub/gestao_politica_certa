# update_final.py
from app import app, db
from sqlalchemy import text

def consolidar_sistema_junior():
    with app.app_context():
        # Lista definitiva de colunas para suportar TODO o seu projeto
        comandos = [
            # Para a tabela de ELEITORES (Pessoa/Família)
            "ALTER TABLE eleitor ADD COLUMN tipo_registro TEXT DEFAULT 'PESSOA'",
            "ALTER TABLE eleitor ADD COLUMN titulo_eleitoral TEXT",
            "ALTER TABLE eleitor ADD COLUMN zona TEXT",
            "ALTER TABLE eleitor ADD COLUMN secao TEXT",
            
            # Para a tabela de USUÁRIOS (Hierarquia e Senhas)
            "ALTER TABLE usuario ADD COLUMN cargo TEXT",
            "ALTER TABLE usuario ADD COLUMN criado_por INTEGER",
            "ALTER TABLE usuario ADD COLUMN senha_plana TEXT" # Para você ver a senha na lista de usuários
        ]
        
        for cmd in comandos:
            try:
                db.session.execute(text(cmd))
                db.session.commit()
            except:
                db.session.rollback()

        # Tabela de AÇÕES (ADM registra: Saúde, Natal, Cidadã)
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS acoes_sociais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eleitor_id INTEGER NOT NULL,
                tipo_acao TEXT NOT NULL, -- SAÚDE, NATAL SOLIDÁRIO, CIDADÃ
                detalhe_acao TEXT,       -- Exames, Cirurgias, UTI, Óculos, etc.
                data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (eleitor_id) REFERENCES eleitor(id)
            )
        """))
        db.session.commit()
        print("✅ ESTRUTURA FINALIZADA E CONSOLIDADA!")

if __name__ == "__main__":
    consolidar_sistema_junior()
