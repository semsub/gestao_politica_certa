import os, json, uuid
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "junior_2026_blindado"

DB_FILE = "banco_dados.json"
MUNICIPIOS_PA = ["Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", "Altamira", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", "Baião", "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito", "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru", "Cachoeira do Arari", "Cachoeira do Piriá", "Caeté", "Canaã dos Carajás", "Capanema", "Capitão Poço", "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", "Cumaru do Norte", "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu", "Eldorado dos Carajás", "Faro", "Floresta do Araguaia", "Garrafão do Norte", "Goianésia do Pará", "Itaituba", "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Marabá", "Marituba", "Medicilândia", "Melgaço", "Mocajuba", "Moju", "Monte Alegre", "Muaná", "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Óbidos", "Oeiras do Pará", "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Paragominas", "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel", "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará", "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari", "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará", "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas", "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará", "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia", "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", "Soure", "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", "Tucumã", "Tucuruí", "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"]

def carregar():
    if not os.path.exists(DB_FILE):
        d = {"usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo": "ADM", "nome": "Júnior Araújo", "municipio": "Salinópolis"}}, "cadastros": []}
        with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)
        return d
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def salvar(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)

# HTML UNIFICADO (DENTRO DO PYTHON PARA NÃO DAR ERRO)
HTML_LOGIN = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Login - GP 2026</title>
</head>
<body class="bg-light d-flex align-items-center" style="height: 100vh;">
    <div class="container border rounded bg-white p-4 shadow-sm" style="max-width: 400px;">
        <h4 class="text-center fw-bold text-primary">GP 2026</h4>
        <form method="POST">
            <label>Login:</label><input type="text" name="login" class="form-control mb-2" required>
            <label>Senha:</label><input type="password" name="senha" class="form-control mb-3" required>
            <button class="btn btn-primary w-100 fw-bold">ENTRAR</button>
        </form>
    </div>
</body>
</html>
'''

HTML_DASH = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <title>Dashboard</title>
    <style>
        body { background: #f8fafc; font-size: 14px; }
        .card-app { border-radius: 15px; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 10px; }
        .fab { position: fixed; bottom: 20px; right: 20px; width: 60px; height: 60px; border-radius: 50%; background: #22c55e; color: white; border: none; font-size: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 1000; }
    </style>
</head>
<body>
    <div class="bg-primary text-white p-3 mb-4 shadow">
        <div class="d-flex justify-content-between align-items-center">
            <span><b>{{ user.nome }}</b> ({{ user.cargo }})</span>
            <a href="/logout" class="btn btn-sm btn-light">Sair</a>
        </div>
        <div class="row mt-3 text-center">
            <div class="col-6 border-end"><b>{{ contas.FAMILIA }}</b><br><small>FAMÍLIAS</small></div>
            <div class="col-6"><b>{{ contas.PESSOA }}</b><br><small>PESSOAS</small></div>
        </div>
    </div>

    <div class="container pb-5">
        {% if user.cargo in ['ADM', 'CANDIDATO'] %}
        <div class="d-grid gap-2 mb-4">
            <button class="btn btn-dark p-3 rounded-4 fw-bold" data-bs-toggle="modal" data-bs-target="#mEquipe">GERENCIAR EQUIPE</button>
            <button class="btn btn-info text-white p-3 rounded-4 fw-bold" data-bs-toggle="modal" data-bs-target="#mSenhas">USUÁRIOS E SENHAS</button>
        </div>
        {% endif %}

        <h6 class="fw-bold text-muted mb-3">LISTA DE CADASTROS</h6>
        {% for c in lista %}
        <div class="card card-app p-3">
            <div class="d-flex justify-content-between align-items-start">
                <span class="badge {% if c.tipo == 'FAMILIA' %}bg-primary{% else %}bg-success{% endif %}">{{ c.tipo }}</span>
                <a href="/excluir_reg/{{c.id}}" class="text-danger" onclick="return confirm('Excluir?')"><i class="bi bi-trash"></i></a>
            </div>
            <h6 class="fw-bold mt-2 mb-1 text-uppercase">{{ c.nome }}</h6>
            <p class="small text-muted mb-1">{{ c.rua }}, {{ c.numero }} - {{ c.bairro }} ({{ c.municipio }})</p>
            <div class="bg-light p-2 rounded small">
                <b>Ações:</b> {{ c.acoes | join(', ') }} <br>
                <b>Liderança:</b> {{ c.lideranca }}
            </div>
        </div>
        {% endfor %}
    </div>

    <button class="fab" data-bs-toggle="modal" data-bs-target="#mCad">+</button>

    <div class="modal fade" id="mEquipe" tabindex="-1">
        <div class="modal-dialog">
            <form action="/add_user" method="POST" class="modal-content">
                <div class="modal-header fw-bold">Novo Membro na Pirâmide</div>
                <div class="modal-body">
                    <label>Cargo:</label>
                    <select name="cargo" id="cSel" class="form-select mb-2" onchange="logic()" required>
                        <option value="">Selecione...</option>
                        {% if user.cargo == 'ADM' %}<option value="CANDIDATO">CANDIDATO</option>{% endif %}
                        <option value="COORDENADOR">COORDENADOR</option>
                        <option value="LIDERANÇA">LIDERANÇA</option>
                    </select>
                    <div id="dPol" style="display:none;">
                        <label>Posição Política:</label>
                        <select name="pos" id="pPol" class="form-select mb-2" onchange="logic()">
                            <option value="FEDERAL">DEP. FEDERAL</option>
                            <option value="ESTADUAL">DEP. ESTADUAL</option>
                            <option value="PREFEITO">PREFEITO</option>
                            <option value="VEREADOR">VEREADOR</option>
                        </select>
                    </div>
                    <div id="dMun" style="display:none;">
                        <label>Município:</label>
                        <select name="mun" class="form-select mb-2">
                            {% for m in munis %}<option value="{{m}}">{{m}}</option>{% endfor %}
                        </select>
                    </div>
                    <input type="text" name="nome" placeholder="Nome Completo" class="form-control mb-2" required>
                    <input type="text" name="login" placeholder="Login" class="form-control mb-2" required>
                    <input type="text" name="senha" placeholder="Senha" class="form-control mb-2" required>
                </div>
                <div class="modal-footer"><button class="btn btn-primary w-100">CADASTRAR</button></div>
            </form>
        </div>
    </div>

    <div class="modal fade" id="mCad" tabindex="-1">
        <div class="modal-dialog">
            <form action="/add_reg" method="POST" class="modal-content">
                <div class="modal-body">
                    <select name="tipo" class="form-select mb-2">
                        <option value="PESSOA">PESSOA</option>
                        <option value="FAMILIA">FAMÍLIA</option>
                    </select>
                    <input type="text" name="nome" placeholder="Nome Completo" class="form-control mb-2" required>
                    <div class="row g-1 mb-2">
                        <div class="col-8"><input type="text" name="rua" placeholder="Rua" class="form-control"></div>
                        <div class="col-4"><input type="text" name="numero" placeholder="Nº" class="form-control"></div>
                    </div>
                    <input type="text" name="bairro" placeholder="Bairro" class="form-control mb-3">
                    
                    <h6 class="fw-bold small">AÇÕES ADM/SAÚDE:</h6>
                    <div class="form-check"><input type="checkbox" name="acs" value="AÇÃO CIDADÃ"> Ação Cidadã</div>
                    <div class="form-check"><input type="checkbox" name="acs" value="NATAL SOLIDÁRIO"> Natal Solidário</div>
                    <div class="form-check"><input type="checkbox" name="acs" value="SAÚDE" onclick="document.getElementById('saude_d').style.display=this.checked?'block':'none'"> Saúde</div>
                    
                    <div id="saude_d" class="mt-2 p-2 bg-light rounded" style="display:none;">
                        <select name="s_tipo" class="form-select small">
                            <option value="Exame">Agendar Exame</option>
                            <option value="Cirurgia">Agendar Cirurgia</option>
                            <option value="UTI">Leito UTI</option>
                            <option value="Remedio">Medicamento</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer"><button class="btn btn-success w-100">SALVAR</button></div>
            </form>
        </div>
    </div>

    <div class="modal fade" id="mSenhas" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header"><b>Usuários Cadastrados</b></div>
                <div class="modal-body p-0">
                    <table class="table table-sm small">
                        <thead><tr class="table-dark"><th>Nome</th><th>Login/Senha</th><th>Cadastrado por</th></tr></thead>
                        <tbody>
                            {% for log, inf in equipe.items() %}
                            <tr>
                                <td>{{ inf.nome }}<br><small>{{ inf.cargo }}</small></td>
                                <td>{{ log }} / <b>{{ inf.senha }}</b></td>
                                <td>{{ inf.cad_por }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        function logic() {
            let c = document.getElementById('cSel').value;
            let p = document.getElementById('pPol').value;
            document.getElementById('dPol').style.display = (c === 'CANDIDATO') ? 'block' : 'none';
            let showM = (c === 'LIDERANÇA') || (c === 'CANDIDATO' && (p === 'PREFEITO' || p === 'VEREADOR'));
            document.getElementById('dMun').style.display = showM ? 'block' : 'none';
        }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        l, s = request.form.get('login').lower().strip(), request.form.get('senha')
        d = carregar()
        if l in d['usuarios'] and d['usuarios'][l]['senha'] == s:
            session['u'] = l
            session['u_d'] = d['usuarios'][l]
            return redirect(url_for('dash'))
    return render_template_string(HTML_LOGIN)

@app.route('/dash')
def dash():
    if 'u' not in session: return redirect(url_for('login'))
    d = carregar(); u = session['u_d']; l_u = session['u']
    
    if u['cargo'] == 'ADM':
        lista, equipe = d['cadastros'], d['usuarios']
    elif u['cargo'] == 'CANDIDATO':
        lista = [c for c in d['cadastros'] if c.get('pai') == l_u]
        equipe = {k:v for k,v in d['usuarios'].items() if v.get('pai') == l_u or k == l_u}
    else:
        lista = [c for c in d['cadastros'] if c.get('r_por') == l_u]
        equipe = {l_u: u}

    contas = {"FAMILIA": len([x for x in lista if x['tipo'] == 'FAMILIA']), "PESSOA": len([x for x in lista if x['tipo'] == 'PESSOA'])}
    return render_template_string(HTML_DASH, user=u, lista=lista, equipe=equipe, munis=MUNICIPIOS_PA, contas=contas)

@app.route('/add_user', methods=['POST'])
def add_user():
    d = carregar(); l_novo = request.form.get('login').lower().strip()
    pai = session['u'] if session['u_d']['cargo'] == 'CANDIDATO' else session['u_d'].get('pai')
    d['usuarios'][l_novo] = {
        "nome": request.form.get('nome'), "senha": request.form.get('senha'), "cargo": request.form.get('cargo'),
        "municipio": request.form.get('mun'), "pai": pai, "cad_por": session['u_d']['nome']
    }
    salvar(d); return redirect(url_for('dash'))

@app.route('/add_reg', methods=['POST'])
def add_reg():
    d = carregar(); u = session['u_d']
    novo = {
        "id": str(uuid.uuid4()), "tipo": request.form.get('tipo'), "nome": request.form.get('nome'),
        "rua": request.form.get('rua'), "numero": request.form.get('numero'), "bairro": request.form.get('bairro'),
        "municipio": u.get('municipio'), "lideranca": u['nome'], "r_por": session['u'],
        "pai": u.get('pai'), "acoes": request.form.getlist('acs'), "saude": request.form.get('s_tipo')
    }
    d['cadastros'].append(novo); salvar(d); return redirect(url_for('dash'))

@app.route('/excluir_reg/<rid>')
def excluir_reg(rid):
    d = carregar(); d['cadastros'] = [c for c in d['cadastros'] if c['id'] != rid]
    salvar(d); return redirect(url_for('dash'))

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))

if __name__ == "__main__": app.run(host='0.0.0.0', port=5000)
