from django.shortcuts import render
from .models import Pagamento
from .pix import gerar_pix

CHAVE_PIX = "SEU_PIX_AQUI"

def pagar(request, campanha_id, valor):
    pagamento = Pagamento.objects.create(
        campanha_id=campanha_id,
        valor=valor,
        chave_pix=CHAVE_PIX
    )
    pix = gerar_pix(valor, CHAVE_PIX)
    return render(request, "pagamentos/pagar.html", {"pix": pix})
