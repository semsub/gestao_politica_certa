import requests
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

# IP Local para testes, mudar para o IP do servidor na produção
BASE_URL = "http://127.0.0.1:8000"

class LoginScreen(Screen):
    def logar(self):
        # Chave 'email' agora casa perfeitamente com o Serializer acima
        payload = {
            "email": "junior.araujo21@yahoo.com.br",
            "password": "230808Deus#"
        }
        
        try:
            res = requests.post(f"{BASE_URL}/api/login/", json=payload, timeout=10)
            
            if res.status_code == 200:
                MDApp.get_running_app().token = res.json()['access']
                print("✅ ACESSO AO COMANDO AUTORIZADO")
                self.manager.current = 'dashboard'
            else:
                print(f"❌ Falha: {res.status_code} - {res.text}")
                self.ids.error.text = "E-mail ou Senha incorretos."
        except Exception as e:
            print(f"⚠️ Erro de conexão: {e}")
            self.ids.error.text = "Servidor de Campanha Offline"

class DashboardScreen(Screen):
    def capturar_voto(self):
        app = MDApp.get_running_app()
        # Captura simulada de GPS em Belém/PA
        data = {
            "eleitor_nome": "Novo Apoiador PA",
            "latitude": -1.4558,
            "longitude": -48.4902,
            "descricao": "Base Belém - Captura via App",
            "categoria": 1 
        }
        headers = {"Authorization": f"Bearer {app.token}"}
        
        try:
            res = requests.post(f"{BASE_URL}/api/v1/sincronizar/", json=data, headers=headers)
            if res.status_code == 201:
                print("🔥 Voto sincronizado no Mapa de Calor!")
            else:
                print(f"Erro na sincronia: {res.status_code}")
        except:
            print("Offline: Voto registrado no cache do celular.")

class PoliticaApp(MDApp):
    token = None
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file('main.kv')

if __name__ == "__main__":
    PoliticaApp().run()
