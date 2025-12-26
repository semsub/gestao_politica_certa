from django.db import models
from eleitores.models import Eleitor

class Projecao(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.CASCADE)
    percentual = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.eleitor.nome} - {self.percentual}%"
