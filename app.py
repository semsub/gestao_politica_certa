import os, json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "junior_pa_2026_sistema_seguro_v5"

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DB_FILE = os.path.join(BASE_DIR, "banco_dados.json")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria as pastas de fotos se não existirem (Evita Erro 500)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MUNICIPIOS_PA = ["Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", "Altamira", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", "Baião", "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito", "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru", "Cachoeira do Arari", "Cachoeira do Piriá", "Caeté", "Canaã dos Carajás", "Capanema", "Capitão Poço", "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", "Cumaru do Norte", "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu", "Eldorado dos Carajás", "Faro", "Floresta do Araguaia", "Garrafão do Norte", "Goianésia do Pará", "Itaituba", "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Marabá", "Marituba", "Medicilândia", "Melgaço", "Mocajuba", "Moju", "Monte Alegre", "Muaná", "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Óbidos", "Oeiras do Pará", "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Paragominas", "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel", "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará", "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari", "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará", "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas", "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará", "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia", "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", "Soure", "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", "Tucumã", "Tucuruí", "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"]

def carregar():
    if not os.path.exists(DB_FILE):
        return {"usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo_sistema": "CRIADOR", "nome": "Júnior Araújo", "foto": ""}}, "eleitores": []}
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo_sistema": "CRIADOR", "nome": "Júnior Araújo", "foto": ""}}, "eleitores": []}

def salvar(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=4, ensure_ascii=False)

@app.context_processor
def inject():
    d = carregar()
    cands = {k: v for k, v in d['usuarios'].items() if v.get('cargo_sistema') == 'CANDIDATO'}
    return dict(municipios=MUNICIPIOS_PA, lista_cands=cands)

@app.route('/')
def index():
    if 'user' not in session: return redirect(url_for('login_page'))
    d = carregar()
    u = session.get('user_data')
    l_u = session.get('user')
    
    if not u: return redirect(url_for('logout'))

    # RENDIMENTO (CONTADORES)
    if u['cargo_sistema'] == 'CRIADOR':
        equipe = d['usuarios']
        eleitores = d['eleitores']
    else:
        equipe = {k: v for k, v in d['usuarios'].items() if v.get('cand_pai') == l_u or v.get('criador_por') == l_u or k == l_u}
        eleitores = [e for e in d['eleitores'] if e.get('cand_pai') == l_u or e.get('criador_por') == l_u]

    stats_mun = {}
    for e in eleitores:
        m = e.get('municipio')
        if m: stats_mun[m] = stats_mun.get(m, 0) + 1
    
    total_l = len([v for v in equipe.values() if v.get('cargo_sistema') == 'LIDERANÇA'])

    return render_template('dashboard.html', user=u, equipe=equipe, eleitores=eleitores, stats=stats_mun, total_l=total_l)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = request.form.get('senha')
        d = carregar()
        if login in d['usuarios'] and str(d['usuarios'][login]['senha']) == str(senha):
            session['user'] = login
            session['user_data'] = d['usuarios'][login]
            return redirect(url_for('index'))
        flash("Acesso Negado: Login ou Senha Incorretos")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
