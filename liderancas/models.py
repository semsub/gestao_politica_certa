from django.db import models
from django.conf import settings

class Auditoria(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta: abstract = True

class Familia(Auditoria):
    responsavel = models.CharField(max_length=255)
    municipio = models.ForeignKey('municipios.Municipio', on_delete=models.CASCADE)
    endereco = models.CharField(max_length=255)
    contato = models.CharField(max_length=50)
    votos_estimados = models.IntegerField(default=1)
    necessidades = models.TextField(blank=True, verbose_name="Demandas da Família")

    def __str__(self): return f"{self.responsavel} - {self.municipio}"

class AtendimentoSocial(Auditoria):
    TIPO_CHOICES = [('SAUDE', 'Saúde/Exame'), ('CESTA', 'Cesta Básica'), ('JURIDICO', 'Apoio Jurídico')]
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='atendimentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    concluido = models.BooleanField(default=False)
