from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = "junior_araujo_2026_chave_mestre"

DB_FILE = "banco_dados.json"

# Função para carregar dados do arquivo JSON
def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "usuarios": {
            "junior.araujo21": {
                "senha": "230808Deus#", 
                "cargo_sistema": "CRIADOR", 
                "nome": "Júnior Araújo"
            }
        },
        "liderancas": {},
        "eleitores": []
    }

# Função para salvar dados no arquivo JSON
def salvar_dados(dados):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    
    dados = carregar_dados()
    user_data = session['user_data']
    
    # Lógica de Dashboard: Se for Candidato/Coord, vê tudo. Se for Líder, vê só o dele.
    if user_data['cargo_sistema'] in ['CRIADOR', 'CANDIDATO', 'COORDENADOR']:
        meus_eleitores = dados['eleitores']
    else:
        meus_eleitores = [e for e in dados['eleitores'] if e['lideranca_login'] == session['user']]

    return render_template('dashboard.html', 
                           user=user_data, 
                           total_eleitores=len(meus_eleitores),
                           lista_eleitores=meus_eleitores,
                           liderancas=dados['liderancas'])

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user = request.form.get('login')
        senha = request.form.get('senha')
        dados = carregar_dados()
        
        if user in dados['usuarios'] and dados['usuarios'][user]['senha'] == senha:
            session['user'] = user
            session['user_data'] = dados['usuarios'][user]
            return redirect(url_for('index'))
        else:
            flash("Login ou Senha incorretos!")
            
    return render_template('login.html')

@app.route('/cadastrar_candidato', methods=['POST'])
def cadastrar_candidato():
    if session['user_data']['cargo_sistema'] != 'CRIADOR':
        return "Acesso Negado", 403
    
    dados = carregar_dados()
    login = request.form.get('login')
    dados['usuarios'][login] = {
        "senha": request.form.get('senha'),
        "nome": request.form.get('nome'),
        "cargo_sistema": "CANDIDATO",
        "cargo_politico": request.form.get('cargo_politico')
    }
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_hierarquia', methods=['POST'])
def cadastrar_hierarquia():
    dados = carregar_dados()
    login = request.form.get('login')
    tipo = request.form.get('tipo')
    
    dados['usuarios'][login] = {
        "senha": request.form.get('senha'),
        "nome": request.form.get('nome'),
        "cargo_sistema": tipo,
        "superior": session['user']
    }
    
    if tipo == 'LIDERANCA':
        dados['liderancas'][login] = {
            "nome": request.form.get('nome'),
            "municipio": request.form.get('municipio'),
            "base": []
        }
    
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/cadastrar_eleitor', methods=['POST'])
def cadastrar_eleitor():
    dados = carregar_dados()
    novo_eleitor = {
        "nome": request.form.get('nome'),
        "titulo": request.form.get('titulo'),
        "zona": request.form.get('zona'),
        "secao": request.form.get('secao'),
        "contato": request.form.get('contato'),
        "lideranca_nome": session['user_data']['nome'],
        "lideranca_login": session['user']
    }
    dados['eleitores'].append(novo_eleitor)
    salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
