import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from liderancas.models import RegiaoIntegracao, CategoriaAcao, Lideranca
from municipios.models import Municipio
from django.contrib.auth import get_user_model

User = get_user_model()

def carga_final():
    print("Injetando inteligência geográfica do Pará...")
    reg, _ = RegiaoIntegracao.objects.get_or_create(nome="METROPOLITANA")
    muni, _ = Municipio.objects.get_or_create(nome="BELÉM", defaults={'estado':'PA', 'regiao':reg})
    CategoriaAcao.objects.get_or_create(nome="Voto Confirmado", icone="check-bold")
    
    user = User.objects.get(email="junior.araujo21@yahoo.com.br")
    Lideranca.objects.get_or_create(usuario=user, defaults={'municipio':muni, 'regiao':reg})
    print("✅ TUDO PRONTO PARA VENDA!")

if __name__ == "__main__":
    carga_final()
