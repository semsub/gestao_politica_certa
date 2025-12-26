from django.db import models
from municipios.models import Municipio

class Lideranca(models.Model):
    NIVEIS = [('A', 'Influência Alta'), ('B', 'Média'), ('C', 'Local')]
    
    nome = models.CharField(max_length=200, verbose_name="Nome da Liderança")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Cidade Base")
    telefone = models.CharField(max_length=20, verbose_name="WhatsApp")
    meta_votos = models.PositiveIntegerField(default=0, verbose_name="Meta de Votos")
    nivel = models.CharField(max_length=1, choices=NIVEIS, default='C', verbose_name="Nível")

    class Meta:
        verbose_name = "Liderança"
        verbose_name_plural = "Lideranças"

    def __str__(self):
        return self.nome

class AtendimentoSocial(models.Model):
    lideranca = models.ForeignKey(Lideranca, on_delete=models.CASCADE)
    demanda = models.TextField(verbose_name="Descrição do Pedido")
    data_solicitacao = models.DateField(auto_now_add=True)
    concluido = models.BooleanField(default=False, verbose_name="Resolvido?")

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
