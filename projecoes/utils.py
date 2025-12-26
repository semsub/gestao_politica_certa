from liderancas.models import Lideranca
def calcular_votos(campanha):
    liderancas = Lideranca.objects.filter(campanha=campanha)
    total = sum(l.votos_estimados for l in liderancas)
    return total
