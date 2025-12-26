from django.db import models
from django.conf import settings

class Auditoria(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta: abstract = True

class Familia(Auditoria):
    responsavel = models.CharField(max_length=255)
    municipio = models.ForeignKey('municipios.Municipio', on_delete=models.CASCADE)
    votos_estimados = models.IntegerField(default=1)
    necessidades = models.TextField(blank=True)
    def __str__(self): return self.responsavel

class AtendimentoSocial(Auditoria):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    concluido = models.BooleanField(default=False)

class Lideranca(Auditoria):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meta_votos = models.IntegerField(default=1000)
    regiao = models.CharField(max_length=100)
