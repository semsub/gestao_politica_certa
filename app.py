import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "230808Deus#"

# --- CONFIGURAÇÕES PARA PERSISTÊNCIA NO RENDER ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('/data'):
    # Configuração para Produção (Render com Disco Persistente)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/junior_araujo_sistemas.db'
    app.config['UPLOAD_FOLDER'] = '/data/static/uploads'
else:
    # Configuração para Desenvolvimento Local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'junior_araujo_sistemas.db')
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Garante que a pasta de uploads exista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# --- MODELOS (BANCO DE DADOS) ---

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.String(20)) # ADM, CANDIDATO, COORDENADOR, LIDERANÇA
    cargo = db.Column(db.String(50))
    municipio = db.Column(db.String(100))
    pai_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    foto_perfil = db.Column(db.String(200), default='logo_default.png')
    fundo_login = db.Column(db.String(200), default='default_bg.jpg')

class Eleitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    titulo_eleitoral = db.Column(db.String(20))
    zona = db.Column(db.String(10))
    secao = db.Column(db.String(10))
    rua = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    bairro = db.Column(db.String(100))
    municipio = db.Column(db.String(100))
    lider_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class AcaoSocial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleitor_id = db.Column(db.Integer, db.ForeignKey('eleitor.id'))
    tipo = db.Column(db.String(50)) # Saúde, Social, etc.
    servico = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    status = db.Column(db.String(50), default='AGUARDANDO ATENDIMENTO')
    documento = db.Column(db.String(200))
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    lancado_por = db.Column(db.Integer)
    data = db.Column(db.DateTime, default=datetime.utcnow)

class Midia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    arquivo = db.Column(db.String(200))
    criado_por = db.Column(db.Integer)

# --- LISTAS OFICIAIS ---

MUNICIPIOS_PA = [
    "Abaetetuba", "Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", "Altamira",
    "Anajás", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", "Baião",
    "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito",
    "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru",
    "Cachoeira do Arari", "Cachoeira do Piriá", "Cametá", "Canaã dos Carajás", "Capanema", "Capitão Poço",
    "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", "Cumaru do Norte",
    "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu", "Eldorado do Carajás", "Faro", "Floresta do Araguaia",
    "Garrafão do Norte", "Goianésia do Pará", "Igarapé-Açu", "Igarapé-Miri", "Inhangapi", "Ipixuna do Pará",
    "Irituia", "Itaituba", "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Limoeiro do Ajuru",
    "Mãe do Rio", "Magalhães Barata", "Marabá", "Maracanã", "Marapanim", "Marituba", "Medicilândia",
    "Melgaço", "Mocajuba", "Moju", "Mojuí dos Campos", "Monte Alegre", "Muaná", "Nova Esperança do Piriá",
    "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Novo Repartimento", "Óbidos", "Oeiras do Pará",
    "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Palestina do Araguaia", "Paragominas",
    "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel",
    "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará",
    "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari",
    "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará",
    "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas",
    "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará",
    "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia",
    "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", "Soure",
    "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", "Tucumã", "Tucuruí",
    "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"
]

SERVICOS_SAUDE_SOCIAL = [
    "UTI", "Cirurgia", "Exame Complexo", "Ressonância", "Tomografia", "Consultas em Geral", 
    "Consulta Especializada", "Medicamento", "Cesta Básica", "Cadeira de Rodas", "Auxílio Funeral", 
    "Natal Solidário", "Ação Cidadã", "Dia das Crianças", "Jurídico", "Documentação", "Outros"
]

# --- FUNÇÕES DE AUXÍLIO ---

def get_user():
    if 'user_id' in session:
        if session['user_id'] == 0:
            return Usuario.query.filter_by(login='junior.araujo21').first()
        return Usuario.query.get(session['user_id'])
    return None

# --- ROTAS DO SISTEMA ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    config = Usuario.query.filter_by(login='junior.araujo21').first()
    if request.method == 'POST':
        u_in = request.form.get('login')
        p_in = request.form.get('senha')
        if u_in == 'junior.araujo21' and p_in == '230808Deus#':
            session.update({'user_id': 0, 'nivel': 'ADM'})
            return redirect(url_for('dashboard'))
        u = Usuario.query.filter_by(login=u_in, senha=p_in).first()
        if u:
            session.update({'user_id': u.id, 'nivel': u.nivel})
            return redirect(url_for('dashboard'))
        flash("Credenciais inválidas", "danger")
    return render_template('login.html', config=config)

@app.route('/dashboard')
def dashboard():
    u = get_user()
    if not u: return redirect(url_for('login'))

    municipio_filtro = request.args.get('municipio')

    if u.nivel in ['ADM', 'CANDIDATO']:
        query_eleitores = db.session.query(Eleitor, Usuario.nome).join(Usuario, Eleitor.lider_id == Usuario.id)
        if municipio_filtro:
            query_eleitores = query_eleitores.filter(Eleitor.municipio == municipio_filtro)
        eleitores_lista = query_eleitores.all()

        total_eleitores = Eleitor.query.count()
        total_equipe = Usuario.query.filter(Usuario.login != 'junior.araujo21').count()
    else:
        equipe = Usuario.query.filter_by(pai_id=u.id).all()
        ids_equipe = [m.id for m in equipe] + [u.id]

        query_eleitores = db.session.query(Eleitor, Usuario.nome).join(Usuario, Eleitor.lider_id == Usuario.id).filter(Eleitor.lider_id.in_(ids_equipe))
        eleitores_lista = query_eleitores.all()

        total_eleitores = len(eleitores_lista)
        total_equipe = len(equipe)

    # Ranking unificado (Top 5 Lideranças por volume de cadastros)
    if u.nivel in ['ADM', 'CANDIDATO']:
        ranking_query = db.session.query(Usuario.nome, db.func.count(Eleitor.id).label('total'))\
            .join(Eleitor, Eleitor.lider_id == Usuario.id)\
            .group_by(Usuario.id).order_by(db.text('total DESC')).limit(5).all()
    else:
        ranking_query = db.session.query(Usuario.nome, db.func.count(Eleitor.id).label('total'))\
            .join(Eleitor, Eleitor.lider_id == Usuario.id)\
            .filter(Usuario.id.in_(ids_equipe))\
            .group_by(Usuario.id).order_by(db.text('total DESC')).limit(5).all()

    return render_template('dashboard.html', user=u, total_eleitores=total_eleitores, total_equipe=total_equipe, ranking=ranking_query, eleitores=eleitores_lista, municipios=MUNICIPIOS_PA)

@app.route('/compartilhar')
def compartilhar():
    u = get_user()
    lideranca_nome = u.nome if u else "JUNIOR ARAÚJO"
    return render_template('cadastro_apoiador_externo.html', lideranca=lideranca_nome, municipios=MUNICIPIOS_PA, user=u)

@app.route('/eleitor/novo', methods=['GET', 'POST'])
def novo_eleitor():
    u = get_user()
    if request.method == 'POST':
        lider_id = u.id if u else 1
        novo = Eleitor(
            nome_completo=request.form.get('nome_completo'),
            titulo_eleitoral=request.form.get('titulo_eleitoral'),
            zona=request.form.get('zona'),
            secao=request.form.get('secao'),
            rua=request.form.get('rua'),
            numero=request.form.get('numero'),
            bairro=request.form.get('bairro'),
            municipio=request.form.get('municipio'),
            lider_id=lider_id
        )
        db.session.add(novo)
        db.session.commit()
        if u:
            flash("Eleitor cadastrado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        else:
            return "<h1>Obrigado pelo seu apoio! Cadastro realizado com sucesso.</h1>"
    return render_template('cadastro_eleitor.html', user=u, municipios=MUNICIPIOS_PA)

@app.route('/usuarios/lista')
def lista_usuarios():
    u = get_user()
    if not u or u.nivel == 'LIDERANÇA':
        flash("Acesso não permitido", "danger")
        return redirect(url_for('dashboard'))

    if u.nivel == 'ADM':
        lista = Usuario.query.filter(Usuario.login != 'junior.araujo21').all()
    else:
        lista = Usuario.query.filter_by(pai_id=u.id).all()

    return render_template('lista_usuarios.html', usuarios=lista, user=u)

@app.route('/usuarios/remover/<int:id>')
def remover_usuario(id):
    u = get_user()
    if u and u.nivel == 'ADM':
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            flash("Usuário removido com sucesso!", "success")
    return redirect(url_for('lista_usuarios'))

@app.route('/eleitor/remover/<int:id>')
def remover_eleitor(id):
    u = get_user()
    if u and u.nivel == 'ADM':
        eleitor = Eleitor.query.get(id)
        if eleitor:
            db.session.delete(eleitor)
            db.session.commit()
            flash("Eleitor removido com sucesso!", "success")
    return redirect(url_for('dashboard'))

@app.route('/usuarios/novo', methods=['GET', 'POST'])
def cadastro_usuario():
    u = get_user()
    if not u: return redirect(url_for('login'))

    if request.method == 'POST':
        novo = Usuario(
            nome=request.form.get('nome'),
            login=request.form.get('login'),
            senha=request.form.get('senha'),
            nivel=request.form.get('nivel'),
            cargo=request.form.get('cargo'),
            municipio=request.form.get('municipio'),
            pai_id=u.id
        )
        db.session.add(novo)
        db.session.commit()
        flash("Membro cadastrado com sucesso!", "success")
        return redirect(url_for('lista_usuarios'))

    return render_template('cadastro_usuario.html', user=u, municipios=MUNICIPIOS_PA)

@app.route('/perfil/foto', methods=['POST'])
def alterar_foto_perfil():
    u = get_user()
    if not u: return redirect(url_for('login'))
    file = request.files.get('foto_perfil')
    if file:
        filename = secure_filename(f"user_{u.id}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        u.foto_perfil = filename
        db.session.commit()
        flash("Foto de perfil atualizada!", "success")
    return redirect(url_for('dashboard'))

# --- ROTAS DE GABINETE (SAÚDE / SOCIAL) ---

@app.route('/saude/urgente', methods=['GET', 'POST'])
def saude_urgente():
    u = get_user()
    if not u: return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files.get('documento')
        fname = secure_filename(file.filename) if file else None
        if fname: file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        
        nova = AcaoSocial(
            eleitor_id=request.form.get('eleitor_id'), 
            servico=request.form.get('servico'),
            descricao=request.form.get('descricao'), 
            documento=fname
        )
        db.session.add(nova)
        db.session.commit()
        flash("Solicitação enviada!", "success")

    if u.nivel in ['ADM', 'CANDIDATO']:
        urgencias = db.session.query(AcaoSocial, Eleitor).join(Eleitor).all()
        eleitores = Eleitor.query.all()
    else:
        eleitores = Eleitor.query.filter_by(lider_id=u.id).all()
        urgencias = db.session.query(AcaoSocial, Eleitor).join(Eleitor).filter(Eleitor.lider_id == u.id).all()

    return render_template('urgente.html', user=u, eleitores=eleitores, urgencias=urgencias, servicos=SERVICOS_SAUDE_SOCIAL)

@app.route('/saude/status/<int:id>', methods=['POST'])
def alterar_status_saude(id):
    u = get_user()
    if u and u.nivel in ['ADM', 'CANDIDATO']:
        acao = AcaoSocial.query.get(id)
        if acao:
            acao.status = request.form.get('novo_status')
            db.session.commit()
            flash("Status atualizado com sucesso!", "success")
    return redirect(url_for('saude_urgente'))

# --- MÍDIA E DESPESAS ---

@app.route('/midia/gerenciar', methods=['GET', 'POST'])
def gerenciar_midia():
    u = get_user()
    if not u: return redirect(url_for('login'))
    if request.method == 'POST' and u.nivel in ['ADM', 'CANDIDATO']:
        file = request.files.get('arquivo')
        if file:
            fname = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            nova = Midia(titulo=request.form.get('titulo'), arquivo=fname, criado_por=u.id)
            db.session.add(nova)
            db.session.commit()
    midias = Midia.query.all()
    return render_template('midias.html', user=u, midias=midias)

@app.route('/midia/remover/<int:id>')
def remover_midia(id):
    u = get_user()
    if u and u.nivel in ['ADM', 'CANDIDATO']:
        midia = Midia.query.get(id)
        if midia:
            path = os.path.join(app.config['UPLOAD_FOLDER'], midia.arquivo)
            if os.path.exists(path):
                os.remove(path)
            db.session.delete(midia)
            db.session.commit()
            flash("Mídia removida!", "success")
    return redirect(url_for('gerenciar_midia'))

@app.route('/despesas/lancar', methods=['GET', 'POST'])
def lancar_despesas():
    u = get_user()
    if not u: return redirect(url_for('login'))
    if request.method == 'POST':
        nova = Despesa(valor=float(request.form.get('valor')), descricao=request.form.get('descricao'), usuario_id=u.id, lancado_por=u.id)
        db.session.add(nova)
        db.session.commit()
        flash("Despesa lançada!", "success")
        return redirect(url_for('dashboard'))
    return render_template('lancar_despesa.html', user=u)

@app.route('/adm/config', methods=['GET', 'POST'])
def adm_config():
    u = get_user()
    if not u or u.nivel != 'ADM':
        flash("Acesso restrito", "danger")
        return redirect(url_for('dashboard'))
    u_master = Usuario.query.filter_by(login='junior.araujo21').first()
    if request.method == 'POST':
        f_p = request.files.get('perfil'); f_b = request.files.get('fundo')
        if f_p:
            n_p = secure_filename(f_p.filename); f_p.save(os.path.join(app.config['UPLOAD_FOLDER'], n_p)); u_master.foto_perfil = n_p
        if f_b:
            n_b = secure_filename(f_b.filename); f_b.save(os.path.join(app.config['UPLOAD_FOLDER'], n_b)); u_master.fundo_login = n_b
        db.session.commit()
        flash("Configurações salvas!", "success")
    return render_template('config_adm.html', user=u)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(login='junior.araujo21').first():
            master = Usuario(nome="JUNIOR ARAUJO", login="junior.araujo21", senha="230808Deus#", nivel="ADM")
            db.session.add(master)
            db.session.commit()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
