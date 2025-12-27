import os, json, uuid, base64, re
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "junior_araujo_2026_premium_final_v5"

DB_FILE = "banco_dados.json"

# Listas de Configuração
CARGOS_POLITICOS = ["PRESIDENTE", "GOVERNADOR", "SENADOR", "DEPUTADO FEDERAL", "DEPUTADO ESTADUAL", "PREFEITO", "VEREADOR"]
MUNICIPIOS_PA = ["Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", "Altamira", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", "Baião", "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito", "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru", "Cachoeira do Arari", "Cachoeira do Piriá", "Caeté", "Canaã dos Carajás", "Capanema", "Capitão Poço", "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", "Cumaru do Norte", "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu", "Eldorado dos Carajás", "Faro", "Floresta do Araguaia", "Garrafão do Norte", "Goianésia do Pará", "Itaituba", "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Marabá", "Marituba", "Medicilândia", "Melgaço", "Mocajuba", "Moju", "Monte Alegre", "Muaná", "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Óbidos", "Oeiras do Pará", "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Paragominas", "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel", "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará", "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari", "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará", "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas", "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará", "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia", "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", "Soure", "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", "Tucumã", "Tucuruí", "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"]
OPCOES_SAUDE = ["Marcação de Exame", "Marcação de Consulta", "Marcação de Cirurgia", "Leito de UTI", "Medicamento", "Óculos", "Viagem para Consulta", "Buscar Alta Médica"]

# Funções de Banco de Dados
def carregar():
    if not os.path.exists(DB_FILE):
        d = {"usuarios": {"junior.araujo21": {"senha": "230808Deus#", "cargo": "ADM", "nome": "Júnior Araújo", "foto_b64": ""}}, "cadastros": [], "financeiro": []}
        salvar(d); return d
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def salvar(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)

def format_tel(v):
    v = re.sub(r'\D', '', v)
    if len(v) == 11: return f"({v[:2]}) {v[2:7]}-{v[7:]}"
    return v

# Estilização
CSS_STYLE = """
<style>
    :root { --laranja: #FF6600; --azul: #004AAD; --fundo: #F8F9FA; }
    body { background: var(--fundo); font-family: 'Segoe UI', sans-serif; margin-bottom: 90px; }
    .header-lux { background: white; border-bottom: 5px solid var(--laranja); padding: 25px 10px; text-align: center; border-radius: 0 0 35px 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .foto-perfil { width: 95px; height: 95px; border-radius: 20px; object-fit: contain; border: 2px solid var(--laranja); background: white; }
    .card-premium { background: white; border-radius: 20px; border: none; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 12px; border-left: 6px solid var(--laranja); }
    .btn-orange { background: var(--laranja); color: white; border-radius: 50px; font-weight: bold; border: none; padding: 14px; }
    .btn-blue { background: var(--azul); color: white; border-radius: 50px; font-weight: bold; border: none; padding: 14px; }
    .nav-bottom { position: fixed; bottom: 0; left: 0; right: 0; background: white; display: flex; justify-content: space-around; padding: 15px; border-top: 1px solid #ddd; z-index: 1000; }
    .nav-item { text-align: center; color: var(--azul); font-size: 11px; text-decoration: none; font-weight: bold; }
    .logo-login { max-width: 250px; width: 100%; height: auto; display: block; margin: 0 auto; filter: drop-shadow(0 5px 10px rgba(0,0,0,0.1)); }
</style>
"""

# Templates HTML
HTML_LOGIN = """
<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
""" + CSS_STYLE + """
</head>
<body class="bg-white d-flex align-items-center justify-content-center" style="height: 100vh;">
    <div style="width: 100%; max-width: 320px;" class="text-center">
        {% if adm_foto %}<img src="data:image/png;base64,{{ adm_foto }}" class="logo-login mb-4">
        {% else %}<h2 class="text-primary fw-bold mb-4">SISTEMA JÚNIOR ARAÚJO</h2>{% endif %}
        <form method="POST">
            <input type="text" name="login" class="form-control rounded-pill mb-2 p-3 bg-light border-0" placeholder="Usuário" required>
            <input type="password" name="senha" class="form-control rounded-pill mb-3 p-3 bg-light border-0" placeholder="Senha" required>
            <button class="btn btn-orange w-100 shadow">ENTRAR</button>
        </form>
    </div>
</body></html>
"""

HTML_DASH = """
<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
""" + CSS_STYLE + """
</head>
<body>
    <div class="header-lux mb-4">
        {% if user.foto_b64 %}<img src="data:image/png;base64,{{ user.foto_b64 }}" class="foto-perfil mb-2">
        {% else %}<i class="bi bi-person-circle text-muted" style="font-size: 50px;"></i>{% endif %}
        <h6 class="fw-bold mb-0 text-uppercase">{{ user.nome }}</h6>
        <span class="badge bg-light text-primary border small">{{ user.cargo }}</span>
    </div>

    <div class="container">
        <div class="row g-2 mb-4 text-center">
            <div class="col-6"><div class="bg-white p-3 rounded-4 shadow-sm"><b>{{ total_cadastros }}</b><br><small class="text-muted">CADASTROS</small></div></div>
            <div class="col-6"><div class="bg-white p-3 rounded-4 shadow-sm"><b>R$ {{ total_fin }}</b><br><small class="text-muted">DESPESAS</small></div></div>
        </div>

        <div class="d-grid gap-2 mb-4">
            <button class="btn btn-outline-primary rounded-pill fw-bold" data-bs-toggle="modal" data-bs-target="#mPerfil">MINHA FOTO</button>
            {% if user.cargo in ['ADM', 'CANDIDATO'] %}
                <button class="btn btn-blue shadow" data-bs-toggle="modal" data-bs-target="#mEquipe">CADASTRAR EQUIPE</button>
                <button class="btn btn-danger rounded-pill fw-bold" data-bs-toggle="modal" data-bs-target="#mFin">LANÇAR DESPESA</button>
            {% endif %}
            {% if user.cargo == 'ADM' %}
                <button class="btn btn-dark rounded-pill fw-bold" data-bs-toggle="modal" data-bs-target="#mSenhas">AUDITORIA DE SENHAS</button>
            {% endif %}
        </div>

        <h6 class="fw-bold text-muted mb-3"><i class="bi bi-bar-chart-fill"></i> DESEMPENHO POR MUNICÍPIO</h6>
        {% for mun, qtd in stats_mun.items() %}
            <div class="bg-white p-3 rounded-4 shadow-sm mb-2 d-flex justify-content-between align-items-center">
                <span class="fw-bold text-uppercase">{{ mun }}</span>
                <span class="badge bg-primary rounded-pill">{{ qtd }} ELEITORES</span>
            </div>
        {% endfor %}

        <hr>
        <h6 class="fw-bold text-muted mb-3">LISTA GERAL</h6>
        {% for c in lista %}
        <div class="card card-premium p-3">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h6 class="fw-bold text-primary mb-0">{{ c.nome }}</h6>
                    <small class="text-muted">Título: {{c.titulo}} (Z:{{c.zona}} S:{{c.secao}})</small>
                </div>
                <div class="d-flex">
                    <a href="/excluir_reg/{{c.id}}" class="text-danger ms-2" onclick="return confirm('Excluir?')"><i class="bi bi-trash-fill"></i></a>
                </div>
            </div>
            <p class="small mb-2 mt-2">
                <b>Tel:</b> {{c.contato}}<br>
                <i class="bi bi-geo-alt"></i> {{c.rua}}, {{c.numero}} - {{c.bairro}} ({{c.municipio}})<br>
                <span class="text-orange"><b>Por:</b> {{ c.nome_quem_cadastrou }}</span>
            </p>
            <div class="bg-light p-2 rounded small">
                <b>AÇÕES (ADM):</b>
                {% if user.cargo == 'ADM' %}<button class="btn btn-sm text-primary float-end p-0 fw-bold" data-bs-toggle="modal" data-bs-target="#mAcoes{{ loop.index }}">EDITAR</button>{% endif %}
                <div class="mt-2">{% for a in c.acoes %}<span class="badge bg-white text-dark border me-1">{{ a }}</span>{% endfor %}</div>
            </div>
        </div>

        <div class="modal fade" id="mAcoes{{ loop.index }}" tabindex="-1">
            <div class="modal-dialog"><form action="/update_acoes/{{c.id}}" method="POST" class="modal-content">
                <div class="modal-body">
                    <h6 class="fw-bold mb-3">MARCAR AÇÕES: {{ c.nome }}</h6>
                    <div class="form-check"><input class="form-check-input" type="checkbox" name="acs" value="AÇÃO CIDADÃ" {% if 'AÇÃO CIDADÃ' in c.acoes %}checked{% endif %}> AÇÃO CIDADÃ</div>
                    <div class="form-check"><input class="form-check-input" type="checkbox" name="acs" value="NATAL SOLIDÁRIO" {% if 'NATAL SOLIDÁRIO' in c.acoes %}checked{% endif %}> NATAL SOLIDÁRIO</div>
                    <hr><label class="fw-bold small">SAÚDE:</label>
                    {% for s_opt in opcoes_saude %}
                        <div class="form-check"><input class="form-check-input" type="checkbox" name="acs" value="SAÚDE: {{ s_opt }}" {% if 'SAÚDE: '~s_opt in c.acoes %}checked{% endif %}> {{ s_opt }}</div>
                    {% endfor %}
                    <button class="btn btn-orange w-100 mt-4">SALVAR ALTERAÇÕES</button>
                </div>
            </form></div>
        </div>
        {% endfor %}
    </div>

    <div class="modal fade" id="mPerfil" tabindex="-1">
        <div class="modal-dialog"><form action="/update_foto" method="POST" enctype="multipart/form-data" class="modal-content"><div class="modal-body text-center">
            <h6 class="fw-bold mb-3">ALTERAR MINHA FOTO</h6>
            <input type="file" name="foto" class="form-control mb-3" accept="image/*" required>
            <button class="btn btn-blue w-100">SALVAR FOTO</button>
        </div></form></div>
    </div>

    <div class="modal fade" id="mFin" tabindex="-1">
        <div class="modal-dialog"><form action="/add_fin" method="POST" class="modal-content"><div class="modal-body">
            <h6 class="fw-bold mb-3 text-center">LANÇAR DESPESA</h6>
            <input type="text" name="desc" placeholder="Descrição" class="form-control mb-2" required>
            <input type="number" step="0.01" name="valor" placeholder="Valor R$" class="form-control mb-3" required>
            <button class="btn btn-danger w-100 shadow">SALVAR NO CAIXA</button>
        </div></form></div>
    </div>

    <div class="modal fade" id="mSenhas" tabindex="-1">
        <div class="modal-dialog modal-fullscreen-sm-down"><div class="modal-content">
            <div class="modal-header fw-bold">USUÁRIOS E SENHAS</div>
            <div class="modal-body small">
                {% for login, u_info in todos_usuarios.items() %}
                    <div class="border-bottom py-2">
                        <b>{{ u_info.nome }}</b> ({{ u_info.cargo }})<br>
                        Login: {{ login }} | Senha: <b>{{ u_info.senha }}</b><br>
                        <small class="text-primary">Cadastrado por: {{ u_info.cad_por or 'ADM' }}</small>
                    </div>
                {% endfor %}
            </div>
        </div></div>
    </div>

    <div class="modal fade" id="mEquipe" tabindex="-1">
        <div class="modal-dialog"><form action="/add_user" method="POST" enctype="multipart/form-data" class="modal-content">
            <div class="modal-body">
                <h6 class="fw-bold text-center mb-3 text-primary">CADASTRAR EQUIPE</h6>
                <select name="cargo" id="cSel" class="form-select mb-2 rounded-pill" onchange="logic()" required>
                    <option value="">Cargo...</option>
                    {% if user.cargo == 'ADM' %}<option value="CANDIDATO">CANDIDATO</option>{% endif %}
                    <option value="COORDENADOR">COORDENADOR</option><option value="LIDERANÇA">LIDERANÇA</option>
                </select>
                <div id="dCand" style="display:none;" class="bg-light p-2 rounded mb-2">
                    <select name="pos" id="posSel" class="form-select mb-2" onchange="logic()">{% for cp in cargos %}<option value="{{ cp }}">{{ cp }}</option>{% endfor %}</select>
                </div>
                <div id="dMun" style="display:none;"><select name="mun" class="form-select mb-2">{% for m in munis %}<option value="{{ m }}">{{ m }}</option>{% endfor %}</select></div>
                <div id="dApoio" style="display:none;" class="border p-2 mb-2 rounded">
                    <label class="small fw-bold">Apoia quais Candidatos?</label>
                    <select name="apoios" class="form-select" multiple>
                        {% for log, uinfo in todos_usuarios.items() if uinfo.cargo == 'CANDIDATO' %}
                            <option value="{{ log }}">{{ uinfo.nome }} ({{ uinfo.posicao }})</option>
                        {% endfor %}
                    </select>
                </div>
                <input type="text" name="nome" placeholder="Nome" class="form-control mb-2 rounded-pill" required>
                <input type="text" name="login" placeholder="Login" class="form-control mb-2 rounded-pill" required>
                <input type="text" name="senha" placeholder="Senha" class="form-control mb-3 rounded-pill" required>
                <button class="btn btn-blue w-100">SALVAR</button>
            </div>
        </form></div>
    </div>

    <div class="modal fade" id="mCad" tabindex="-1">
        <div class="modal-dialog"><form action="/add_reg" method="POST" class="modal-content rounded-4">
            <div class="modal-body">
                <h5 class="fw-bold text-center text-primary mb-3">NOVO ELEITOR</h5>
                <input type="text" name="nome" placeholder="Nome Completo" class="form-control mb-2 rounded-pill" required>
                <input type="text" name="contato" placeholder="Contato (91) 98888-8888" class="form-control mb-2 rounded-pill" required>
                <div class="row g-1 mb-2">
                    <div class="col-6"><input type="text" name="titulo" placeholder="Título" class="form-control rounded-pill" required></div>
                    <div class="col-3"><input type="text" name="zona" placeholder="Z" class="form-control rounded-pill" required></div>
                    <div class="col-3"><input type="text" name="secao" placeholder="S" class="form-control rounded-pill" required></div>
                </div>
                <input type="text" name="rua" placeholder="Rua" class="form-control mb-2 rounded-pill">
                <div class="row g-1 mb-3"><div class="col-8"><input type="text" name="bairro" placeholder="Bairro" class="form-control rounded-pill"></div><div class="col-4"><input type="text" name="numero" placeholder="Nº" class="form-control rounded-pill"></div></div>
                <button class="btn btn-orange w-100 p-3 shadow">CADASTRAR</button>
            </div>
        </form></div>
    </div>

    <div class="nav-bottom">
        <a href="/dash" class="nav-item"><i class="bi bi-house-door-fill fs-3"></i><br>INÍCIO</a>
        <a href="#" class="nav-item" data-bs-toggle="modal" data-bs-target="#mCad"><i class="bi bi-person-plus-fill fs-3"></i><br>CADASTRAR</a>
        <a href="/logout" class="nav-item text-danger"><i class="bi bi-door-open-fill fs-3"></i><br>SAIR</a>
    </div>

    <script>
        function logic() {
            let c = document.getElementById('cSel').value;
            let p = document.getElementById('posSel').value;
            document.getElementById('dCand').style.display = (c === 'CANDIDATO') ? 'block' : 'none';
            document.getElementById('dApoio').style.display = (c === 'LIDERANÇA' || c === 'COORDENADOR') ? 'block' : 'none';
            document.getElementById('dMun').style.display = (c === 'LIDERANÇA' || (c === 'CANDIDATO' && (p === 'PREFEITO' || p === 'VEREADOR'))) ? 'block' : 'none';
        }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body></html>
"""

# Rotas Backend
@app.route('/', methods=['GET', 'POST'])
def login():
    d = carregar()
    if request.method == 'POST':
        l, s = request.form.get('login').lower().strip(), request.form.get('senha')
        if l in d['usuarios'] and d['usuarios'][l]['senha'] == s:
            session['u'] = l
            return redirect(url_for('dash'))
    return render_template_string(HTML_LOGIN, adm_foto=d['usuarios']['junior.araujo21'].get('foto_b64'))

@app.route('/dash')
def dash():
    if 'u' not in session: return redirect(url_for('login'))
    d = carregar(); u = d['usuarios'][session['u']]
    meu_login = session['u']
    
    if u['cargo'] == 'ADM':
        lista = d['cadastros']
    elif u['cargo'] == 'CANDIDATO':
        # Candidato vê o dele + o de quem o apoia
        lista = [c for c in d['cadastros'] if c['pai'] == meu_login or meu_login in d['usuarios'].get(c['r_por'], {}).get('apoios', [])]
    else:
        lista = [c for c in d['cadastros'] if c['r_por'] == meu_login]

    stats_mun = {}
    for c in lista: stats_mun[c['municipio']] = stats_mun.get(c['municipio'], 0) + 1
    
    total_fin = sum(float(f['valor']) for f in d['financeiro'] if u['cargo'] == 'ADM' or f['quem'] == meu_login)
    return render_template_string(HTML_DASH, user=u, lista=lista, stats_mun=stats_mun, 
                                  todos_usuarios=d['usuarios'], munis=MUNICIPIOS_PA, 
                                  cargos=CARGOS_POLITICOS, total_cadastros=len(lista), 
                                  total_fin=f"{total_fin:,.2f}", opcoes_saude=OPCOES_SAUDE)

@app.route('/update_foto', methods=['POST'])
def update_foto():
    d = carregar(); f = request.files['foto']
    if f: d['usuarios'][session['u']]['foto_b64'] = base64.b64encode(f.read()).decode('utf-8')
    salvar(d); return redirect(url_for('dash'))

@app.route('/add_user', methods=['POST'])
def add_user():
    d = carregar(); l_n = request.form.get('login').lower().strip()
    d['usuarios'][l_n] = {
        "nome": request.form.get('nome'), "senha": request.form.get('senha'), "cargo": request.form.get('cargo'),
        "pai": session['u'], "cad_por": d['usuarios'][session['u']]['nome'], "posicao": request.form.get('pos'),
        "municipio": request.form.get('mun'), "foto_b64": "", "apoios": request.form.getlist('apoios')
    }
    salvar(d); return redirect(url_for('dash'))

@app.route('/add_reg', methods=['POST'])
def add_reg():
    d = carregar(); u = d['usuarios'][session['u']]
    novo = {
        "id": str(uuid.uuid4()), "nome": request.form.get('nome'), "contato": format_tel(request.form.get('contato')),
        "titulo": request.form.get('titulo'), "zona": request.form.get('zona'), "secao": request.form.get('secao'),
        "rua": request.form.get('rua'), "numero": request.form.get('numero'), "bairro": request.form.get('bairro'),
        "municipio": u.get('municipio') or 'Pará', "r_por": session['u'], "nome_quem_cadastrou": u['nome'],
        "pai": u.get('pai') or session['u'], "acoes": []
    }
    d['cadastros'].append(novo); salvar(d); return redirect(url_for('dash'))

@app.route('/update_acoes/<rid>', methods=['POST'])
def update_acoes(rid):
    d = carregar()
    if d['usuarios'][session['u']]['cargo'] != 'ADM': return redirect(url_for('dash'))
    selecionadas = request.form.getlist('acs')
    for c in d['cadastros']:
        if c['id'] == rid: c['acoes'] = selecionadas
    salvar(d); return redirect(url_for('dash'))

@app.route('/add_fin', methods=['POST'])
def add_fin():
    d = carregar()
    d['financeiro'].append({"desc": request.form.get('desc'), "valor": request.form.get('valor'), "quem": session['u']})
    salvar(d); return redirect(url_for('dash'))

@app.route('/excluir_reg/<rid>')
def excluir_reg(rid):
    d = carregar()
    d['cadastros'] = [c for c in d['cadastros'] if c['id'] != rid]
    salvar(d); return redirect(url_for('dash'))

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
