from .models import Assinatura

def pode_usar(campanha, recurso):
    try:
        assinatura = Assinatura.objects.get(campanha=campanha, ativa=True)
        return getattr(assinatura.plano, recurso, False)
    except Assinatura.DoesNotExist:
        return False
