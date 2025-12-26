from django.db import models
from municipios.models import Municipio

class Lideranca(models.Model):
    NIVEL_CHOICES = [('A', 'Influência Alta'), ('B', 'Média'), ('C', 'Local')]
    
    nome = models.CharField(max_length=200, verbose_name="Nome da Liderança")
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, verbose_name="Cidade Base")
    telefone = models.CharField(max_length=25, verbose_name="WhatsApp")
    meta_votos = models.PositiveIntegerField(default=0, verbose_name="Meta de Votos")
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, default='C', verbose_name="Nível")

    class Meta:
        verbose_name = "Liderança"
        verbose_name_plural = "Lideranças"

    def __str__(self):
        return f"{self.nome} - {self.municipio.nome}"

class AtendimentoSocial(models.Model):
    lideranca = models.ForeignKey(Lideranca, on_delete=models.CASCADE, verbose_name="Liderança")
    demanda = models.TextField(verbose_name="Pedido")
    concluido = models.BooleanField(default=False, verbose_name="Atendido?")

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
