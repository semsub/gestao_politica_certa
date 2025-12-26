from django.db import models

class Municipio(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, default='PA')

    def __str__(self):
        return f"{self.nome} - {self.estado}"
