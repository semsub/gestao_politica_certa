import sys
import os
import json

# --- CONFIGURAÇÕES DE CORES ---
AZUL = '\033[94m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
VERMELHO = '\033[91m'
RESET = '\033[0m'

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

CARGOS_POLITICOS = ["DEPUTADO ESTADUAL", "DEPUTADO FEDERAL", "SENADOR", "GOVERNADOR", "PREFEITO", "VEREADOR"]
COORDENACOES = ["COORDENAÇÃO GERAL", "MARKETING", "FINANCEIRO", "LIDERANÇAS"]

class SistemaPolitico:
    def __init__(self):
        self.arquivo_dados = "banco_dados.json"
        self.usuarios = {
            "junior.araujo21": {"senha": "230808Deus#", "cargo_sistema": "CRIADOR", "nome": "Júnior Araújo"}
        }
        self.liderancas_info = {} 
        self.base_eleitores = []   
        self.sessao = None
        self.carregar_dados()

    def salvar_dados(self):
        dados = {
            "usuarios": self.usuarios,
            "liderancas": self.liderancas_info,
            "eleitores": self.base_eleitores
        }
        with open(self.arquivo_dados, 'w') as f:
            json.dump(dados, f, indent=4)

    def carregar_dados(self):
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'r') as f:
                dados = json.load(f)
                self.usuarios = dados.get("usuarios", self.usuarios)
                self.liderancas_info = dados.get("liderancas", {})
                self.base_eleitores = dados.get("eleitores", [])

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def login(self):
        self.limpar_tela()
        print(f"{AZUL}=================================================={RESET}")
        print(f"{AZUL}    SISTEMA DE GESTÃO POLÍTICA - ESTADO DO PARÁ   {RESET}")
        print(f"{AZUL}=================================================={RESET}")
        user = input("Login: ")
        senha = input("Senha: ")
        
        if user in self.usuarios and self.usuarios[user]["senha"] == senha:
            self.sessao = self.usuarios[user]
            self.sessao["id_login"] = user
            return True
        print(f"{VERMELHO}Acesso Negado.{RESET}")
        input("Pressione Enter...")
        return False

    def cadastrar_candidato(self):
        self.limpar_tela()
        print(f"{VERDE}--- CADASTRO DE CANDIDATO ---{RESET}")
        login = input("Login: ")
        senha = input("Senha: ")
        nome = input("Nome do Candidato: ")
        print("\nCargos:")
        for i, cargo in enumerate(CARGOS_POLITICOS): print(f"{i}. {cargo}")
        c_idx = int(input("Opção: "))
        
        self.usuarios[login] = {
            "senha": senha, "cargo_sistema": "CANDIDATO", 
            "nome": nome, "cargo_politico": CARGOS_POLITICOS[c_idx]
        }
        self.salvar_dados()
        print(f"\n{VERDE}Candidato Salvo!{RESET}")
        input("Enter...")

    def cadastrar_hierarquia(self):
        self.limpar_tela()
        print(f"{AMARELO}--- CADASTRAR HIERARQUIA ---{RESET}")
        print("1. COORDENADOR | 2. LIDERANÇA")
        tipo = input("Escolha: ")
        login = input("Login: ")
        senha = input("Senha: ")
        nome = input("Nome Completo: ")

        if tipo == "1":
            for i, c in enumerate(COORDENACOES): print(f"{i}. {c}")
            setor = COORDENACOES[int(input("Setor: "))]
            self.usuarios[login] = {"senha": senha, "cargo_sistema": "COORDENADOR", "nome": nome, "setor": setor}
        else:
            mun = input("Município (Ex: Salinópolis): ")
            contato = input("WhatsApp: ")
            self.usuarios[login] = {"senha": senha, "cargo_sistema": "LIDERANCA", "nome": nome}
            self.liderancas_info[login] = {
                "nome": nome, "municipio": mun, "contato": contato, "base": []
            }
        self.salvar_dados()
        print(f"\n{VERDE}Membro Cadastrado!{RESET}")
        input("Enter...")

    def cadastrar_base(self):
        self.limpar_tela()
        if self.sessao["cargo_sistema"] != "LIDERANCA":
            print(f"{VERMELHO}ERRO: Apenas LIDERANÇAS podem cadastrar eleitores.{RESET}")
            print("Se você é o Criador ou Candidato, crie uma Liderança e entre com o login dela.")
            input("\nEnter para continuar...")
            return

        print(f"{VERDE}--- CADASTRAR PESSOA NA BASE ---{RESET}")
        nome = input("Nome Completo: ")
        titulo = input("Nº do Título Eleitoral: ")
        zona = input("Zona: ")
        secao = input("Seção: ")
        contato = input("WhatsApp: ")
        
        dados = {
            "nome": nome, 
            "titulo": titulo, 
            "zona": zona, 
            "secao": secao, 
            "contato": contato, 
            "lideranca": self.sessao["nome"],
            "municipio": self.liderancas_info[self.sessao["id_login"]]["municipio"]
        }
        
        self.liderancas_info[self.sessao["id_login"]]["base"].append(dados)
        self.base_eleitores.append(dados)
        self.salvar_dados()
        print(f"\n{VERDE}Pessoa {nome} adicionada com sucesso!{RESET}")
        input("Enter...")

    def dashboard(self):
        self.limpar_tela()
        print(f"{AZUL}=================================================={RESET}")
        print(f"      DASHBOARD GERAL - TOTAL: {len(self.base_eleitores)}")
        print(f"{AZUL}=================================================={RESET}")
        
        for lid_id, info in self.liderancas_info.items():
            print(f"MUNICÍPIO: {info['municipio']:<15} | LÍDER: {info['nome']:<15} | TOTAL: {len(info['base'])}")
        
        print("\n--- LISTAGEM DETALHADA ---")
        for e in self.base_eleitores:
            print(f"Nome: {e['nome']} | T: {e['titulo']} Z: {e['zona']} S: {e['secao']} | Mun: {e['municipio']}")
            
        input("\nEnter para voltar...")

    def menu(self):
        while True:
            if not self.sessao:
                if not self.login(): continue
            self.limpar_tela()
            print(f"{AMARELO}USUÁRIO: {self.sessao['nome']} | CARGO: {self.sessao['cargo_sistema']}{RESET}")
            print("-" * 50)
            
            if self.sessao["cargo_sistema"] == "CRIADOR":
                print("1. Cadastrar Candidato")
            
            if self.sessao["cargo_sistema"] in ["CANDIDATO", "COORDENADOR"]:
                print("2. Cadastrar Coordenador ou Liderança")
                print("3. Dashboard e Relatórios")
            
            if self.sessao["cargo_sistema"] == "LIDERANCA":
                print("4. Cadastrar Eleitor na sua Base")
                print("5. Ver Minha Lista")

            print("L. Logout")
            print("S. Sair")
            
            op = input("\nOpção: ").upper()
            
            if op == "1" and self.sessao["cargo_sistema"] == "CRIADOR": self.cadastrar_candidato()
            elif op == "2" and self.sessao["cargo_sistema"] in ["CANDIDATO", "COORDENADOR"]: self.cadastrar_hierarquia()
            elif op == "3": self.dashboard()
            elif op == "4": self.cadastrar_base()
            elif op == "5" and self.sessao["cargo_sistema"] == "LIDERANCA":
                self.limpar_tela()
                for p in self.liderancas_info[self.sessao["id_login"]]["base"]:
                    print(f"- {p['nome']} | Título: {p['titulo']} Zona: {p['zona']} Seção: {p['secao']}")
                input("\nEnter para continuar...")
            elif op == "L": self.sessao = None
            elif op == "S": sys.exit()

if __name__ == "__main__":
    app = SistemaPolitico()
    app.menu()
