from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "junior_araujo_2026_mestre_pa"

# Configurações de Upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DB_FILE = "banco_dados.json"

# --- DADOS ESTÁTICOS ---
MUNICIPIOS_PA = ["Abaetetuba", "Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", "Altamira", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", "Baião", "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito", "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru", "Cachoeira do Arari", "Cachoeira do Piriá", "Caeté", "Canaã dos Carajás", "Capanema", "Capitão Poço", "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", "Cumaru do Norte", "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu", "Eldorado dos Carajás", "Faro", "Floresta do Araguaia", "Garrafão do Norte", "Goianésia do Pará", "Itaituba", "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Marabá", "Marituba", "Medicilândia", "Melgaço", "Mocajuba", "Moju", "Monte Alegre", "Muaná", "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Óbidos", "Oeiras do Pará", "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Paragominas", "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel", "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará", "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari", "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará", "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas", "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará", "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia", "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", "Soure", "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", "Tucumã", "Tucuruí", "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"]

CARGOS_POLITICOS = ["CANDIDATO À VEREADOR", "CANDIDATO À PREFEITO", "CANDIDATO À DEPUTADO FEDERAL", "CANDIDATO À DEPUTADO ESTADUAL", "CANDIDATO À SENADOR", "CANDIDATO À GOVERNADOR", "CANDIDATO À PRESIDENTE"]

SETORES_COORD = ["GERAL", "MARKETING", "FINANCEIRO", "LIDERANÇA"]

def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo_sistema": "CRIADOR", "nome": "Júnior Araújo"}},
        "eleitores": [], "financas": [], "config": {"logo": ""}
    }

def salvar_dados(dados):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.context_processor
def inject_logo():
    dados = carregar_dados()
    return dict(logo_url=dados.get('config', {}).get('logo', ''))

@app.route('/')
def index():
    if 'user' not in session: return redirect(url_for('login_page'))
    dados = carregar_dados()
    u = session['user_data']
    l_u = session['user']
    
    # Filtros de Hierarquia
    if u['cargo_sistema'] == 'CRIADOR':
        eleitores = dados['eleitores']
    elif u['cargo_sistema'] == 'CANDIDATO':
        eleitores = [e for e in dados['eleitores'] if e.get('id_candidato') == l_u]
    elif u['cargo_sistema'] == 'COORDENADOR':
        eleitores = [e for e in dados['eleitores'] if e.get('id_coord') == l_u]
    else: # Liderança
        eleitores = [e for e in dados['eleitores'] if e.get('id_lider') == l_u]

    stats_mun = {}
    for e in eleitores:
        m = e.get('municipio', 'Outros')
        stats_mun[m] = stats_mun.get(m, 0) + 1

    return render_template('dashboard.html', user=u, eleitores=eleitores, stats_mun=stats_mun, 
                           municipios=MUNICIPIOS_PA, cargos=CARGOS_POLITICOS, setores=SETORES_COORD,
                           financas=[f for f in dados.get('financas', []) if f.get('id_cand') == (l_u if u['cargo_sistema'] == 'CANDIDATO' else u.get('id_candidato'))])

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user, senha = request.form.get('login'), request.form.get('senha')
        dados = carregar_dados()
        if user in dados['usuarios'] and dados['usuarios'][user]['senha'] == senha:
            session['user'] = user
            session['user_data'] = dados['usuarios'][user]
            return redirect(url_for('index'))
        flash("Login ou senha incorretos.")
    return render_template('login.html')

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    if 'logo' not in request.files: return redirect(request.url)
    file = request.files['logo']
    if file.filename == '': return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dados = carregar_dados()
        dados['config']['logo'] = filename
        salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    dados = carregar_dados()
    login = request.form.get('login')
    cargo = request.form.get('cargo_sistema')
    u_atual = session['user_data']
    
    novo = {
        "nome": request.form.get('nome'), "senha": request.form.get('senha'),
        "cargo_sistema": cargo, "municipio": request.form.get('municipio'),
        "id_candidato": session['user'] if u_atual['cargo_sistema'] == 'CANDIDATO' else u_atual.get('id_candidato')
    }
    if cargo == "CANDIDATO": novo["cargo_politico"] = request.form.get('cargo_politico')
    if cargo == "COORDENADOR": novo["setor"] = request.form.get('setor')
    
    dados['usuarios'][login] = novo
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_eleitor', methods=['POST'])
def cadastrar_eleitor():
    dados = carregar_dados()
    u = session['user_data']
    novo = {
        "nome": request.form.get('nome'), "titulo": request.form.get('titulo'),
        "zona": request.form.get('zona'), "secao": request.form.get('secao'),
        "contato": request.form.get('contato'), "municipio": u.get('municipio'),
        "id_lider": session['user'], "id_candidato": u.get('id_candidato')
    }
    dados['eleitores'].append(novo)
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_financa', methods=['POST'])
def cadastrar_financa():
    dados = carregar_dados()
    dados['financas'].append({
        "desc": request.form.get('desc'), "valor": float(request.form.get('valor')),
        "tipo": request.form.get('tipo'), "id_cand": session['user']
    })
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
