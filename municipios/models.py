from django.db import models

class Municipio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, default='PA', verbose_name="UF")

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.estado}"
