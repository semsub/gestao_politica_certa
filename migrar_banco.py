# migrar_banco.py
from app import app, db
from sqlalchemy import text

def atualizar_sistema_junior_araujo():
    with app.app_context():
        print("🚀 Iniciando atualização do banco JÚNIOR ARAÚJO SISTEMAS...")
        
        # Lista de novas colunas necessárias para o mapeamento eleitoral e hierarquia
        comandos = [
            # Tabela Eleitores
            "ALTER TABLE eleitor ADD COLUMN tipo_registro TEXT DEFAULT 'PESSOA'",
            "ALTER TABLE eleitor ADD COLUMN titulo_eleitoral TEXT",
            "ALTER TABLE eleitor ADD COLUMN zona TEXT",
            "ALTER TABLE eleitor ADD COLUMN secao TEXT",
            
            # Tabela Usuarios (Hierarquia)
            "ALTER TABLE usuario ADD COLUMN cargo TEXT",
            "ALTER TABLE usuario ADD COLUMN criado_por INTEGER"
        ]
        
        for cmd in comandos:
            try:
                db.session.execute(text(cmd))
                db.session.commit()
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                # Se a coluna já existir, ele apenas ignora e pula para a próxima
                db.session.rollback()
                print(f"ℹ️ Pulado (já existe ou erro): {cmd}")

        # Criar a nova tabela de Ações de Saúde se não existir
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS acoes_sociais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    eleitor_id INTEGER NOT NULL,
                    tipo_acao TEXT NOT NULL,
                    detalhe_acao TEXT,
                    status TEXT DEFAULT 'PENDENTE',
                    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (eleitor_id) REFERENCES eleitor(id)
                )
            """))
            db.session.commit()
            print("✅ Tabela de Ações Sociais/Saúde verificada/criada!")
        except Exception as e:
            print(f"❌ Erro ao criar tabela de ações: {e}")

        print("\n🔥 Sistema atualizado com sucesso sem perda de dados!")

if __name__ == "__main__":
    atualizar_sistema_junior_araujo()
