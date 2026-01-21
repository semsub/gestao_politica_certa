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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/junior_araujo_sistemas.db'
    app.config['UPLOAD_FOLDER'] = '/data/static/uploads'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'junior_araujo_sistemas.db')
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    meta_cadastros = db.Column(db.Integer, default=0)
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
    tipo = db.Column(db.String(50))
    servico = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    status = db.Column(db.String(50), default='Aguardando')
    documento = db.Column(db.String(200))
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    beneficiario = db.Column(db.String(150))
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
        query_eleitores = db.session.query(Eleitor, Usuario).join(Usuario, Eleitor.lider_id == Usuario.id)
        if municipio_filtro:
            query_eleitores = query_eleitores.filter(Eleitor.municipio == municipio_filtro)
        eleitores_raw = query_eleitores.all()
        total_eleitores = Eleitor.query.count()
        total_equipe = Usuario.query.filter(Usuario.login != 'junior.araujo21').count()
    else:
        equipe = Usuario.query.filter_by(pai_id=u.id).all()
        ids_equipe = [m.id for m in equipe] + [u.id]
        query_eleitores = db.session.query(Eleitor, Usuario).join(Usuario, Eleitor.lider_id == Usuario.id).filter(Eleitor.lider_id.in_(ids_equipe))
        eleitores_raw = query_eleitores.all()
        total_eleitores = len(eleitores_raw)
        total_equipe = len(equipe)

    ranking_query = db.session.query(Usuario.nome, db.func.count(Eleitor.id).label('total'))\
        .join(Eleitor, Eleitor.lider_id == Usuario.id).group_by(Usuario.id).order_by(db.text('total DESC')).limit(5).all()

    eleitores_lista = []
    for el, lider in eleitores_raw:
        nome_exibicao = lider.nome
        eleitores_lista.append((el, nome_exibicao))

    return render_template('dashboard.html', user=u, total_eleitores=total_eleitores, total_equipe=total_equipe, ranking=ranking_query, eleitores=eleitores_lista, municipios=MUNICIPIOS_PA)

@app.route('/compartilhar')
def compartilhar():
    u = get_user()
    if not u: return redirect(url_for('login'))
    lider_id = request.args.get('lider', default=u.id, type=int)
    u_lider = Usuario.query.get(lider_id)
    lideranca_nome = u_lider.nome if u_lider else "JUNIOR ARAÚJO"
    return render_template('compartilhar.html', user=u, lider_id=lider_id, lideranca_nome=lideranca_nome)

@app.route('/eleitor/novo', methods=['GET', 'POST'])
def novo_eleitor():
    u = get_user()
    if request.method == 'POST':
        lider_id_form = request.form.get('lider_id')
        lider_final = lider_id_form if lider_id_form else (u.id if u else 1)
        novo = Eleitor(
            nome_completo=request.form.get('nome_completo'),
            titulo_eleitoral=request.form.get('titulo_eleitoral'),
            zona=request.form.get('zona'),
            secao=request.form.get('secao'),
            rua=request.form.get('rua'),
            numero=request.form.get('numero'),
            bairro=request.form.get('bairro'),
            municipio=request.form.get('municipio'),
            lider_id=lider_final
        )
        db.session.add(novo); db.session.commit()
        if u:
            flash("Eleitor cadastrado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        return "<h1>Obrigado! Cadastro realizado com sucesso.</h1>"
    return render_template('cadastro_eleitor.html', user=u, municipios=MUNICIPIOS_PA)

@app.route('/eleitor/remover/<int:id>')
def remover_eleitor(id):
    u = get_user()
    if u and u.nivel == 'ADM':
        eleitor = Eleitor.query.get(id); db.session.delete(eleitor); db.session.commit()
        flash("Eleitor removido!", "success")
    return redirect(url_for('dashboard'))

# --- GESTÃO DE USUÁRIOS ---

@app.route('/usuarios/lista')
def lista_usuarios():
    u = get_user()
    if not u or u.nivel == 'LIDERANÇA': return redirect(url_for('dashboard'))
    lista = Usuario.query.filter(Usuario.login != 'junior.araujo21').all() if u.nivel == 'ADM' else Usuario.query.filter_by(pai_id=u.id).all()
    return render_template('lista_usuarios.html', usuarios=lista, user=u)

@app.route('/usuarios/novo', methods=['GET', 'POST'])
def cadastro_usuario():
    u = get_user()
    if not u: return redirect(url_for('login'))
    if request.method == 'POST':
        novo = Usuario(
            nome=request.form.get('nome'), login=request.form.get('login'),
            senha=request.form.get('senha'), nivel=request.form.get('nivel'),
            cargo=request.form.get('cargo'), municipio=request.form.get('municipio'),
            meta_cadastros=request.form.get('meta', 0), pai_id=u.id
        )
        db.session.add(novo); db.session.commit()
        flash("Membro cadastrado com sucesso!", "success")
        return redirect(url_for('lista_usuarios'))
    return render_template('cadastro_usuario.html', user=u, municipios=MUNICIPIOS_PA)

@app.route('/usuarios/remover/<int:id>')
def remover_usuario(id):
    u = get_user()
    if u and u.nivel == 'ADM':
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario); db.session.commit()
            flash("Usuário removido!", "success")
    return redirect(url_for('lista_usuarios'))

# --- SAÚDE E AÇÕES SOCIAIS ---

@app.route('/atualizar_status_saude', methods=['POST'])
def atualizar_status_saude_ajax():
    u = get_user()
    if not u: return jsonify({'success': False, 'message': 'Não logado'}), 401
    data = request.get_json()
    acao = AcaoSocial.query.get(data.get('id'))
    if acao:
        acao.status = data.get('status')
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

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
            documento=fname,
            status='Aguardando'
        )
        db.session.add(nova); db.session.commit()
        flash("Solicitação enviada!", "success")

    if u.nivel in ['ADM', 'CANDIDATO']:
        eleitores = Eleitor.query.all()
        acoes_raw = db.session.query(AcaoSocial, Eleitor).join(Eleitor).order_by(AcaoSocial.data_registro.desc()).all()
    else:
        eleitores = Eleitor.query.filter_by(lider_id=u.id).all()
        acoes_raw = db.session.query(AcaoSocial, Eleitor).join(Eleitor).filter(Eleitor.lider_id == u.id).order_by(AcaoSocial.data_registro.desc()).all()

    acoes_lista = [{'id': a.id, 'nome_eleitor': e.nome_completo, 'municipio': e.municipio, 'servico': a.servico, 'status': a.status, 'data': a.data_registro.strftime('%d/%m/%Y'), 'documento': a.documento} for a, e in acoes_raw]
    return render_template('urgente.html', user=u, eleitores=eleitores, acoes=acoes_lista)

# --- FINANÇAS E MÍDIA ---

@app.route('/despesas/lancar', methods=['GET', 'POST'])
def lancar_despesas():
    u = get_user()
    if not u: return redirect(url_for('login'))
    if request.method == 'POST':
        nova = Despesa(valor=float(request.form.get('valor')), descricao=request.form.get('descricao'), beneficiario=request.form.get('beneficiario'), usuario_id=u.id, lancado_por=u.id)
        db.session.add(nova); db.session.commit()
        flash("Despesa lançada!", "success")
        return redirect(url_for('dashboard'))
    beneficiarios = [usr.nome for usr in Usuario.query.all()] + [el.nome_completo for el in Eleitor.query.all()]
    return render_template('lancar_despesa.html', user=u, beneficiarios=sorted(list(set(beneficiarios))))

@app.route('/midia/gerenciar', methods=['GET', 'POST'])
def gerenciar_midia():
    u = get_user()
    if request.method == 'POST' and u.nivel in ['ADM', 'CANDIDATO']:
        file = request.files.get('arquivo')
        if file:
            fname = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            nova = Midia(titulo=request.form.get('titulo'), arquivo=fname, criado_por=u.id)
            db.session.add(nova); db.session.commit()
    midias = Midia.query.all()
    return render_template('midias.html', user=u, midias=midias)

@app.route('/midia/remover/<int:id>')
def remover_midia(id):
    u = get_user()
    if u and u.nivel in ['ADM', 'CANDIDATO']:
        m = Midia.query.get(id); db.session.delete(m); db.session.commit()
        flash("Mídia removida!", "success")
    return redirect(url_for('gerenciar_midia'))

# --- CONFIGURAÇÕES E PERFIL ---

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
    return redirect(request.referrer)

@app.route('/adm/config', methods=['GET', 'POST'])
def adm_config():
    u = get_user()
    if not u or u.nivel != 'ADM': return redirect(url_for('dashboard'))
    u_master = Usuario.query.filter_by(login='junior.araujo21').first()
    if request.method == 'POST':
        f_p = request.files.get('perfil'); f_b = request.files.get('fundo')
        if f_p: n_p = secure_filename(f_p.filename); f_p.save(os.path.join(app.config['UPLOAD_FOLDER'], n_p)); u_master.foto_perfil = n_p
        if f_b: n_b = secure_filename(f_b.filename); f_b.save(os.path.join(app.config['UPLOAD_FOLDER'], n_b)); u_master.fundo_login = n_b
        db.session.commit(); flash("Configurações salvas!", "success")
    return render_template('config_adm.html', user=u)

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(login='junior.araujo21').first():
            master = Usuario(nome="JUNIOR ARAUJO", login="junior.araujo21", senha="230808Deus#", nivel="ADM")
            db.session.add(master); db.session.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
