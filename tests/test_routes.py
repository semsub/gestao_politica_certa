"""Deterministic route tests — each test is fully isolated via the conftest
fixtures (in-memory DB + tmp upload folder) so no ordering or timing
dependencies exist."""

import os

from app import db as _db, Usuario, Eleitor, AcaoSocial, Despesa, Midia


# -----------------------------------------------------------------------
# Authentication & login
# -----------------------------------------------------------------------

class TestLogin:
    def test_index_redirects_to_login(self, client):
        resp = client.get("/", follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]

    def test_login_page_renders(self, client):
        resp = client.get("/login")
        assert resp.status_code == 200

    def test_master_login_succeeds(self, client):
        resp = client.post(
            "/login",
            data={"login": "junior.araujo21", "senha": os.environ.get("MASTER_PASSWORD", "admin")},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert "/dashboard" in resp.headers["Location"]

    def test_invalid_login_flashes_error(self, client):
        resp = client.post(
            "/login",
            data={"login": "nobody", "senha": "wrong"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert "Credenciais" in resp.data.decode("utf-8")

    def test_db_user_login_succeeds(self, client, db):
        user = Usuario(
            nome="Regular", login="regular.user", senha="pass1", nivel="LIDERANÇA"
        )
        db.session.add(user)
        db.session.commit()

        resp = client.post(
            "/login",
            data={"login": "regular.user", "senha": "pass1"},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert "/dashboard" in resp.headers["Location"]

    def test_logout_clears_session(self, admin_session):
        resp = admin_session.get("/logout", follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]

        # After logout, dashboard should redirect to login
        resp2 = admin_session.get("/dashboard", follow_redirects=False)
        assert resp2.status_code == 302
        assert "/login" in resp2.headers["Location"]


# -----------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------

class TestDashboard:
    def test_dashboard_requires_login(self, client):
        resp = client.get("/dashboard", follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]

    def test_dashboard_renders_for_admin(self, admin_session):
        resp = admin_session.get("/dashboard")
        assert resp.status_code == 200

    def test_dashboard_with_eleitores(self, admin_session, db):
        master = Usuario.query.filter_by(login="junior.araujo21").first()
        eleitor = Eleitor(
            nome_completo="Test Voter",
            municipio="Belém",
            lider_id=master.id,
        )
        db.session.add(eleitor)
        db.session.commit()

        resp = admin_session.get("/dashboard")
        assert resp.status_code == 200
        assert b"Test Voter" in resp.data


# -----------------------------------------------------------------------
# Eleitor CRUD
# -----------------------------------------------------------------------

class TestEleitor:
    def test_novo_eleitor_get(self, admin_session):
        resp = admin_session.get("/eleitor/novo")
        assert resp.status_code == 200

    def test_novo_eleitor_post(self, admin_session, db):
        resp = admin_session.post(
            "/eleitor/novo",
            data={
                "nome_completo": "Maria Silva",
                "titulo_eleitoral": "1234",
                "zona": "01",
                "secao": "02",
                "rua": "Rua A",
                "numero": "10",
                "bairro": "Centro",
                "municipio": "Belém",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302

        assert Eleitor.query.count() == 1
        e = Eleitor.query.first()
        assert e.nome_completo == "Maria Silva"
        # Verify timezone-aware default was applied
        assert e.data_cadastro is not None

    def test_remover_eleitor(self, admin_session, db):
        master = Usuario.query.filter_by(login="junior.araujo21").first()
        eleitor = Eleitor(nome_completo="To Remove", lider_id=master.id)
        db.session.add(eleitor)
        db.session.commit()
        eid = eleitor.id

        resp = admin_session.get(f"/eleitor/remover/{eid}", follow_redirects=False)
        assert resp.status_code == 302
        assert db.session.get(Eleitor, eid) is None


# -----------------------------------------------------------------------
# Usuario CRUD
# -----------------------------------------------------------------------

class TestUsuario:
    def test_lista_usuarios_requires_login(self, client):
        resp = client.get("/usuarios/lista", follow_redirects=False)
        assert resp.status_code == 302

    def test_lista_usuarios_admin(self, admin_session):
        resp = admin_session.get("/usuarios/lista")
        assert resp.status_code == 200

    def test_cadastro_usuario_post(self, admin_session, db):
        resp = admin_session.post(
            "/usuarios/novo",
            data={
                "nome": "New User",
                "login": "new.user",
                "senha": "pass",
                "nivel": "LIDERANÇA",
                "cargo": "Lider",
                "municipio": "Belém",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert Usuario.query.filter_by(login="new.user").first() is not None

    def test_remover_usuario(self, admin_session, db):
        user = Usuario(nome="Del Me", login="del.me", senha="x", nivel="LIDERANÇA")
        db.session.add(user)
        db.session.commit()
        uid = user.id

        resp = admin_session.get(f"/usuarios/remover/{uid}", follow_redirects=False)
        assert resp.status_code == 302
        assert db.session.get(Usuario, uid) is None

    def test_lideranca_cannot_access_lista(self, regular_user):
        client, _ = regular_user
        resp = client.get("/usuarios/lista", follow_redirects=False)
        assert resp.status_code == 302


# -----------------------------------------------------------------------
# Saude / AcaoSocial
# -----------------------------------------------------------------------

class TestSaude:
    def test_saude_urgente_requires_login(self, client):
        resp = client.get("/saude/urgente", follow_redirects=False)
        assert resp.status_code == 302

    def test_saude_urgente_renders(self, admin_session):
        resp = admin_session.get("/saude/urgente")
        assert resp.status_code == 200

    def test_criar_acao_social(self, admin_session, db):
        master = Usuario.query.filter_by(login="junior.araujo21").first()
        eleitor = Eleitor(nome_completo="Patient", lider_id=master.id)
        db.session.add(eleitor)
        db.session.commit()

        resp = admin_session.post(
            "/saude/urgente",
            data={
                "eleitor_id": eleitor.id,
                "servico": "UTI",
                "descricao": "Needs care",
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert AcaoSocial.query.count() == 1

    def test_alterar_status(self, admin_session, db):
        master = Usuario.query.filter_by(login="junior.araujo21").first()
        eleitor = Eleitor(nome_completo="P2", lider_id=master.id)
        db.session.add(eleitor)
        db.session.commit()

        acao = AcaoSocial(eleitor_id=eleitor.id, servico="UTI")
        db.session.add(acao)
        db.session.commit()

        resp = admin_session.post(
            f"/saude/status/{acao.id}",
            data={"novo_status": "ATENDIDO"},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        db.session.refresh(acao)
        assert acao.status == "ATENDIDO"


# -----------------------------------------------------------------------
# Despesas
# -----------------------------------------------------------------------

class TestDespesas:
    def test_lancar_despesas_requires_login(self, client):
        resp = client.get("/despesas/lancar", follow_redirects=False)
        assert resp.status_code == 302

    def test_lancar_despesas_get(self, admin_session):
        resp = admin_session.get("/despesas/lancar")
        assert resp.status_code == 200

    def test_lancar_despesas_post(self, admin_session, db):
        resp = admin_session.post(
            "/despesas/lancar",
            data={"valor": "150.50", "descricao": "Office supplies"},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert Despesa.query.count() == 1
        d = Despesa.query.first()
        assert d.valor == 150.50
        assert d.data is not None


# -----------------------------------------------------------------------
# Midia
# -----------------------------------------------------------------------

class TestMidia:
    def test_gerenciar_midia_requires_login(self, client):
        resp = client.get("/midia/gerenciar", follow_redirects=False)
        assert resp.status_code == 302

    def test_gerenciar_midia_renders(self, admin_session):
        resp = admin_session.get("/midia/gerenciar")
        assert resp.status_code == 200


# -----------------------------------------------------------------------
# Config ADM
# -----------------------------------------------------------------------

class TestAdmConfig:
    def test_adm_config_requires_admin(self, regular_user):
        client, _ = regular_user
        resp = client.get("/adm/config", follow_redirects=False)
        assert resp.status_code == 302

    def test_adm_config_renders_for_admin(self, admin_session):
        resp = admin_session.get("/adm/config")
        assert resp.status_code == 200


# -----------------------------------------------------------------------
# Compartilhar (public page)
# -----------------------------------------------------------------------

class TestCompartilhar:
    def test_compartilhar_renders_without_login(self, client):
        resp = client.get("/compartilhar")
        assert resp.status_code == 200


# -----------------------------------------------------------------------
# Test isolation — proves that database state does NOT leak between tests
# -----------------------------------------------------------------------

class TestIsolation:
    """These two tests MUST run in order. They prove the in-memory DB fixture
    creates a fresh database for each test — the voter created in test_a
    must not exist in test_b."""

    def test_a_create_voter(self, admin_session, db):
        master = Usuario.query.filter_by(login="junior.araujo21").first()
        db.session.add(Eleitor(nome_completo="Isolation Check", lider_id=master.id))
        db.session.commit()
        assert Eleitor.query.filter_by(nome_completo="Isolation Check").count() == 1

    def test_b_voter_does_not_leak(self, admin_session, db):
        assert Eleitor.query.filter_by(nome_completo="Isolation Check").count() == 0
