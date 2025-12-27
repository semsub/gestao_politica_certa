from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = "junior_araujo_2026_mestre"

DB_FILE = "banco_dados.json"

# --- DADOS ESTÁTICOS ---
MUNICIPIOS_PA = [
    "Abaetetuba", "Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", 
    "Altamira", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", 
    "Baião", "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", 
    "Bonito", "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", 
    "Bujaru", "Cachoeira do Arari", "Cachoeira do Piriá", "Caeté", "Canaã dos Carajás", "Capanema", 
    "Capitão Poço", "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", 
    "Cumaru do Norte", "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu", "Eldorado dos Carajás", 
    "Faro", "Floresta do Araguaia", "Garrafão do Norte", "Goianésia do Pará", "Itaituba", "Itupiranga", 
    "Jacareacanga", "Jacundá", "Juruti", "Marabá", "Marituba", "Medicilândia", "Melgaço", "Mocajuba", 
    "Moju", "Monte Alegre", "Muaná", "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Óbidos", 
    "Oeiras do Pará", "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Paragominas", 
    "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel", 
    "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará", 
    "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari", 
    "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará", 
    "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas", 
    "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará", 
    "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia", 
    "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", 
    "Soure", "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", 
    "Tucumã", "Tucuruí", "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"
]

CARGOS_CANDIDATO = [
    "VEREADOR", "PREFEITO", "DEPUTADO FEDERAL", 
    "DEPUTADO ESTADUAL", "SENADOR", "GOVERNADOR", "PRESIDENTE"
]

SETORES_COORD = ["GERAL", "MARKETING", "FINANCEIRO", "LIDERANÇA"]

# --- FUNÇÕES DE BANCO ---
def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo_sistema": "CRIADOR", "nome": "Júnior Araújo"}},
        "eleitores": [],
        "financas": []
    }

def salvar_dados(dados):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# --- ROTAS ---
@app.route('/')
def index():
    if 'user' not in session: return redirect(url_for('login_page'))
    
    dados = carregar_dados()
    user_data = session['user_data']
    login_atual = session['user']
    
    # Lógica de Visibilidade
    if user_data['cargo_sistema'] == 'CRIADOR':
        eleitores = dados['eleitores']
    elif user_data['cargo_sistema'] == 'CANDIDATO':
        # Vê todos que foram cadastrados sob a sua árvore (lideranças e coordenadores dele)
        eleitores = [e for e in dados['eleitores'] if e.get('candidato_pai') == login_atual]
    elif user_data['cargo_sistema'] == 'COORDENADOR':
        eleitores = [e for e in dados['eleitores'] if e.get('cadastrado_por_login') == login_atual or e.get('coord_pai') == login_atual]
    else: # Liderança
        eleitores = [e for e in dados['eleitores'] if e.get('cadastrado_por_login') == login_atual]

    # Estatísticas por Município
    stats_mun = {}
    for e in eleitores:
        mun = e.get('municipio', 'Não Informado')
        stats_mun[mun] = stats_mun.get(mun, 0) + 1

    return render_template('dashboard.html', 
                           user=user_data, 
                           eleitores=eleitores, 
                           stats_mun=stats_mun,
                           municipios=MUNICIPIOS_PA,
                           cargos=CARGOS_CANDIDATO,
                           setores=SETORES_COORD,
                           financas=[f for f in dados.get('financas', []) if f.get('candidato') == login_atual])

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user = request.form.get('login')
        senha = request.form.get('senha')
        dados = carregar_dados()
        if user in dados['usuarios'] and dados['usuarios'][user]['senha'] == senha:
            session['user'] = user
            session['user_data'] = dados['usuarios'][user]
            session['user_data']['login'] = user # Garante o login nos dados
            return redirect(url_for('index'))
        flash("Credenciais inválidas!")
    return render_template('login.html')

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    dados = carregar_dados()
    login = request.form.get('login')
    cargo = request.form.get('cargo_sistema')
    
    novo_user = {
        "nome": request.form.get('nome'),
        "senha": request.form.get('senha'),
        "cargo_sistema": cargo,
        "municipio": request.form.get('municipio'),
        "criado_por": session['user']
    }

    # Lógica de Hierarquia
    if cargo == "CANDIDATO":
        novo_user["cargo_politico"] = request.form.get('cargo_politico')
    
    if session['user_data']['cargo_sistema'] == 'CANDIDATO':
        novo_user["candidato_pai"] = session['user']
    elif session['user_data']['cargo_sistema'] == 'COORDENADOR':
        novo_user["coord_pai"] = session['user']
        novo_user["candidato_pai"] = session['user_data'].get('candidato_pai')

    dados['usuarios'][login] = novo_user
    salvar_dados(dados)
    flash(f"{cargo} cadastrado com sucesso!")
    return redirect(url_for('index'))

@app.route('/cadastrar_eleitor', methods=['POST'])
def cadastrar_eleitor():
    dados = carregar_dados()
    user_data = session['user_data']
    
    novo = {
        "nome": request.form.get('nome'),
        "titulo": request.form.get('titulo'),
        "zona": request.form.get('zona'),
        "secao": request.form.get('secao'),
        "contato": request.form.get('contato'),
        "municipio": user_data.get('municipio'), # Pega o município da Liderança
        "cadastrado_por_nome": user_data['nome'],
        "cadastrado_por_login": session['user'],
        "candidato_pai": user_data.get('candidato_pai')
    }
    dados['eleitores'].append(novo)
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_financa', methods=['POST'])
def cadastrar_financa():
    dados = carregar_dados()
    nova_f = {
        "descricao": request.form.get('descricao'),
        "valor": request.form.get('valor'),
        "tipo": request.form.get('tipo'), # Entrada ou Saída
        "candidato": session['user']
    }
    if 'financas' not in dados: dados['financas'] = []
    dados['financas'].append(nova_f)
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
