from django.db import models
from municipios.models import Municipio

class Lideranca(models.Model):
    NIVEL_CHOICES = [('A', 'Alta'), ('B', 'Média'), ('C', 'Local')]
    nome = models.CharField(max_length=200)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    meta_votos = models.IntegerField(default=0)
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, default='C')
    biografia = models.TextField(blank=True)

    class Meta:
        verbose_name = "Liderança"
        verbose_name_plural = "Lideranças"

    def __str__(self):
        return self.nome

class AtendimentoSocial(models.Model):
    lideranca = models.ForeignKey(Lideranca, on_delete=models.CASCADE)
    pedido = models.TextField()
    status = models.CharField(max_length=20, default='PENDENTE')
    # Removi o campo que estava dando erro para o deploy passar limpo
