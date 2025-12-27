import os, json, uuid
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "junior_araujo_2026_final_v1"

DB_FILE = "banco_dados.json"

# Configurações de Memória
CARGOS_POLITICOS = ["PRESIDENTE", "VICE-PRESIDENTE", "GOVERNADOR", "VICE-GOVERNADOR", "SENADOR", "DEPUTADO FEDERAL", "DEPUTADO ESTADUAL", "DEPUTADO DISTRITAL", "PREFEITO", "VICE-PREFEITO", "VEREADOR"]
MUNICIPIOS_PA = ["Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", "Altamira", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", "Baião", "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito", "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru", "Cachoeira do Arari", "Cachoeira do Piriá", "Caeté", "Canaã dos Carajás", "Capanema", "Capitão Poço", "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", "Cumaru do Norte", "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu", "Eldorado dos Carajás", "Faro", "Floresta do Araguaia", "Garrafão do Norte", "Goianésia do Pará", "Itaituba", "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Marabá", "Marituba", "Medicilândia", "Melgaço", "Mocajuba", "Moju", "Monte Alegre", "Muaná", "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Óbidos", "Oeiras do Pará", "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Paragominas", "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel", "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará", "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari", "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará", "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas", "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará", "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia", "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", "Soure", "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", "Tucumã", "Tucuruí", "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"]

def carregar():
    if not os.path.exists(DB_FILE):
        d = {"usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo": "ADM", "nome": "Júnior Araújo", "municipio": "Salinópolis"}}, "cadastros": []}
        salvar(d); return d
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def salvar(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)

HTML_LOGIN = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Login GP 2026</title>
</head>
<body class="bg-light d-flex align-items-center justify-content-center" style="height: 100vh;">
    <div class="card p-4 shadow-sm" style="width: 100%; max-width: 350px;">
        <h4 class="text-center fw-bold text-primary mb-4">GP 2026</h4>
        <form method="POST">
            <input type="text" name="login" class="form-control mb-2" placeholder="Usuário" required>
            <input type="password" name="senha" class="form-control mb-3" placeholder="Senha" required>
            <button class="btn btn-primary w-100">ACESSAR</button>
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
        body { background: #f4f6f9; font-size: 14px; }
        .nav-app { background: #0d6efd; color: white; padding: 15px; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; }
        .reg-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
</head>
<body>
    <div class="nav-app shadow mb-3">
        <div class="container d-flex justify-content-between align-items-center">
            <span><b>{{ user.nome }}</b><br><small>{{ user.cargo }}</small></span>
            <a href="/logout" class="btn btn-sm btn-light">Sair</a>
        </div>
        <div class="row text-center mt-3">
            <div class="col-4"><b>{{ contas.FAMILIA }}</b><br><small>FAMÍLIAS</small></div>
            <div class="col-4"><b>{{ contas.PESSOA }}</b><br><small>PESSOAS</small></div>
            <div class="col-4"><b>{{ contas.EQUIPE }}</b><br><small>EQUIPE</small></div>
        </div>
    </div>

    <div class="container pb-5">
        {% if user.cargo in ['ADM', 'CANDIDATO'] %}
        <div class="d-grid gap-2 mb-4">
            <button class="btn btn-dark fw-bold" data-bs-toggle="modal" data-bs-target="#mEquipe">GERENCIAR HIERARQUIA</button>
            <button class="btn btn-info text-white fw-bold" data-bs-toggle="modal" data-bs-target="#mSenhas">USUÁRIOS E SENHAS</button>
        </div>
        {% endif %}

        <h6 class="fw-bold text-muted mb-3"><i class="bi bi-list"></i> REGISTROS DA HIERARQUIA</h6>
        {% for c in lista %}
        <div class="reg-card">
            <div class="d-flex justify-content-between">
                <span class="badge bg-primary mb-2">{{ c.tipo }}</span>
                <a href="/excluir_reg/{{c.id}}" class="text-danger" onclick="return confirm('Excluir?')"><i class="bi bi-trash"></i></a>
            </div>
            <h6 class="fw-bold mb-1">{{ c.nome }}</h6>
            <p class="small text-muted mb-1">
                <i class="bi bi-card-checklist"></i> Título: {{c.titulo}} | Z: {{c.zona}} | S: {{c.secao}}<br>
                <i class="bi bi-geo-alt"></i> {{c.rua}}, {{c.numero}} - {{c.bairro}}<br>
                <span class="text-primary fw-bold"><i class="bi bi-person-plus"></i> Cadastrado por: {{ c.nome_quem_cadastrou }}</span>
            </p>
            <div class="bg-light p-2 rounded small mt-2">
                <b>AÇÕES (ADM):</b> 
                {% if user.cargo == 'ADM' %}<button class="btn btn-sm p-0 text-primary float-end fw-bold" data-bs-toggle="modal" data-bs-target="#mAcao{{ loop.index }}">+ AÇÃO</button>{% endif %}
                <br>
                {% for a in c.acoes %}<span class="badge bg-white text-dark border me-1">{{ a }}</span>{% endfor %}
            </div>
        </div>

        <div class="modal fade" id="mAcao{{ loop.index }}" tabindex="-1">
            <div class="modal-dialog">
                <form action="/add_acao/{{c.id}}" method="POST" class="modal-content">
                    <div class="modal-body">
                        <select name="tipo_acao" class="form-select mb-2" onchange="this.nextElementSibling.style.display=(this.value=='SAÚDE'?'block':'none')">
                            <option value="AÇÃO CIDADÃ">AÇÃO CIDADÃ</option>
                            <option value="NATAL SOLIDÁRIO">NATAL SOLIDÁRIO</option>
                            <option value="SAÚDE">SAÚDE</option>
                        </select>
                        <select name="saude_detalhe" class="form-select mb-2" style="display:none;">
                            <option value="Exame">Exame</option><option value="Consulta">Consulta</option><option value="Cirurgia">Cirurgia</option><option value="UTI">UTI</option><option value="Medicamento">Medicamento</option><option value="Óculos">Óculos</option><option value="Viagem">Viagem</option><option value="Alta">Alta Médica</option>
                        </select>
                    </div>
                    <div class="modal-footer"><button class="btn btn-primary w-100">SALVAR</button></div>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>

    <button style="position:fixed; bottom:20px; right:20px; width:60px; height:60px; border-radius:50%; background:#198754; color:white; border:none; font-size:30px; box-shadow:0 4px 10px rgba(0,0,0,0.3);" data-bs-toggle="modal" data-bs-target="#mCad">+</button>

    <div class="modal fade" id="mCad" tabindex="-1">
        <div class="modal-dialog">
            <form action="/add_reg" method="POST" class="modal-content">
                <div class="modal-body">
                    <select name="tipo" class="form-select mb-2"><option value="PESSOA">PESSOA</option><option value="FAMILIA">FAMÍLIA</option></select>
                    <input type="text" name="nome" placeholder="Nome Completo" class="form-control mb-2" required>
                    <div class="row g-1 mb-2">
                        <div class="col-6"><input type="text" name="titulo" placeholder="Título Eleitoral" class="form-control" required></div>
                        <div class="col-3"><input type="text" name="zona" placeholder="Zona" class="form-control" required></div>
                        <div class="col-3"><input type="text" name="secao" placeholder="Seção" class="form-control" required></div>
                    </div>
                    <input type="text" name="rua" placeholder="Rua" class="form-control mb-2">
                    <div class="row g-1 mb-2"><div class="col-8"><input type="text" name="bairro" placeholder="Bairro" class="form-control"></div><div class="col-4"><input type="text" name="numero" placeholder="Nº" class="form-control"></div></div>
                </div>
                <div class="modal-footer"><button class="btn btn-success w-100">SALVAR</button></div>
            </form>
        </div>
    </div>

    <div class="modal fade" id="mEquipe" tabindex="-1">
        <div class="modal-dialog">
            <form action="/add_user" method="POST" class="modal-content">
                <div class="modal-body">
                    <select name="cargo" id="cSel" class="form-select mb-2" onchange="logic()" required>
                        <option value="">Cargo...</option>
                        {% if user.cargo == 'ADM' %}<option value="CANDIDATO">CANDIDATO</option>{% endif %}
                        <option value="COORDENADOR">COORDENADOR</option><option value="LIDERANÇA">LIDERANÇA</option>
                    </select>
                    <div id="dPol" style="display:none;"><select name="pos" class="form-select mb-2">{% for cp in cargos %}<option value="{{cp}}">{{cp}}</option>{% endfor %}</select></div>
                    <div id="dMun" style="display:none;"><select name="mun" class="form-select mb-2">{% for m in munis %}<option value="{{m}}">{{m}}</option>{% endfor %}</select></div>
                    <input type="text" name="nome" placeholder="Nome" class="form-control mb-2" required>
                    <input type="text" name="login" placeholder="Login" class="form-control mb-2" required>
                    <input type="text" name="senha" placeholder="Senha" class="form-control mb-2" required>
                </div>
                <div class="modal-footer"><button class="btn btn-primary w-100">CADASTRAR</button></div>
            </form>
        </div>
    </div>

    <div class="modal fade" id="mSenhas" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-body p-0">
                    <table class="table table-sm small mb-0">
                        <thead class="table-dark"><tr><th>Nome</th><th>Login/Senha</th><th>Cadastrado por</th></tr></thead>
                        <tbody>{% for log, inf in equipe.items() %}<tr><td>{{ inf.nome }}<br><small>{{ inf.cargo }}</small></td><td>{{ log }} / <b>{{ inf.senha }}</b></td><td>{{ inf.cad_por }}</td></tr>{% endfor %}</tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        function logic() {
            let c = document.getElementById('cSel').value;
            document.getElementById('dPol').style.display = (c === 'CANDIDATO') ? 'block' : 'none';
            document.getElementById('dMun').style.display = (c === 'LIDERANÇA' || c === 'CANDIDATO') ? 'block' : 'none';
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
            session['u'], session['u_d'] = l, d['usuarios'][l]
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

    contas = {"FAMILIA": len([x for x in lista if x['tipo'] == 'FAMILIA']), "PESSOA": len([x for x in lista if x['tipo'] == 'PESSOA']), "EQUIPE": len(equipe)}
    return render_template_string(HTML_DASH, user=u, lista=lista, equipe=equipe, munis=MUNICIPIOS_PA, cargos=CARGOS_POLITICOS, contas=contas)

@app.route('/add_user', methods=['POST'])
def add_user():
    d = carregar(); l_n = request.form.get('login').lower().strip()
    pai = session['u'] if session['u_d']['cargo'] == 'CANDIDATO' else session['u_d'].get('pai')
    d['usuarios'][l_n] = {"nome": request.form.get('nome'), "senha": request.form.get('senha'), "cargo": request.form.get('cargo'), "pai": pai, "cad_por": session['u_d']['nome']}
    salvar(d); return redirect(url_for('dash'))

@app.route('/add_reg', methods=['POST'])
def add_reg():
    d = carregar(); u = session['u_d']
    novo = {
        "id": str(uuid.uuid4()), "tipo": request.form.get('tipo'), "nome": request.form.get('nome'),
        "titulo": request.form.get('titulo'), "zona": request.form.get('zona'), "secao": request.form.get('secao'),
        "rua": request.form.get('rua'), "numero": request.form.get('numero'), "bairro": request.form.get('bairro'),
        "municipio": u.get('municipio'), "r_por": session['u'], "nome_quem_cadastrou": u['nome'], # AQUI O DETALHE PEDIDO
        "pai": u.get('pai'), "acoes": []
    }
    d['cadastros'].append(novo); salvar(d); return redirect(url_for('dash'))

@app.route('/add_acao/<rid>', methods=['POST'])
def add_acao(rid):
    if session['u_d']['cargo'] != 'ADM': return redirect(url_for('dash'))
    d = carregar(); tipo = request.form.get('tipo_acao')
    if tipo == 'SAÚDE': tipo = f"SAÚDE: {request.form.get('saude_detalhe')}"
    for c in d['cadastros']:
        if c['id'] == rid: c['acoes'].append(tipo)
    salvar(d); return redirect(url_for('dash'))

@app.route('/excluir_reg/<rid>')
def excluir_reg(rid):
    d = carregar(); d['cadastros'] = [c for c in d['cadastros'] if c['id'] != rid]
    salvar(d); return redirect(url_for('dash'))

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))

if __name__ == "__main__": app.run(host='0.0.0.0', port=5000)
