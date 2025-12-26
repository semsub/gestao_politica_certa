from django.db import models
from municipios.models import Municipio

class Lideranca(models.Model):
    NIVEL_CHOICES = [('A', 'Influência Alta'), ('B', 'Influência Média'), ('C', 'Influência Local')]
    
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Município Base")
    telefone = models.CharField(max_length=20, verbose_name="WhatsApp")
    meta_votos = models.IntegerField(default=0, verbose_name="Meta de Votos")
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, default='C', verbose_name="Nível")
    biografia = models.TextField(blank=True, verbose_name="Dossiê Político")

    class Meta:
        verbose_name = "Liderança"
        verbose_name_plural = "Lideranças"

    def __str__(self):
        return self.nome

class AtendimentoSocial(models.Model):
    lideranca = models.ForeignKey(Lideranca, on_delete=models.CASCADE, verbose_name="Solicitado por")
    pedido = models.TextField(verbose_name="Descrição do Pedido")
    status = models.CharField(max_length=20, choices=[('P', 'Pendente'), ('E', 'Em Andamento'), ('C', 'Concluído')], default='P')

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
