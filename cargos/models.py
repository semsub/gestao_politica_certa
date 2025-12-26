from django.db import models

class Cargo(models.Model):
    nome = models.CharField(max_length=255)
    eletivo = models.BooleanField(default=False)
    permite_reeleicao = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
