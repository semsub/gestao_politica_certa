import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "junior_salinas_2026"

# Configurações de Pastas e Caminhos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DB_FILE = os.path.join(BASE_DIR, "banco_dados.json")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Listas de Apoio
MUNICIPIOS_PA = ["Salinópolis", "Belém", "Ananindeua", "Castanhal", "Capanema", "Santarém", "Marabá"] # + 144 municípios
CARGOS_POLITICOS = ["CANDIDATO À VEREADOR", "CANDIDATO À PREFEITO", "DEPUTADO ESTADUAL", "DEPUTADO FEDERAL", "SENADOR", "GOVERNADOR", "PRESIDENTE"]
ACOES_SOCIAIS = ["AÇÃO SOCIAL CIDADÃ (DOCUMENTOS)", "NATAL SOLIDÁRIO (CESTA BÁSICA)", "SAÚDE (EXAMES/CIRURGIAS/UTI)"]

def carregar_dados():
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except: pass
    return {
        "usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo_sistema": "CRIADOR", "nome": "Júnior Araújo", "municipio": "Salinópolis"}},
        "eleitores": [], "config": {"logo": ""}
    }

def salvar_dados(dados):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.context_processor
def inject_global():
    dados = carregar_dados()
    return dict(logo_url=dados.get('config', {}).get('logo', ''), municipios=MUNICIPIOS_PA, cargos=CARGOS_POLITICOS, acoes_disponiveis=ACOES_SOCIAIS)

@app.route('/')
def index():
    if 'user' not in session: return redirect(url_for('login_page'))
    dados = carregar_dados()
    u = session['user_data']
    l_u = session['user']
    
    # Filtro Hierárquico
    if u['cargo_sistema'] == 'CRIADOR':
        lista = dados['eleitores']
    elif u['cargo_sistema'] == 'CANDIDATO':
        lista = [e for e in dados['eleitores'] if e.get('cand_pai') == l_u]
    else:
        lista = [e for e in dados['eleitores'] if e.get('lider_pai') == l_u]

    return render_template('dashboard.html', user=u, eleitores=lista)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        login, senha = request.form.get('login'), request.form.get('senha')
        dados = carregar_dados()
        if login in dados['usuarios'] and dados['usuarios'][login]['senha'] == senha:
            session['user'] = login
            session['user_data'] = dados['usuarios'][login]
            return redirect(url_for('index'))
        flash("Erro: Acesso Negado")
    return render_template('login.html')

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    file = request.files.get('logo')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dados = carregar_dados()
        dados['config']['logo'] = filename
        salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/registrar_ajuda', methods=['POST'])
def registrar_ajuda():
    dados = carregar_dados()
    eleitor_index = int(request.form.get('eleitor_index'))
    nova_ajuda = {
        "tipo": request.form.get('tipo_ajuda'),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    if "historico_ajudas" not in dados['eleitores'][eleitor_index]:
        dados['eleitores'][eleitor_index]['historico_ajudas'] = []
    
    dados['eleitores'][eleitor_index]['historico_ajudas'].append(nova_ajuda)
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    dados = carregar_dados()
    login = request.form.get('login')
    cargo = request.form.get('cargo_sistema')
    dados['usuarios'][login] = {
        "nome": request.form.get('nome'), "senha": request.form.get('senha'),
        "cargo_sistema": cargo, "municipio": request.form.get('municipio'),
        "cargo_politico": request.form.get('cargo_politico'),
        "cand_pai": session['user'] if session['user_data']['cargo_sistema'] == 'CANDIDATO' else session['user_data'].get('cand_pai')
    }
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_eleitor', methods=['POST'])
def cadastrar_eleitor():
    dados = carregar_dados()
    u = session['user_data']
    dados['eleitores'].append({
        "nome": request.form.get('nome'), "contato": request.form.get('contato'),
        "municipio": u.get('municipio'), "lider_pai": session['user'],
        "cand_pai": u.get('cand_pai'), "historico_ajudas": []
    })
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
