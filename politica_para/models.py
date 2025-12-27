from django.db import models

class Obra(models.Model):
    TIPOS = [('INFRA', 'Infraestrutura'), ('SAUDE', 'Saúde'), ('EDUC', 'Educação')]
    titulo = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    percentual = models.IntegerField(default=0)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f"{self.titulo} - {self.municipio}"

class AlertaSeguranca(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    vulneravel = models.CharField(max_length=100) # Ex: Produtor Rural
